"""MID-TERM task B - timebot.py  (fill in every TODO)

Save the time of every question in a JSON file. On every rerun, check whether any
question is older than QUIZ_AFTER_MINUTES and not yet quizzed -> quiz on it.
"""
import json
import os
from datetime import datetime, timedelta

import streamlit as st

DATA_FILE = "timebot_memory.json"
QUIZ_AFTER_MINUTES = 10


def load():
    # TODO 1: safe-load the JSON file (missing / empty file -> {"items": []})
    ...


def save(data):
    # TODO 2
    ...


def due_items(data, now=None):
    now = now or datetime.now()
    # TODO 3: return items where quizzed is False and now - asked_at >= QUIZ_AFTER_MINUTES
    #   hint: datetime.fromisoformat(item["asked_at"]) and timedelta(minutes=...)
    ...

# TODO 4: build the chat UI. Store each question as
#   {"query": ..., "answer": ..., "asked_at": datetime.now().isoformat(), "quizzed": False}
# TODO 5: before showing the input box, call due_items(); if one is due, quiz on it.
# Hint for testing: set QUIZ_AFTER_MINUTES = 1 while developing.
