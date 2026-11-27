"""Week 1 - a Gemini clone that remembers every chat in a JSON file.

    streamlit run week1_foundations/examples/app.py
"""
import json
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemini Clone", page_icon="💬")
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
DATA_FILE = "chat_history.json"


# ---------------- JSON memory ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"interactions": []}
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:            # empty / corrupted file
        return {"interactions": []}


def save_interaction(query, response):
    data = load_data()
    data["interactions"].append({"query": query, "response": response,
                                 "time": datetime.now().isoformat()})
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- UI ----------------
st.title("💬 Gemini clone with saved history")
st.caption(f"Every chat is stored in `{DATA_FILE}` - open it while you chat!")

if "chat" not in st.session_state:
    st.session_state.chat = []

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask anything..."):
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=user_input)])],
        )
        reply = response.text
    except Exception as e:                  # quota, network, wrong model name...
        reply = f"⚠️ API error: {e}"
    st.session_state.chat.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
    save_interaction(user_input, reply)

with st.sidebar:
    st.header("Saved history")
    for item in load_data()["interactions"][-10:]:
        st.markdown(f"**Q:** {item['query']}\n\n*{item['time'][:16]}*\n\n---")
