"""Re-Mind v2 - run with:  streamlit run app/streamlit_app.py

Tip: put REMIND_DAY_SECONDS=60 in .env so that "1 day" = 1 minute during demos.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from remind import prompts
from remind.llm import LLM
from remind.tutor import Tutor, DAY_SECONDS
from remind.env import GAPS
from remind.memory_model import GRADE_NAMES

st.set_page_config(page_title="Re-Mind", page_icon="🧠", layout="wide")

with st.sidebar:
    st.title("🧠 Re-Mind")
    mode = st.radio("Tutor mode", ["Direct", "Socratic"], horizontal=True)
    sched = st.radio("Scheduler", ["rl", "leitner"], horizontal=True)
    st.caption(f"1 'day' = {DAY_SECONDS:g} s  (set REMIND_DAY_SECONDS in .env)")

if "tutor" not in st.session_state or st.session_state.get("sched") != sched:
    q_path = "data/q_table.json"
    os.makedirs("data", exist_ok=True)
    st.session_state.tutor = Tutor(LLM(), store_path="data/memory.json", q_path=q_path, scheduler=sched)
    st.session_state.sched = sched
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("quiz", None)

tutor: Tutor = st.session_state.tutor
llm = tutor.llm
if llm.offline:
    st.warning("No GEMINI_API_KEY found - running in offline mode.")

# ---------------- chat column ----------------
chat_col, mem_col = st.columns([2, 1])
with chat_col:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Agentic step: before the student even asks, check if something is due.
    due = tutor.due_items()
    if due and st.session_state.quiz is None:
        item = due[0]
        q = tutor.make_quiz(item)
        st.session_state.quiz = {"item": item, "question": q}
        msg = f"⏰ **Quick recall check on _{item['topic']}_**\n\n{q}"
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.rerun()

    placeholder = "Answer the quiz..." if st.session_state.quiz else "Ask anything..."
    if user := st.chat_input(placeholder):
        st.session_state.messages.append({"role": "user", "content": user})
        if st.session_state.quiz:                       # answering a quiz
            quiz = st.session_state.quiz
            grade, fb, r, gap = tutor.grade_and_learn(quiz["item"], quiz["question"], user)
            reply = (f"**{GRADE_NAMES[grade].title()}** - {fb}\n\n"
                     f"reward = `{r:+.2f}` · next review in **{gap} day(s)**")
            st.session_state.quiz = None
        else:                                            # normal tutoring turn
            system = prompts.SOCRATIC if mode == "Socratic" else prompts.DIRECT
            reply = llm.chat(st.session_state.messages[-12:], system=system)
            item = tutor.remember(user, reply)
            reply += f"\n\n_🧠 saved **{item['topic']}** - I'll quiz you in {GAPS[item['gap_action']]} day(s)._"
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ---------------- memory column ----------------
with mem_col:
    st.subheader("What I remember about you")
    import time
    for it in sorted(tutor.items, key=lambda i: i["next_due"]):
        mins = (it["next_due"] - time.time()) / DAY_SECONDS
        st.markdown(f"**{it['topic']}** · streak {it['streak']} · "
                    f"{'due now' if mins <= 0 else f'due in {mins:.1f} d'}")
    if st.button("Save & reset chat"):
        tutor.save()
        st.session_state.messages = []
        st.rerun()
