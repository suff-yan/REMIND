# Mid-term — “From chatbot to agent”
**Released:** start of Week 2 · **Due:** end of Week 2 (23:59 IST, date on the course site) · **Weight:** pass/fail for completion + feedback

## Problem statement
Build three Streamlit bots that act **without being asked**, on top of the Week 1 memory chatbot.

| File | Must do |
|---|---|
| `counterbot.py` | Answer normally. After every **5** questions, quiz the student on a **random one of those 5**, grade the answer, reset the counter. |
| `timebot.py` | Store the time of each question in JSON. On every rerun, if a question is **≥ 10 min old** and not yet quizzed, quiz on it before anything else. |
| `gradebot.py` | Take either bot and grade every quiz answer with Gemini in **JSON mode** → `{"grade": 0|1|2, "feedback"}`; append each graded attempt to `grades.json`. |

All decision logic goes in **`logic.py`** as pure functions (`should_quiz`, `pick_topic`, `due_items`, `parse_grade`). The bots import them. This split is the main software-design lesson: logic you can test, UI you can change.

## Submission format
1. **Use the template:** copy `templates/midterm/` into a new **public GitHub repo** named `remind-midterm-<roll>`.
2. Public tests must pass: `python -m pytest -q`.
3. Fill in `README.md` and add a **≤ 2-minute screen recording** link (unlisted YouTube or Drive, viewable by anyone with the link).
4. Submit the repo link on the course site → **Mid-term** page. Re-submitting before the deadline overwrites.
5. Never commit `.env`.

## Evaluation (100)
| Part | Marks | How |
|---|---|---|
| `logic.py` correctness | 40 | public + hidden tests (edge cases: empty history, exact 10-min boundary, malformed JSON) |
| Bots work end-to-end | 30 | mentors run each bot from the README |
| Code clarity & structure | 15 | readable, logic separated from UI, no hard-coded keys |
| README + recording | 15 | explains what was built and shows all three bots |

**Pass mark:** 50. Late by ≤ 48 h: −10. AI tools allowed; you must be able to explain any line if asked.
