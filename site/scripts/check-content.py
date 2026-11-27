"""Validate content: YAML parses, quizzes well-formed, and each browser checkpoint
FAILS with the starter code and PASSES with the mentor solution (mentor_solutions/checkpoints/<id>.py)."""
import contextlib, io, os, re, sys, glob, yaml
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
sys.path.insert(0, REPO)
bad = 0
for f in sorted(glob.glob(os.path.join(ROOT, "content", "w*", "*.md"))):
    txt = open(f).read()
    fm = yaml.safe_load(txt.split("---")[1])
    week = re.search(r"w(\d)", f).group(1); slug = re.match(r"\d+-(.+)\.md", os.path.basename(f)).group(1)
    sid = f"{week}-{slug}"
    for i, q in enumerate(fm.get("quiz", [])):
        assert 0 <= q["answer"] < len(q["options"]) and q["explain"], (sid, i)
    cp = fm.get("checkpoint")
    status = f"quiz={len(fm.get('quiz', []))}"
    if cp and cp["kind"] == "browser":
        def run(code):
            ns = {}
            with contextlib.redirect_stdout(io.StringIO()):
                try:
                    exec(code, ns); exec(cp["tests"], ns); return True
                except Exception as e:
                    return e
        starter = run(cp["starter"])
        solf = os.path.join(REPO, "mentor_solutions", "checkpoints", sid + ".py")
        sol = run(open(solf).read()) if os.path.exists(solf) else "NO SOLUTION"
        ok = starter is not True and sol is True
        status += f" starter_fails={starter is not True} solution_passes={sol is True}" + ("" if sol is True else f" ({sol!r})")
        bad += not ok
    print(("OK  " if "False" not in status and "NO SOL" not in status else "BAD ") + sid, status)
sys.exit(1 if bad else 0)
