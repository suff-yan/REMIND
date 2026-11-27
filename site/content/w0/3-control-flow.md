---
title: "Python II: loops, conditions and functions"
minutes: 60
checkpoint:
  kind: browser
  title: Which topics are due?
  prompt: "Each topic has the day it was last reviewed and a gap in days. Write `due_topics(items, today)` returning the names of topics whose next review day (last + gap) is today or earlier, most overdue first."
  starter: |
    items = [
        {"topic": "APIs", "last": 1, "gap": 2},      # due on day 3
        {"topic": "JSON", "last": 4, "gap": 7},      # due on day 11
        {"topic": "Bandits", "last": 0, "gap": 1},   # due on day 1
    ]

    def due_topics(items, today):
        due = []
        # TODO: loop over items, keep those with last + gap <= today
        # TODO: sort most overdue first (smallest last + gap first)
        return [x["topic"] for x in due]

    print(due_topics(items, today=5))
  tests: |
    assert due_topics(items, 5) == ["Bandits", "APIs"], due_topics(items, 5)
    assert due_topics(items, 0) == []
    assert due_topics(items, 11) == ["Bandits", "APIs", "JSON"]
    print("due_topics works")
quiz:
  - q: "How many times does the body run in `for i in range(3):`?"
    options: ["2", "3", "4", "It depends on i"]
    answer: 1
    explain: "range(3) gives 0, 1, 2."
  - q: "What does a function return if it has no `return` statement?"
    options: ["0", "An empty string", "None", "It raises an error"]
    answer: 2
    explain: "Every Python function returns None by default."
  - q: "Which line keeps only the even numbers of `xs`?"
    options: ["[x for x in xs if x % 2 == 0]", "[x % 2 for x in xs]", "xs.filter(even)", "[x for x in xs and x % 2]"]
    answer: 0
    explain: "A list comprehension with an `if` filter."
  - q: "`sorted(items, key=lambda x: x[\"gap\"])` sorts by...?"
    options: ["the dict's first key", "the value of \"gap\", smallest first", "alphabetical order of topics", "random order"]
    answer: 1
    explain: "`key` tells sorted what to compare; ascending by default."
  - q: "Why write `def is_due(item, now)` instead of reading the clock inside the function?"
    options: ["It's faster", "You can test it with any fake time instead of waiting", "Python requires it", "It uses less memory"]
    answer: 1
    explain: "Passing `now` in makes the function testable. You'll use this trick for every scheduler in the project."
  - q: "What does `while not done:` do when `done` is False?"
    options: ["Never runs", "Runs the body, and keeps going until done becomes True", "Runs exactly once", "Raises an error"]
    answer: 1
    explain: "`not False` is True, so the loop runs until something sets done = True. Every RL episode loop looks like this."
resources:
  - label: Official tutorial, control flow
    url: https://docs.python.org/3/tutorial/controlflow.html
  - label: Real Python, list comprehensions
    url: https://realpython.com/list-comprehension-python/
---
## Conditions

```python
if grade == 0:
    streak = 0
elif grade == 1:
    streak += 1
else:
    streak += 2
```

## Loops

`for` walks over a collection; `while` repeats until a condition changes. Reinforcement learning is literally a `while` loop: act, observe, learn, until the episode is done.

```python
for item in items:
    print(item["topic"])

done = False
while not done:
    done = step()
```

**List comprehensions** build lists in one line: `[x["topic"] for x in items if x["gap"] > 3]`.

## Functions

Functions name a piece of logic so you can test it and reuse it:

```python
def next_review(last_day, gap):
    return last_day + gap
```

A habit that will save you hours: **pass the current time in** instead of reading the clock inside the function. `is_due(item, now)` can be tested with a fake `now`; a function that calls `datetime.now()` itself can only be tested by waiting.

## Sorting with a key

```python
sorted(items, key=lambda x: x["last"] + x["gap"])
```

`lambda` is a tiny unnamed function. Here it tells `sorted` to compare items by their due day.
