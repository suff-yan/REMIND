"""End-term structural checks (public). Run: python -m pytest -q"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def test_required_files_exist():
    for p in ["app/streamlit_app.py", "cup/entry.json", "results/benchmark.json", "report/report.pdf", "README.md"]:
        assert os.path.exists(os.path.join(ROOT, p)), f"missing {p}"


def test_cup_entry_is_valid():
    from remind.env import N_ACTIONS, N_STATES
    e = json.load(open(os.path.join(ROOT, "cup/entry.json")))
    if "policy" in e:
        assert len(e["policy"]) == N_STATES and all(0 <= int(a) < N_ACTIONS for a in e["policy"])
    else:
        assert len(e["q"]) == N_STATES and all(len(r) == N_ACTIONS for r in e["q"])


def test_tutor_offline_roundtrip(tmp_path):
    from remind.llm import LLM
    from remind.tutor import Tutor
    llm = LLM(api_key=None); llm.offline = True
    t = Tutor(llm, store_path=str(tmp_path / "m.json"))
    item = t.remember("What is a Q-table?", "A table of action values.")
    grade, _, r, gap = t.grade_and_learn(item, "q?", "values", now=item["last_review"] + 86400)
    assert grade in (0, 1, 2) and gap >= 1
