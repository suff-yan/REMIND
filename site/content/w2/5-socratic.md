---
title: Socratic mode
minutes: 40
checkpoint:
  kind: local
  title: Make it ask, not tell
  steps:
    - "Run `streamlit run week2_agentic_chatbot/examples/socratic_bot.py` and ask it to explain gradient descent."
    - "Check it asks ONE question and stops, instead of writing your reply for you."
    - "Try 'just tell me the answer' and see how it responds."
    - "Edit the SOCRATIC instruction to add a rule of your own and test it."
    - "Then: the mid-term (link below). Start from `templates/midterm/` in the repo."
quiz:
  - q: "What's the main idea of Socratic tutoring?"
    options: ["Give the answer quickly", "Guide the student to the answer with questions", "Quiz at fixed times", "Never answer"]
    answer: 1
    explain: "Questions expose gaps; working through them builds understanding."
  - q: "Last year the bot sometimes invented the student's replies. What fixes that best?"
    options: ["A longer prompt in the user message", "A system instruction that says to ask one question and stop", "A bigger model", "Higher temperature"]
    answer: 1
    explain: "System instructions hold for the whole chat and outrank the conversation."
  - q: "Where is a system instruction passed?"
    options: ["As the first user message", "In GenerateContentConfig(system_instruction=...)", "In .env", "In st.title"]
    answer: 1
    explain: "It's part of the config, separate from the messages."
  - q: "The student says 'just tell me'. A good Socratic tutor first..."
    options: ["refuses forever", "asks what they think and why, then explains briefly if still stuck", "ends the chat", "gives a quiz"]
    answer: 1
    explain: "Respect the request, but make them think once first."
resources:
  - label: Mid-term brief
    url: /midterm
  - label: Gemini API, system instructions
    url: https://ai.google.dev/gemini-api/docs/text-generation
---
## About the method

The Socratic way of studying is learning by questioning instead of absorbing. Each question forces clarity; each vague answer shows exactly where understanding is shallow. Combined with Feynman's habit of explaining things simply, it builds understanding rather than recognition.

## System instructions

Last year we pasted the Socratic rules into the user's message, and the bot sometimes wrote a whole fake conversation with itself. The fix is a **system instruction**, a personality that holds for the entire chat:

```python
SOCRATIC = """You are a Socratic tutor. Guide the student with short questions instead of
answers. Ask ONE question at a time and stop - never write the student's reply yourself.
If the student is stuck after two attempts, give a small hint."""

config = types.GenerateContentConfig(system_instruction=SOCRATIC, temperature=0.7)
```

Good rules are concrete and testable: "one question, then stop" beats "be Socratic".

## Mid-term

You now have everything for the [mid-term](/midterm): three bots that act without being asked, with logic you can test. Read the brief, copy `templates/midterm/`, and make the public tests pass.
