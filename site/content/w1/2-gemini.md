---
title: Talking to Gemini from Python
minutes: 60
checkpoint:
  kind: local
  title: Your first calls
  steps:
    - "Activate the venv and run `pip install -r requirements.txt` in the REMIND folder."
    - "Run `python week1_foundations/examples/hello_gemini.py`. It lists models your key can use, then answers a question."
    - "If the model name errors, copy a *flash-lite* name from that list into `GEMINI_MODEL` in `.env`."
    - "Open `week1_foundations/01_gemini_basics.ipynb` in VS Code and run every cell."
    - "Change the JSON-output cell to return a quiz question with fields `question` and `answer`."
quiz:
  - q: "What object do you create once and reuse for every Gemini call?"
    options: ["genai.Model()", "genai.Client(api_key=...)", "types.Content()", "st.session_state"]
    answer: 1
    explain: "The client holds your key and connection; every call goes through client.models.generate_content."
  - q: "Gemini calls the assistant's role in a conversation..."
    options: ["assistant", "bot", "model", "system"]
    answer: 2
    explain: "Roles are `user` and `model`. Streamlit uses `assistant`, so we translate when sending history."
  - q: "What does `response_mime_type=\"application/json\"` do?"
    options: ["Makes the reply faster", "Asks Gemini to reply with valid JSON your code can parse", "Encrypts the reply", "Saves the reply to a file"]
    answer: 1
    explain: "JSON mode is how the tutor gets grades and concepts it can store, not free-form prose."
  - q: "A system instruction is..."
    options: ["a message from the user", "a personality and rules that hold for the whole conversation", "an error message", "the API key"]
    answer: 1
    explain: "It's set in GenerateContentConfig and shapes every reply. Socratic mode in Week 2 is a system instruction."
  - q: "Why wrap calls in try/except?"
    options: ["To make them faster", "Network calls can fail (quota, wrong model, no internet) and the app shouldn't crash", "Python requires it", "To hide the key"]
    answer: 1
    explain: "Show the error in the UI and keep going."
  - q: "Your call fails with 'model not found'. First thing to do?"
    options: ["Reinstall Python", "List available models and update GEMINI_MODEL", "Create a new Google account", "Wait an hour"]
    answer: 1
    explain: "Model names change every few months; `client.models.list()` tells you what exists."
resources:
  - label: google-genai SDK reference
    url: https://googleapis.github.io/python-genai/
  - label: Gemini API, structured output
    url: https://ai.google.dev/gemini-api/docs/structured-output
  - label: Gemini API, system instructions
    url: https://ai.google.dev/gemini-api/docs/text-generation
---
## The client and one call

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

resp = client.models.generate_content(model=MODEL, contents="Explain entropy in two lines.")
print(resp.text)
```

## Which model?

Model names change every few months. Never guess; ask:

```python
for m in client.models.list():
    if "flash" in m.name:
        print(m.name)
```

Pick a **flash-lite** model for this project: fast, cheap, and on the free tier.

## Messages with roles

For anything beyond one-shot questions, send structured messages. Each has a **role** (`user` or `model`) and **parts**:

```python
msg = types.Content(role="user", parts=[types.Part.from_text(text="What is a Q-table?")])
resp = client.models.generate_content(model=MODEL, contents=[msg])
```

## Configuration

`GenerateContentConfig` controls *how* Gemini answers:

```python
config = types.GenerateContentConfig(
    system_instruction="You are a tutor. Answer in two sentences, then ask one question.",
    temperature=0.4,                         # lower = more predictable
    response_mime_type="application/json",  # only when you want JSON back
)
```

Three settings, three future features: the **system instruction** becomes Socratic mode, **temperature 0** makes the grader consistent, and **JSON mode** gives the tutor grades and concepts it can store.

## When things fail

```python
try:
    reply = client.models.generate_content(model=MODEL, contents=prompt).text
except Exception as e:
    reply = f"API error: {e}"
```

Free-tier limits, a wrong model name, flaky Wi-Fi: your app should show the problem, not crash.
