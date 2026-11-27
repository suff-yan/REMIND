---
title: Acting on its own
minutes: 60
checkpoint:
  kind: browser
  title: Two helpers every agent needs
  prompt: "`trim_history` keeps the last `k` messages but must never start with a `model` turn. `should_interrupt` decides whether to quiz now: after `n` questions since the last quiz, OR `m` minutes since the last quiz (if at least one question was asked)."
  starter: |
    def trim_history(messages, k):
        recent = messages[-k:]
        # TODO: drop leading messages whose role is "model"
        return recent

    def should_interrupt(questions_since_quiz, minutes_since_quiz, n=5, m=10):
        # TODO
        return False

    chat = [{"role": "user", "content": "hi"}, {"role": "model", "content": "hello"},
            {"role": "user", "content": "what is RL?"}, {"role": "model", "content": "..."}]
    print(trim_history(chat, 3))
  tests: |
    t = trim_history(chat, 3)
    assert [m["role"] for m in t] == ["user", "model"], t
    assert trim_history(chat, 10) == chat
    assert trim_history([{"role": "model", "content": "x"}], 5) == []
    assert should_interrupt(5, 0) and should_interrupt(1, 10)
    assert not should_interrupt(4, 9.9) and not should_interrupt(0, 60)
    assert should_interrupt(3, 3, n=3, m=99)
    print("both helpers work")
quiz:
  - q: "In the pending-quiz pattern, how does the bot know the next message is an answer?"
    options: ["It asks Gemini", "A flag in session_state says a quiz is open", "Answers start with 'A:'", "It can't know"]
    answer: 1
    explain: "`st.session_state.pending_quiz` holds the open question until it's graded."
  - q: "Where should the clock check for a time-based quiz go?"
    options: ["Only inside the button handler", "At the top of every rerun, before drawing the input box", "In a separate thread", "In the JSON file"]
    answer: 1
    explain: "Every rerun is a chance to notice something is due. That's the 'perceive' step."
  - q: "Why test `should_interrupt(questions, minutes)` instead of calling datetime.now() inside it?"
    options: ["It's shorter", "So it can be tested instantly with any numbers", "datetime is slow", "Streamlit forbids it"]
    answer: 1
    explain: "Pure functions are testable. The mid-term autograder relies on this."
  - q: "Both triggers are...?"
    options: ["learned by RL", "hand-written rules: the thing RL will replace", "random", "decided by Gemini"]
    answer: 1
    explain: "This week the timing is a rule we chose. By Week 5 a Q-learning agent chooses it."
  - q: "Your counterbot quizzes on question #5 every time, never a random one. Likely bug?"
    options: ["random.choice was called on the latest question instead of the list", "The API key", "Streamlit caching", "JSON encoding"]
    answer: 0
    explain: "Pick from the list of recent questions, then reset the list."
resources:
  - label: Mid-term brief
    url: /midterm
  - label: Streamlit, st.rerun
    url: https://docs.streamlit.io/develop/api-reference/execution-flow/st.rerun
---
This is where the chatbot becomes an agent: it starts conversations, not just answers them.

## Trigger 1: a counter

Keep the recent questions in session state. After each answer, append; when there are $n$ of them, pick one at random, ask Gemini for a quiz question on it, open a pending quiz, and reset the list.

## Trigger 2: a clock

Save `asked_at` for every question. At the **top of every rerun**, before drawing anything else, check what is at least 10 minutes old and not yet quizzed. If something is, quiz on it first. The bot interrupts *you*.

## The pending-quiz pattern

Both bots need to know whether the next message is a new question or an answer to a quiz:

```python
if user := st.chat_input():
    if st.session_state.pending_quiz:          # it's an ANSWER
        grade, feedback = grade_answer(st.session_state.pending_quiz, user)
        st.session_state.pending_quiz = None
    else:                                      # it's a QUESTION
        reply = answer(user)
        maybe_start_quiz()                     # counter or clock decides
```

One flag in session state lets a quiz stay open across reruns.

## Logic apart from UI

Write the decisions as **pure functions** (inputs → output, no Streamlit, no API) and call them from the UI. You can test them in a second without clicking through a chat. The mid-term requires exactly this split: a `logic.py` that we autograde.
