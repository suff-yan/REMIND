---
title: APIs and API keys
minutes: 40
video: w1_request
videoTitle: One request, end to end
checkpoint:
  kind: local
  title: Get your key and keep it secret
  steps:
    - "Open https://aistudio.google.com/apikey, sign in with a Google account and click Create API key."
    - "In the REMIND folder run `cp .env.example .env` and paste your key after `GEMINI_API_KEY=`."
    - "Run `git status` and confirm `.env` is NOT listed (it's in `.gitignore`)."
    - "Never paste your key into code, a screenshot, or the WhatsApp group."
quiz:
  - q: "In the restaurant analogy, what is the API?"
    options: ["The kitchen", "The waiter", "The menu prices", "The customer"]
    answer: 1
    explain: "You hand requests to the waiter (API); the kitchen (Gemini's servers) does the work you never see."
  - q: "Why must an API key stay out of your code?"
    options: ["It slows Python down", "Anyone who sees it can use your quota as you", "Python can't read long strings", "GitHub deletes it"]
    answer: 1
    explain: "A key is a password for your account's usage. Pushed to GitHub, it can be scraped within minutes."
  - q: "Where does Re-Mind read the key from?"
    options: ["Hard-coded in app.py", "An environment variable loaded from .env", "A cookie", "The Streamlit sidebar"]
    answer: 1
    explain: "`load_dotenv()` reads `.env` into environment variables and `os.getenv(\"GEMINI_API_KEY\")` fetches it."
  - q: "You get error 429 RESOURCE_EXHAUSTED. Most likely?"
    options: ["Your code has a syntax error", "You hit the free-tier rate limit; wait or slow down", "The key is wrong", "The internet is down"]
    answer: 1
    explain: "429 means too many requests. Wait a minute or switch to a lite model."
  - q: "What does an SDK add on top of a raw API?"
    options: ["More intelligence", "Ready-made Python functions so you don't build HTTP requests by hand", "A free key", "A user interface"]
    answer: 1
    explain: "google-genai wraps the HTTP calls in functions like client.models.generate_content."
resources:
  - label: Gemini API quickstart (Python)
    url: https://ai.google.dev/gemini-api/docs/quickstart
  - label: Gemini API rate limits
    url: https://ai.google.dev/gemini-api/docs/rate-limits
  - label: What is a REST API? (MDN, HTTP overview)
    url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
---
## What is an API?

Gemini is a model with billions of parameters running on Google's servers. You will never run it on your laptop, and you don't need to. You talk to it through an **API** (Application Programming Interface): a doorway into a big system. You pass a request through the door; a result comes back.

Think of a restaurant. Gemini is the **kitchen**: expert chefs and equipment you can't touch. The API is the **waiter**. You say "write a quiz question about Newton's laws", the waiter carries it to the kitchen, and a moment later brings back a finished answer. You cooked nothing, yet you get the whole kitchen's skill.

In code, the waiter is one line:

```python
response = client.models.generate_content(model=MODEL, contents="Explain gravity simply.")
print(response.text)
```

## What is an API key?

Millions of people use the same kitchen. Gemini needs to know **who** is ordering and how much they're allowed. Your **API key** is that identity card: a long secret string sent with every request.

Because it's as powerful as a password, it never goes in your code. It lives in a file called `.env`:

```bash
GEMINI_API_KEY=your-key-here
GEMINI_MODEL=gemini-3.1-flash-lite
```

and your program reads it at runtime:

```python
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
```

`.env` is listed in `.gitignore`, so git never uploads it.

## The SDK

You could send raw HTTP requests, but Google ships a **Software Development Kit** (`google-genai`) that turns them into Python functions. That's the only Gemini library we use this year. Old tutorials show `google.generativeai` and `genai.configure(...)`: that library is deprecated, so skip any code that uses it.
