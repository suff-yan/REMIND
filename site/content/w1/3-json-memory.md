---
title: "Memory on disk: JSON and time"
minutes: 50
checkpoint:
  kind: browser
  title: A memory that survives restarts
  prompt: "The browser has a tiny file system, so `open()` works here. Make `load_data` safe (missing or broken file returns an empty memory) and make `save_interaction` append and save. The checks delete and corrupt the file to test you."
  starter: |
    import json, os
    from datetime import datetime

    DATA_FILE = "chat_history.json"

    def load_data():
        # TODO: if the file doesn't exist, or isn't valid JSON, return {"interactions": []}
        with open(DATA_FILE) as f:
            return json.load(f)

    def save_data(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def save_interaction(query, response, now=None):
        now = now or datetime.now()
        data = load_data()
        # TODO: append {"query", "response", "time": now.isoformat()} and save
        return data

    save_interaction("What is JSON?", "A text format for data.")
    print(load_data())
  tests: |
    if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
    assert load_data() == {"interactions": []}
    save_interaction("q1", "a1", now=datetime(2026, 12, 20, 18, 0))
    save_interaction("q2", "a2", now=datetime(2026, 12, 20, 18, 5))
    d = load_data()
    assert [i["query"] for i in d["interactions"]] == ["q1", "q2"], d
    assert d["interactions"][1]["time"] == "2026-12-20T18:05:00"
    open(DATA_FILE, "w").write("{broken")
    assert load_data() == {"interactions": []}
    print("memory works")
quiz:
  - q: "`json.dump(data, f)` vs `json.dumps(data)`: what's the difference?"
    options: ["None", "dump writes to a file; dumps returns a string", "dumps is faster", "dump only works on lists"]
    answer: 1
    explain: "The s is for string."
  - q: "Why store time as `datetime.now().isoformat()`?"
    options: ["It's shorter", "JSON has no date type, and ISO strings convert back with fromisoformat", "It's more accurate", "Streamlit requires it"]
    answer: 1
    explain: "Store a string, convert back to a datetime to do arithmetic."
  - q: "Which value can't go into JSON directly?"
    options: ["A dict of lists", "None", "A datetime object", "True"]
    answer: 2
    explain: "datetime isn't JSON-serialisable. Convert it to an ISO string first."
  - q: "What does the safe-load pattern protect against?"
    options: ["Slow disks", "A missing or corrupted file crashing the app", "Viruses", "Wrong API keys"]
    answer: 1
    explain: "First run (no file yet) and a half-written file are both common."
  - q: "`datetime.fromisoformat(a) - datetime.fromisoformat(b)` gives..."
    options: ["a string", "a timedelta you can compare, e.g. >= timedelta(minutes=10)", "an int of seconds", "an error"]
    answer: 1
    explain: "Subtracting datetimes gives a timedelta: the heart of every 'is it due yet?' check."
resources:
  - label: Python docs, json module
    url: https://docs.python.org/3/library/json.html
  - label: Python docs, datetime
    url: https://docs.python.org/3/library/datetime.html
  - label: Course notebook, JSON and datetime
    url: https://github.com/suff-yan/REMIND/blob/main/week1_foundations/02_json_and_datetime.ipynb
---
## Why a file?

While your program runs, its data lives in memory. When it stops, everything is gone. A tutor that forgets every conversation can't quiz you on anything. The `json` module bridges memory and disk: it turns dicts and lists into text and back.

| Function | Direction |
|---|---|
| `json.dump(data, f)` | Python → file |
| `json.load(f)` | file → Python |
| `json.dumps(data)` / `json.loads(s)` | Python ↔ string |

## Load → modify → save

Every memory feature in Re-Mind uses one pattern:

```python
def save_interaction(query, response):
    data = load_data()                       # 1. load what's there
    data["interactions"].append({            # 2. change it
        "query": query, "response": response,
        "time": datetime.now().isoformat(),
    })
    save_data(data)                          # 3. write it back
```

## Load safely

The first time the app runs there is no file; if it crashes mid-write the file may be broken. A safe loader returns an empty memory instead of crashing:

```python
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"interactions": []}
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"interactions": []}
```

## Time

JSON has no date type, so store ISO strings and convert back for arithmetic:

```python
from datetime import datetime, timedelta
stamp = datetime.now().isoformat()                 # '2026-12-20T18:05:00.123456'
elapsed = datetime.now() - datetime.fromisoformat(stamp)
is_due = elapsed >= timedelta(minutes=10)
```

That last line is the seed of every scheduler in the course.
