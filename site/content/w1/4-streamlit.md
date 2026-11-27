---
title: Streamlit and your first chatbot
minutes: 90
checkpoint:
  kind: local
  title: Week 1 assignment
  prompt: "Build your own app.py. Submit the GitHub or Drive link plus a screenshot of your JSON file in the group form."
  steps:
    - "Run the reference: `streamlit run week1_foundations/examples/app.py` and chat with it."
    - "Open `chat_history.json` while chatting and watch it grow."
    - "Write your own `app.py` from scratch (you may peek): it saves {query, response, time} for every message."
    - "Show the last 10 saved questions in the sidebar."
    - "Bonus: a Clear history button, and a count of questions asked today."
    - "Push it to a GitHub repo (no .env!) and submit the link."
quiz:
  - q: "When does Streamlit re-run your script?"
    options: ["Only at startup", "Top to bottom on every interaction", "Every 10 seconds", "Only when you press F5"]
    answer: 1
    explain: "Every click or message re-runs the whole file. That's the key mental model."
  - q: "You store messages in a normal list `chat = []` at the top of app.py. What happens?"
    options: ["It works fine", "The list is recreated empty on every rerun, so history disappears", "Streamlit crashes", "Messages are saved to disk"]
    answer: 1
    explain: "Use st.session_state for anything that must survive reruns."
  - q: "What's the difference between st.session_state and the JSON file?"
    options: ["None", "session_state lasts for this browser tab; the JSON file lasts forever", "JSON is faster", "session_state is shared by all users"]
    answer: 1
    explain: "Close the tab and session_state is gone; the file stays."
  - q: "What does `if q := st.chat_input(\"Ask\"):` do?"
    options: ["Always runs", "Assigns the typed text to q and runs only if the user sent something", "Clears the input box", "Sends q to Gemini"]
    answer: 1
    explain: "The walrus operator assigns and tests in one go."
  - q: "Which element draws a chat bubble?"
    options: ["st.write", "st.chat_message(role)", "st.sidebar", "st.title"]
    answer: 1
    explain: "`with st.chat_message(\"user\"): st.markdown(text)`."
resources:
  - label: Streamlit, build a basic LLM chat app
    url: https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps
  - label: Streamlit, session state
    url: https://docs.streamlit.io/develop/concepts/architecture/session-state
  - label: Reference app.py in the repo
    url: https://github.com/suff-yan/REMIND/blob/main/week1_foundations/examples/app.py
---
## How Streamlit thinks

Streamlit turns a Python script into a web app. There is one idea to understand: **the whole script re-runs from top to bottom on every interaction**. Type a message: re-run. Click a button: re-run.

So a normal variable is recreated every time. Anything that must survive goes into `st.session_state`, a dict that lives as long as the browser tab:

```python
if "chat" not in st.session_state:
    st.session_state.chat = []
```

## The chatbot, block by block

```python
st.title("Gemini clone with saved history")

for msg in st.session_state.chat:                  # 1. redraw the conversation
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask anything..."): # 2. new message?
    st.session_state.chat.append({"role": "user", "content": user_input})
    reply = client.models.generate_content(model=MODEL, contents=user_input).text
    st.session_state.chat.append({"role": "assistant", "content": reply})
    save_interaction(user_input, reply)            # 3. remember it on disk
```

Run it with `streamlit run app.py`.

## Two kinds of memory

| | Lives for | Used for |
|---|---|---|
| `st.session_state` | this browser tab | what's on screen right now |
| `chat_history.json` | forever | what the tutor will quiz you on later |

## Cheatsheet

| Function | Use |
|---|---|
| `st.title`, `st.caption` | headings |
| `st.chat_message(role)` | a chat bubble |
| `st.chat_input(placeholder)` | the input box; returns text or None |
| `st.sidebar` | side panel for history and controls |
| `st.button(label)` | True on the rerun after a click |
| `st.rerun()` | refresh after you change state |
