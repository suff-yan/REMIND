"""MID-TERM task A - counterbot.py  (fill in every TODO)

The bot answers normally, counts the student's questions and - WITHOUT being asked -
quizzes them on a random one of the last N questions when the counter hits N.
"""
import os
import random

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
N = 5

st.title("🔢 Counterbot")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("recent_questions", [])
st.session_state.setdefault("pending_quiz", None)   # {"topic":..., "question":...}

for m in st.session_state.messages:
    st.chat_message(m["role"]).markdown(m["content"])

if user := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user})
    if st.session_state.pending_quiz:
        # TODO 1: grade `user` against the pending quiz (use the JSON grader from examples/grader.py)
        # TODO 2: show the grade + feedback, then clear pending_quiz
        pass
    else:
        # TODO 3: get a normal answer from Gemini and append it to messages
        # TODO 4: add `user` to recent_questions
        # TODO 5: if len(recent_questions) == N -> pick one with random.choice, ask Gemini for a
        #         quiz question on it, store it in pending_quiz, show it, reset recent_questions
        pass
    st.rerun()
