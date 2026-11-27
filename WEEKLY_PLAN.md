# Re-Mind v2 · Weekly plan (5 weeks × ~7 hours)

Each week = **reading** (handbook section) → **hands-on** (notebook / example) → **build** (assignment) → **weekly meet** (45–60 min, slides in `docs/slides/`).
Week 1 is self-paced (placement season); its meet is a short async kickoff + doubt thread.

---

## Week 1 — Foundations *(self-paced)*
**Goal:** go from "I know basic Python" to "my code talks to an LLM and remembers things".

| ~h | Activity | Material |
|---|---|---|
| 1.0 | Set up VS Code, Python 3.11+, venv, `.env`, get a Gemini key | Handbook §2 |
| 1.0 | What is an API / API key / SDK; first call; list models | `01_gemini_basics.ipynb`, `examples/hello_gemini.py` |
| 1.5 | JSON for persistent memory, `datetime` for timestamps | `02_json_and_datetime.ipynb` |
| 1.5 | Streamlit basics: `st.chat_input`, `st.chat_message`, `st.session_state` | Handbook §3, Streamlit chat tutorial |
| 2.0 | **Build:** Gemini clone that stores every chat in JSON | `examples/app.py` |

**Deliverable:** your own `app.py` + a screenshot of `chat_history.json` growing.
**Self-check:** Can you explain why we never hard-code the API key? What does Streamlit do on every click?

## Week 2 — The agentic chatbot
**Goal:** the bot stops being passive: it remembers the conversation, decides *by itself* when to quiz you, grades you with structured output, and can teach Socratically.

| ~h | Activity | Material |
|---|---|---|
| 1.0 | Agentic AI vs AI agents; the perceive → decide → act → remember loop | Handbook §4 |
| 1.0 | Context: sending history, `user`/`model` roles, token budget | `examples/context_chat.py` |
| 1.0 | Autonomous triggers: counter-based and time-based quizzes | Handbook §5, last year's `quiz.py` pattern |
| 1.0 | LLM-as-grader with JSON output (`response_mime_type`) | `examples/grader.py` |
| 0.5 | System instructions & Socratic mode | `examples/socratic_bot.py` |
| 2.5 | **Build: MID-TERM** | `starter/counterbot.py`, `starter/timebot.py` |

**Deliverable (mid-term):** `counterbot.py`, `timebot.py`, `gradebot.py` (grader returning 0/1/2 + feedback). Drive / GitHub link via form.

## Week 3 — Reinforcement learning from scratch
**Goal:** understand agents, states, actions, rewards, exploration vs exploitation, and implement Q-learning.

| ~h | Activity | Material |
|---|---|---|
| 1.0 | RL vocabulary; the agent–environment loop | Handbook §6 |
| 2.0 | Bandits: running mean, greedy trap, ε-greedy, UCB, regret | `01_bandits.ipynb` |
| 1.0 | MDPs, return, discount γ, Q-values | Handbook §7 |
| 2.0 | Q-learning in the study-room gridworld | `02_q_learning_gridworld.ipynb` |
| 1.0 | Exercises (decaying ε, γ sweep, SARSA) | both notebooks |

**Deliverable:** both notebooks with exercises answered.

## Week 4 — Spaced repetition: rules vs RL
**Goal:** frame "when should I quiz?" as an MDP, beat a rule-based scheduler, and see reward hacking.

| ~h | Activity | Material |
|---|---|---|
| 1.0 | Forgetting curves, stability, history of schedulers (fixed → Leitner → SM-2 → FSRS) | Handbook §8 |
| 1.5 | Simulated student + Leitner boxes | `01_forgetting_and_leitner.ipynb` |
| 2.0 | Spaced repetition as an MDP; train the Q-learning scheduler | `02_rl_scheduler.ipynb` |
| 1.0 | Rules vs RL benchmark; reading the learned policy | `scripts/benchmark.py` |
| 1.5 | Reward hacking + exercises | notebook §5 |

**Deliverable:** notebooks + a 1-page comparison (plot + what the agent learned + one reward-hacking example).

## Week 5 — RL inside the live tutor + final
**Goal:** connect everything: the Streamlit tutor quizzes you when the RL agent says so, Gemini grades your answer, and the grade becomes the reward that keeps training the agent.

| ~h | Activity | Material |
|---|---|---|
| 1.0 | Architecture walkthrough; sim-to-real; `REMIND_DAY_SECONDS` | Handbook §9, `remind/tutor.py` |
| 2.0 | Integrate: concept extraction → item store → RL gap → quiz → grade → update | `app/streamlit_app.py` |
| 1.5 | Extend: your own feature (see end-term brief) | `week5_rl_tutor/README.md` |
| 1.0 | Benchmark your scheduler; record a 3-min demo | `scripts/benchmark.py` |
| 1.5 | Report: design choices, reward design, failure cases | `week5_rl_tutor/report_template.md` |

**Deliverable (end-term):** repo link + demo video + report (≤ 4 pages).
