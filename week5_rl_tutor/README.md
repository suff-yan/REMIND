# Week 5 — RL inside the live tutor (End-term)

Read **Handbook §9–10**. Then:
```bash
python scripts/train_scheduler.py          # warm-start Q-table from simulated students
# in .env: REMIND_DAY_SECONDS=60   (1 tutor-day = 1 minute)
streamlit run app/streamlit_app.py
```
Ask a few questions, wait, and watch the tutor interrupt you with recall checks. Every grade updates the Q-table in `data/q_table.json`.

## 🏁 End-term brief
**Part A — Core (required).** Your own Re-Mind tutor (you may start from `app/streamlit_app.py`) that:
1. extracts a concept from each question and stores it as an item in JSON;
2. asks the RL agent (pre-trained in simulation) for the gap until the next quiz;
3. quizzes **on its own** when an item is due;
4. grades with Gemini (0/1/2, JSON) and uses the grade as reward to **update the Q-table online**;
5. has a Socratic mode toggle.

**Part B — Pick at least one extension.**
- a bandit that learns which **quiz style** works best for you (Week 3 → product)
- add difficulty / topic type to the RL state; retrain and benchmark
- a dashboard: recall curve per concept, Q-table heatmap, reward over time
- replace Q-learning with a function approximator (e.g. logistic regression over features)
- import an Anki/CSV deck as items
- anything you can justify!

**Part C — Benchmark & demo.** Compare your scheduler against Leitner in simulation (`scripts/benchmark.py`) and record a ≤ 3-minute demo.

**Part D — Report** (`report_template.md`, ≤ 4 pages): design, reward design, results, one failure case and one case where the reward could be hacked.

Submit: GitHub repo link + demo video + report PDF via the form.
