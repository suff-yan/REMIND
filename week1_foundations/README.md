# Week 1 — Foundations *(self-paced)*

Read **Handbook §1–3** first.

1. Setup: Python 3.11+, VS Code, `python -m venv venv`, `pip install -r ../requirements.txt`, copy `../.env.example` to `.env`.
2. `examples/hello_gemini.py` — first API call + list the models your key can use.
3. `01_gemini_basics.ipynb` — Client, `generate_content`, `Content`/`Part`, JSON output, system instructions, errors.
4. `02_json_and_datetime.ipynb` — persistent memory and time arithmetic.
5. `examples/app.py` — run it: `streamlit run week1_foundations/examples/app.py`.

## Assignment
Write **your own** `app.py`: a chatbot that saves `{query, response, time}` to JSON and shows the last 10 saved queries in the sidebar.
Bonus: a "Clear history" button; a counter of questions asked today.
Submit: GitHub/Drive link + screenshot.
