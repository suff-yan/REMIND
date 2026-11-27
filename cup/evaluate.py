"""Re-Mind Cup scorer.

Score = average recall (%) - reviews per concept      (higher is better)
  e.g. RL reference 96.8 - 11.8 = 85.0 · Leitner 93.3 - 10.0 = 83.3 · daily review 99.5 - 60 = 39.5
Both reward hacks from Week 4 score badly, so they can't win.

Entry format (JSON), either:
  {"q": [[...6 floats...] x 18]}      a Q-table (greedy action is used)
  {"policy": [18 ints in 0..5]}       an action index per state (state = streak*3 + last_grade)

Local:   python cup/evaluate.py my_q_table.json          (public seed, 2000 students)
Nightly: python cup/evaluate.py --supabase               (hidden seed from CUP_SEED, scores every entry)
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from remind.env import N_ACTIONS, N_STATES, SpacedRepetitionEnv
from remind.schedulers import evaluate


def to_policy(entry):
    if "policy" in entry:
        pol = [int(a) for a in entry["policy"]]
    elif "q" in entry:
        q = entry["q"]
        if len(q) != N_STATES or any(len(r) != N_ACTIONS for r in q):
            raise ValueError(f"q must be {N_STATES}x{N_ACTIONS}")
        pol = [max(range(N_ACTIONS), key=lambda a: float(row[a])) for row in q]
    else:
        raise ValueError('entry needs "q" or "policy"')
    if len(pol) != N_STATES or not all(0 <= a < N_ACTIONS for a in pol):
        raise ValueError(f"policy must be {N_STATES} ints in 0..{N_ACTIONS-1}")
    return pol


def score(entry, seed=2026, n=2000):
    pol = to_policy(entry)
    m = evaluate(lambda streak, grade: pol[min(streak, 5) * 3 + grade],
                 lambda s: SpacedRepetitionEnv(seed=s), n=n, seed=seed)
    return {"score": round(100 * m["retention"] - m["reviews"], 2),
            "retention": round(100 * m["retention"], 2), "reviews": round(m["reviews"], 2),
            "exam_pass": round(100 * m["exam_pass"], 2)}


def _req(method, path, body=None):
    url = os.environ["SUPABASE_URL"].rstrip("/") + "/rest/v1/" + path
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"apikey": key, "Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        txt = r.read().decode()
        return json.loads(txt) if txt else None


def run_supabase():
    seed = int(os.environ.get("CUP_SEED", "777"))
    for e in _req("GET", "cup_entries?select=roll,entry"):
        try:
            res = score(e["entry"], seed=seed, n=3000)
            patch = {**res, "error": None}
        except Exception as ex:
            patch = {"score": None, "error": str(ex)[:200]}
        patch["evaluated_at"] = datetime.now(timezone.utc).isoformat()
        _req("PATCH", f"cup_entries?roll=eq.{e['roll']}", patch)
        print(e["roll"], patch)


if __name__ == "__main__":
    if sys.argv[1:] == ["--supabase"]:
        run_supabase()
    else:
        print(json.dumps(score(json.load(open(sys.argv[1]))), indent=2))
