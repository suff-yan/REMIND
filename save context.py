treamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import json
import os

# ---------------- CONFIG ----------------

st.set_page_config(page_title="Gemini Chatbot", layout="centered")
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

HISTORY_FILE = "chat_history.json"

# ---------------- HELPERS ----------------

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# ---------------- UI ----------------

st.title("💬 Gemini Chatbot")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT LOGIC ----------------

user_input = st.chat_input("Ask something...")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Build context for Gemini
    context = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content']}\n"

    # Generate response
    response = model.generate_content(context)

    assistant_reply = response.text

    # Display assistant message
    st.chat_message("assistant").markdown(assistant_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    # Save to JSON
    save_history(st.session_state.messages)

