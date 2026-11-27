---
title: The architecture of Re-Mind 2.0
minutes: 45
video: w5_system
videoTitle: One concept's life
quiz:
  - q: "Which file decides when the next quiz happens?"
    options: ["app/streamlit_app.py", "remind/tutor.py via the Q-learning agent", "remind/prompts.py", ".env"]
    answer: 1
    explain: "The UI asks the tutor; the tutor asks the agent for a gap."
  - q: "What does the tutor store for each concept?"
    options: ["Only the question text", "topic, fact, streak, last grade, last review time, next due time, history", "The whole chat", "The API key"]
    answer: 1
    explain: "Everything the agent's state and reward need, plus a history for your report."
  - q: "How does the tutor 'interrupt' you?"
    options: ["A push notification", "On every rerun it checks due_items() and opens a quiz before you type", "Gemini decides", "It emails you"]
    answer: 1
    explain: "The perceive step from Week 2, now driven by the agent's schedule."
  - q: "Why extract a concept with Gemini instead of quizzing on the raw question?"
    options: ["Raw questions are often messy; a topic plus one key fact makes a cleaner quiz and grade", "It's cheaper", "Streamlit needs it", "No reason"]
    answer: 0
    explain: "'what's the thing where you discount future rewards' becomes {topic: discounting, fact: ...}."
  - q: "The same 18 states and reward are used live and in simulation. Why does that matter?"
    options: ["It doesn't", "So the Q-table pre-trained on simulated students still means the same thing on a real one", "It saves memory", "Gemini requires it"]
    answer: 1
    explain: "That's what makes the warm start possible."
resources:
  - label: remind/tutor.py
    url: https://github.com/suff-yan/REMIND/blob/main/remind/tutor.py
  - label: app/streamlit_app.py
    url: https://github.com/suff-yan/REMIND/blob/main/app/streamlit_app.py
---
Everything you've built, in one app.

| File | Job |
|---|---|
| `app/streamlit_app.py` | chat UI, Socratic/direct toggle, RL/Leitner toggle, memory panel |
| `remind/tutor.py` | the agent: remember, schedule, quiz, grade, learn |
| `remind/llm.py`, `prompts.py` | Gemini: answer, extract a concept, write a quiz, grade (JSON) |
| `remind/rl/qlearning.py` | choose the gap; update from reward |
| `data/memory.json`, `data/q_table.json` | what it remembers about you; what it has learned |

## One concept's life

1. **Ask.** "What is a Q-table?" Gemini answers, directly or Socratically.
2. **Extract.** Gemini returns `{"topic": "Q-table", "fact": "..."}`. The tutor stores an item with `streak = 0`, `last_grade = 0`.
3. **Schedule.** The agent looks at state $(0, \text{forgot})$ and picks a gap, say 1 day. `next_due` is set.
4. **Interrupt.** On every rerun the tutor checks `due_items()`. When one is due, it opens a recall check before you type anything.
5. **Grade.** Gemini returns `{"grade": 0|1|2, "feedback": ...}`.
6. **Learn.** Reward = ± the days actually waited − 1, exactly as in simulation; one Q-update; a new gap is chosen.

Steps 1–5 are Week 2's agent. Step 6 is Weeks 3–4's RL. This week connects them.
