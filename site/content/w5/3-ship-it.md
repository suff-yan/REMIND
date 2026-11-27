---
title: Run it, extend it, ship it
minutes: 120
checkpoint:
  kind: local
  title: End-term checklist
  steps:
    - "`python scripts/train_scheduler.py` to warm-start the Q-table."
    - "Set `REMIND_DAY_SECONDS=60` in `.env`, then `streamlit run app/streamlit_app.py`."
    - "Ask 3–4 questions, wait two minutes, and answer the recall checks the tutor starts on its own."
    - "Open `data/memory.json` and find the reward and gap history of one concept."
    - "Copy `templates/endterm/` into your own repo `remind-endterm-<roll>` and make `python -m pytest -q` pass."
    - "Build your Part B extension and describe it in `extension/EXTENSION.md`."
    - "Run `python cup/evaluate.py data/q_table.json`, beat Leitner (~84), and upload your entry on the Cup page."
    - "Record a demo of 3 minutes or less, write the report, and submit on the End-term page."
quiz:
  - q: "What file do you upload to the Re-Mind Cup?"
    options: ["Your app.py", "A JSON with your Q-table ('q') or policy", "Your report", "Your .env"]
    answer: 1
    explain: "data/q_table.json already has the right shape."
  - q: "The Cup score is..."
    options: ["exam pass rate", "average recall % minus reviews per concept, on hidden students", "number of reviews", "your quiz accuracy"]
    answer: 1
    explain: "Recall rewarded, effort penalised, scored on students you've never seen."
  - q: "What must a good demo show?"
    options: ["Only the code", "An agentic interruption (a quiz nobody asked for) and an online update", "The API key", "The slides"]
    answer: 1
    explain: "Those two moments are the whole project in thirty seconds."
  - q: "What's the best kind of failure case for your report?"
    options: ["Hide failures", "A specific, reproducible situation where the tutor does something wrong, and why", "A typo", "None"]
    answer: 1
    explain: "Honest analysis beats ten screenshots."
resources:
  - label: End-term brief
    url: /endterm
  - label: The Re-Mind Cup
    url: /cup
  - label: Report template
    url: https://github.com/suff-yan/REMIND/blob/main/week5_rl_tutor/report_template.md
---
## Run the whole thing

```bash
python scripts/train_scheduler.py          # ~5 s, writes data/q_table.json
streamlit run app/streamlit_app.py
```

Ask a few questions, wait, and the tutor interrupts you with recall checks. The sidebar switches between Socratic and direct mode, and between the RL and Leitner schedulers, so you can compare them live.

## Extend it (Part B)

Pick at least one, or propose your own:

- a **quiz-style bandit**: Week 3 meets the product;
- a **richer state** (difficulty, topic type), retrained and re-benchmarked;
- a **dashboard**: recall curve per concept, Q-table heatmap, reward over time;
- **function approximation** instead of a table;
- **Anki / CSV import**.

## Enter the Cup (Part C)

Your trained table is already a valid entry:

```bash
python cup/evaluate.py data/q_table.json    # public seed, same formula as the leaderboard
```

Beat Leitner (~84), then upload on the [Cup page](/cup). Entries are re-scored every night on hidden students.

## Report and demo (Part D)

Four pages at most, from the template: your design choices, your reward and why, honest results against Leitner, one failure case, and one way your reward could be hacked and how you stopped it. Plus a demo of three minutes or less that shows an interruption and an online update. Submit on the [End-term page](/endterm).
