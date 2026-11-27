"""Week 1 - your first API call.   python week1_foundations/examples/hello_gemini.py"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

# Which models can my key use? (names change every few months - always check!)
for m in client.models.list():
    if "flash" in m.name:
        print(m.name)

resp = client.models.generate_content(model=MODEL, contents="Explain spaced repetition in 2 lines.")
print("\n" + resp.text)
