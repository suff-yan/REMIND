# End-term — “Re-Mind: an agent that learns when you'll forget”
**Released:** start of Week 5 · **Due:** end of Week 5 (23:59 IST) · **Cup leaderboard** updates nightly until the deadline.

## Problem statement
Build your own Re-Mind tutor in which a reinforcement-learning agent decides when to quiz the student, and keeps learning from the student's answers.

**Part A — Core (required).** A Streamlit tutor that:
1. extracts the concept behind each question (Gemini, JSON) and stores it as an item in JSON;
2. asks an RL agent, pre-trained on simulated students, for the gap before the next quiz;
3. quizzes **on its own** when an item is due;
4. grades with Gemini (0/1/2, JSON) and uses the grade as reward to **update the Q-table online**;
5. has a Socratic-mode toggle.

**Part B — Extension (at least one).** Quiz-style bandit · richer RL state (difficulty / topic type) re-benchmarked · learning dashboard · function approximation instead of a table · Anki/CSV import · your own (justify it).

**Part C — Re-Mind Cup.** Submit your best scheduler as `cup/entry.json`. Every night it is scored on **3,000 hidden simulated students**:
> **Score = average recall (%) − reviews per concept**
Reference points (public seed): Leitner ≈ 84, course RL agent ≈ 85. Review-every-day ≈ 40. Reward hacks score badly by design.

**Part D — Report & demo.** ≤ 4-page report (template provided) and a ≤ 3-minute demo video.

## Submission format
1. Copy `templates/endterm/` into a **public GitHub repo** `remind-endterm-<roll>`; `python -m pytest -q` must pass offline.
2. On the course site → **End-term**: submit the repo link, video link and report link, and upload `cup/entry.json` to enter the Cup (re-upload any time before the deadline; the last upload counts).
3. Never commit `.env`.

## Evaluation (100)
| Part | Marks | What we look for |
|---|---|---|
| A · Core tutor | 35 | all five behaviours work from the README; sensible state/reward handling |
| B · Extension | 20 | ambition × execution; justified in `EXTENSION.md` |
| C · Cup | 15 | 10 for a valid entry beating Leitner on hidden students; +5 scaled by rank |
| D · Report | 20 | design reasoning, honest results vs Leitner, one failure case, one hackable reward and how you prevented it |
| D · Demo | 10 | clear, ≤ 3 min, shows an agentic interruption and an online update |

**Completion:** mid-term pass + end-term ≥ 50. Top Cup entries get a shout-out (and yes, merch).
