"""Mid-term: pure logic, no Streamlit. The autograder imports THIS file.

Keep every function pure (inputs -> output, no API calls, no files) so it can be
tested. Your three bots import these functions and add the UI + Gemini calls.
"""
import json
from datetime import datetime, timedelta


def should_quiz(question_count: int, n: int = 5) -> bool:
    """True exactly when the counter has reached n (and n, 2n, 3n ... if you never reset)."""
    raise NotImplementedError


def pick_topic(recent_questions: list, rng) -> str:
    """Return one of recent_questions using rng.choice. Raise ValueError if empty."""
    raise NotImplementedError


def due_items(items: list, now: datetime, minutes: int = 10) -> list:
    """items: [{"query", "asked_at": iso-string, "quizzed": bool}, ...]
    Return the items not yet quizzed whose age is >= `minutes`, oldest first."""
    raise NotImplementedError


def parse_grade(raw: str) -> dict:
    """raw: the text Gemini returned for a grading prompt.
    Return {"grade": 0|1|2, "feedback": str}. Must never raise:
    on bad JSON / missing keys / out-of-range grade return {"grade": 1, "feedback": "unparseable"}.
    Hint: models sometimes wrap JSON in ```json fences - strip them."""
    raise NotImplementedError
