"""Week 2 - chat WITH context: Gemini sees the whole conversation every turn.

    streamlit run week2_agentic_chatbot/examples/context_chat.py
"""
import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
HISTORY_FILE = "context_history.json"
MAX_TURNS = 20          # only send the last 20 messages -> saves tokens


def load_history():
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def to_gemini(messages):
    """Our {"role","content"} dicts -> Gemini Content objects. Note: Gemini calls the bot 'model'."""
    return [types.Content(role="user" if m["role"] == "user" else "model",
                          parts=[types.Part.from_text(text=m["content"])]) for m in messages]


st.title("🧵 Chat with memory of the conversation")
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

for m in st.session_state.messages:
    st.chat_message(m["role"]).markdown(m["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    resp = client.models.generate_content(model=MODEL, contents=to_gemini(st.session_state.messages[-MAX_TURNS:]))
    st.session_state.messages.append({"role": "assistant", "content": resp.text})
    st.chat_message("assistant").markdown(resp.text)
    with open(HISTORY_FILE, "w") as f:
        json.dump(st.session_state.messages, f, indent=2)
