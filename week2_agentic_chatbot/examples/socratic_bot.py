"""Week 2 - Socratic tutor using a SYSTEM INSTRUCTION (not a prompt pasted into the chat).

    streamlit run week2_agentic_chatbot/examples/socratic_bot.py
"""
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

SOCRATIC = """You are a Socratic tutor. Guide the student with short questions instead of
answers. Ask ONE question at a time and stop - never write the student's reply yourself.
If the student is stuck after two attempts, give a small hint. If they say "just tell me",
first ask what they think, then explain briefly."""

st.title("🏛️ Socratic tutor")
st.session_state.setdefault("messages", [])
for m in st.session_state.messages:
    st.chat_message(m["role"]).markdown(m["content"])

if prompt := st.chat_input("What do you want to understand?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    contents = [types.Content(role="user" if m["role"] == "user" else "model",
                              parts=[types.Part.from_text(text=m["content"])])
                for m in st.session_state.messages]
    resp = client.models.generate_content(
        model=MODEL, contents=contents,
        config=types.GenerateContentConfig(system_instruction=SOCRATIC, temperature=0.7))
    st.session_state.messages.append({"role": "assistant", "content": resp.text})
    st.chat_message("assistant").markdown(resp.text)
