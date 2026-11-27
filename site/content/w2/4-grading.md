---
title: Grading with structured output
minutes: 45
checkpoint:
  kind: browser
  title: Trust, but validate
  prompt: "Gemini already returned JSON and you parsed it into a dict. Write `clean_grade(obj)` that returns `{\"grade\": int, \"feedback\": str}` if the grade is 0, 1 or 2 (accept \"2\" as a string too), and `None` for anything else."
  starter: |
    def clean_grade(obj):
        # TODO: obj may be a dict, or something else entirely
        return None

    print(clean_grade({"grade": 2, "feedback": "Spot on."}))
  tests: |
    assert clean_grade({"grade": 2, "feedback": "ok"}) == {"grade": 2, "feedback": "ok"}
    assert clean_grade({"grade": "1", "feedback": "meh"}) == {"grade": 1, "feedback": "meh"}
    assert clean_grade({"grade": 0}) == {"grade": 0, "feedback": ""}
    for bad in [{"grade": 3}, {"grade": "two"}, {"feedback": "x"}, None, [], "2", {"grade": None}]:
        assert clean_grade(bad) is None, bad
    print("clean_grade works")
quiz:
  - q: "Why ask for JSON instead of 'Start with Correct: or Incorrect:'?"
    options: ["JSON is shorter", "Code can read a number reliably; free text breaks in surprising ways", "Gemini prefers JSON", "It's free"]
    answer: 1
    explain: "A grade your code can use becomes data: stored, averaged, and in Week 5 turned into a reward."
  - q: "Why temperature=0 for grading?"
    options: ["Faster replies", "More consistent: the same answer should get the same grade", "Lower cost", "Required by JSON mode"]
    answer: 1
    explain: "Grading should be predictable, not creative."
  - q: "What do grades 0 / 1 / 2 mean in Re-Mind?"
    options: ["bad / ok / great essay", "forgot or wrong / partly right or hesitant / clearly correct", "easy / medium / hard question", "no / maybe / yes"]
    answer: 1
    explain: "These three numbers are what the RL agent observes in Weeks 4 and 5."
  - q: "JSON mode is on, but you still validate the result. Why?"
    options: ["You don't need to", "Valid JSON can still have the wrong keys or an out-of-range grade", "To slow things down", "Python requires it"]
    answer: 1
    explain: "JSON mode guarantees syntax, not meaning."
resources:
  - label: Gemini API, structured output with a schema
    url: https://ai.google.dev/gemini-api/docs/structured-output
  - label: Reference grader.py
    url: https://github.com/suff-yan/REMIND/blob/main/week2_agentic_chatbot/examples/grader.py
---
## A grade your code can use

Last year the examiner replied in prose starting with "Correct:" or "Incorrect:". Fine for a human, painful for code. This year we ask for **JSON**:

```python
resp = client.models.generate_content(
    model=MODEL,
    contents=GRADE_PROMPT.format(fact=fact, question=q, answer=a),
    config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0),
)
data = json.loads(resp.text)      # {"grade": 2, "feedback": "Spot on."}
```

## Three grades, remember them

| Grade | Meaning |
|---|---|
| **0** | forgot, or wrong |
| **1** | partly right, or hesitant |
| **2** | clearly correct |

In Week 5 these numbers become what the RL agent sees, and the reward it learns from.

## Validate anyway

JSON mode guarantees the reply *parses*, not that it makes sense. A grade of `7`, a missing key or the string `"two"` will happen eventually, so check before you trust it, and fall back to a safe default (grade 1) rather than crash.
