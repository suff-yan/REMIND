---
title: "Python I: values, lists and dictionaries"
minutes: 60
video: w0_python
videoTitle: Python as labels and boxes
checkpoint:
  kind: browser
  title: Summarise a quiz log
  prompt: "Each attempt is a dictionary. Fill in `summarise` so it returns how many attempts there were, the average score, and the topic with the best single score. Press Run checks when ready."
  starter: |
    log = [
        {"topic": "APIs", "score": 2},
        {"topic": "JSON", "score": 1},
        {"topic": "Bandits", "score": 2},
        {"topic": "JSON", "score": 0},
    ]

    def summarise(attempts):
        count = 0          # TODO: how many attempts?
        mean = 0.0         # TODO: average of the "score" values
        best_topic = None  # TODO: topic of the highest score (first one if tied)
        return {"count": count, "mean": mean, "best_topic": best_topic}

    print(summarise(log))
  tests: |
    assert summarise(log) == {"count": 4, "mean": 1.25, "best_topic": "APIs"}, summarise(log)
    assert summarise([{"topic": "x", "score": 0}])["best_topic"] == "x"
    assert summarise([{"topic": "a", "score": 1}, {"topic": "b", "score": 3}])["mean"] == 2.0
    print("summarise works")
quiz:
  - q: "After `a = [1, 2]` and `b = a` and `b.append(3)`, what is `a`?"
    options: ["[1, 2]", "[1, 2, 3]", "[3]", "An error"]
    answer: 1
    explain: "`b = a` doesn't copy the list; both names point at the same list object."
  - q: "Which is the right way to read the value for key \"score\" from a dict `d`?"
    options: ["d.score", "d(score)", "d[\"score\"]", "d->score"]
    answer: 2
    explain: "Square brackets with the key. `d.get(\"score\")` also works and returns None if the key is missing."
  - q: "What is `type(3 / 2)` in Python 3?"
    options: ["int", "float", "str", "bool"]
    answer: 1
    explain: "`/` always returns a float (1.5). Use `//` for integer division."
  - q: "Which structure would you use to store one chat message with its role, text and time?"
    options: ["A list of three strings", "A dict like {\"role\": ..., \"content\": ..., \"time\": ...}", "Three separate variables", "A tuple of numbers"]
    answer: 1
    explain: "A dict names each field, which is exactly what JSON stores later."
  - q: "`scores = [2, 0, 1]`. What is `scores[-1]`?"
    options: ["2", "0", "1", "An error"]
    answer: 2
    explain: "Negative indices count from the end; -1 is the last item."
  - q: "What does `len({\"a\": 1, \"b\": 2})` return?"
    options: ["1", "2", "3", "4"]
    answer: 1
    explain: "`len` of a dict counts its keys."
resources:
  - label: Official Python tutorial, chapters 3 and 5
    url: https://docs.python.org/3/tutorial/introduction.html
  - label: Python Tutor (see your code's boxes and arrows step by step)
    url: https://pythontutor.com/visualize.html
    note: perfect companion to the animation
  - label: CS50P lecture 0 (Harvard, video)
    url: https://cs50.harvard.edu/python/
---
You need surprisingly little Python for this project: values, a few containers, loops, functions, and a way to save things. This section covers the first half.

## Names point at values

In Python, `x = 5` doesn't put 5 "inside" x. It makes the **name** `x` point at a value `5`. That's why this surprises people:

```python
a = [1, 2]
b = a          # b points at the SAME list
b.append(3)
print(a)       # [1, 2, 3]
```

Keep this picture in mind; the animation below draws it.

## The four types you'll use everywhere

| Type | Example | Used for |
|---|---|---|
| `int`, `float` | `3`, `0.9` | counts, probabilities, rewards |
| `str` | `"What is entropy?"` | questions, answers, prompts |
| `bool` | `True` | "was this recalled?" |
| `None` | `None` | "nothing yet" |

## Lists: things in order

```python
scores = [2, 0, 1]
scores.append(2)      # add to the end
scores[0]             # first item -> 2
scores[-1]            # last item  -> 2
len(scores)           # 4
```

## Dictionaries: named fields

A dict maps **keys** to **values**. Almost every piece of data in Re-Mind is a dict, because dicts become JSON almost for free:

```python
item = {"topic": "Q-learning", "streak": 2, "last_grade": 1}
item["streak"]            # 2
item["streak"] += 1       # update
item.get("missing", 0)    # 0, no crash
```

A list of dicts is a tiny database. The chat history, the quiz log and the concept memory in Re-Mind are all lists of dicts.
