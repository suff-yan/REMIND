---
title: "Context: remembering the conversation"
minutes: 40
checkpoint:
  kind: local
  title: Feel the difference
  steps:
    - "Run the Week 1 bot. Ask 'What is entropy?', then 'Give me an example.' Notice it doesn't know what 'it' is."
    - "Run `streamlit run week2_agentic_chatbot/examples/context_chat.py` and ask the same two questions."
    - "Read `to_gemini()` in that file and explain to yourself why `assistant` becomes `model`."
    - "Change MAX_TURNS to 2 and see when the bot starts forgetting."
quiz:
  - q: "Why did the Week 1 bot fail at 'give me an example'?"
    options: ["The model is too small", "Each call sent only the latest message, with no history", "Streamlit lost the message", "The key expired"]
    answer: 1
    explain: "The model only knows what you send in that call."
  - q: "Why send only the last ~20 messages instead of everything?"
    options: ["Gemini can't read more than 20", "Every token costs quota and time, and old turns rarely matter", "Streamlit limits it", "JSON can't store more"]
    answer: 1
    explain: "A sliding window keeps cost bounded."
  - q: "Gemini rejects a conversation whose first message has role 'model'. When trimming, what should you make sure?"
    options: ["Nothing", "The trimmed list still starts with a user message", "It has an even length", "It ends with a model message"]
    answer: 1
    explain: "Drop a leading model turn after slicing. You'll implement this in the next section's checkpoint."
  - q: "Where should the conversation be kept so the next rerun can send it?"
    options: ["A local variable", "st.session_state (and optionally a JSON file)", "The API key", "A global constant"]
    answer: 1
    explain: "Reruns wipe normal variables."
resources:
  - label: Gemini API, multi-turn conversations
    url: https://ai.google.dev/gemini-api/docs/text-generation#multi-turn-conversations
  - label: What is a context window? (IBM)
    url: https://www.ibm.com/think/topics/context-window
---
## The problem

Ask the Week 1 bot "What is entropy?" and then "Give me an example." It has no idea what you mean, because each call sends only your latest message. The model has no memory of its own; it only knows what you send in that call.

## The fix: send the conversation

```python
def to_gemini(messages):
    return [types.Content(role="user" if m["role"] == "user" else "model",
                          parts=[types.Part.from_text(text=m["content"])])
            for m in messages]

resp = client.models.generate_content(model=MODEL, contents=to_gemini(messages[-20:]))
```

Two details:

- Streamlit calls the bot `assistant`; Gemini calls it `model`. Translate when sending.
- `messages[-20:]` is a **sliding window**. Every token you send costs quota and time, and turns from 40 messages ago rarely matter. A slice can start on a `model` turn, which Gemini rejects, so drop it if it does.

## The context window

Models have a maximum amount of text they can read at once: the **context window**. Ours is huge, but cost isn't. Agents in production summarise old turns, or store facts in memory and fetch only the relevant ones. That's exactly what Re-Mind's concept memory does in Week 5.
