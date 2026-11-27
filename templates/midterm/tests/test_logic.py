"""Mid-term autograder (public half). Run: python -m pytest -q
A hidden half with more edge cases is run by the mentors."""
import os, random, sys
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic import should_quiz, pick_topic, due_items, parse_grade

NOW = datetime(2026, 12, 20, 18, 0, 0)


def test_should_quiz():
    assert [should_quiz(c) for c in range(1, 7)] == [False, False, False, False, True, False]
    assert should_quiz(3, n=3)


def test_pick_topic():
    qs = ["a", "b", "c"]
    assert pick_topic(qs, random.Random(0)) in qs
    try:
        pick_topic([], random.Random(0)); assert False
    except ValueError:
        pass


def test_due_items():
    items = [
        {"query": "old", "asked_at": (NOW - timedelta(minutes=30)).isoformat(), "quizzed": False},
        {"query": "new", "asked_at": (NOW - timedelta(minutes=2)).isoformat(), "quizzed": False},
        {"query": "done", "asked_at": (NOW - timedelta(minutes=50)).isoformat(), "quizzed": True},
        {"query": "edge", "asked_at": (NOW - timedelta(minutes=10)).isoformat(), "quizzed": False},
    ]
    assert [i["query"] for i in due_items(items, NOW)] == ["old", "edge"]


def test_parse_grade():
    assert parse_grade('{"grade": 2, "feedback": "ok"}') == {"grade": 2, "feedback": "ok"}
    assert parse_grade('```json\n{"grade": 0, "feedback": "no"}\n```')["grade"] == 0
    for bad in ["", "Correct!", '{"grade": 7}', '{"feedback": "x"}', "null"]:
        assert parse_grade(bad)["grade"] == 1
