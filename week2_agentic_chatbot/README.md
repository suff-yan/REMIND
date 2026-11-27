# Week 2 — The agentic chatbot

Read **Handbook §4–5**. Run every file in `examples/` and read it line by line.

| file | idea |
|---|---|
| `examples/context_chat.py` | send the conversation, not one message; `user`/`model` roles; trimming history |
| `examples/grader.py` | LLM-as-grader with JSON output → a number your code can use |
| `examples/socratic_bot.py` | system instructions; one question at a time |

## 📝 Mid-term (due end of Week 2) — full brief: `docs/assessments/MIDTERM.md`
1. **`counterbot.py`** — counts questions; after N=5 it quizzes you on a random one of them *without being asked*, then resets. Start from `../templates/midterm/`.
2. **`timebot.py`** — stores the time of each question; quizzes you on any question older than 10 minutes. Start from `../templates/midterm/` (use 1 minute while testing).
3. **`gradebot.py`** — combine either bot with the JSON grader: every quiz answer gets `{grade: 0|1|2, feedback}` and the grade is saved to the JSON memory file.

Submit a Drive/GitHub link with the three files via the form. AI use is fine — you must be able to explain the code.
