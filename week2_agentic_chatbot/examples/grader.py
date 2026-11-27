"""Week 2 - LLM-as-a-grader with STRUCTURED (JSON) output.

Free-text grades ("Correct: ...") are hard for code to use. Asking Gemini for JSON
gives us a number we can store, compare and - in Week 5 - turn into an RL reward.

    python week2_agentic_chatbot/examples/grader.py
"""
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

GRADE_PROMPT = """You are a strict but fair examiner.
Key fact: {fact}
Question: {question}
Student answer: {answer}
Return JSON: {{"grade": 0|1|2, "feedback": "<one sentence>"}}
0 = wrong or forgot, 1 = partly right / hesitant, 2 = clearly correct."""


def grade(fact, question, answer):
    resp = client.models.generate_content(
        model=MODEL,
        contents=GRADE_PROMPT.format(fact=fact, question=question, answer=answer),
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0),
    )
    try:
        data = json.loads(resp.text)
        return int(data["grade"]), data.get("feedback", "")
    except (json.JSONDecodeError, KeyError, ValueError):
        return 1, "could not parse grade - defaulting to 1"


if __name__ == "__main__":
    fact = "Q-learning updates Q(s,a) toward r + gamma * max_a' Q(s',a')."
    q = "What target does Q-learning move Q(s,a) towards?"
    for ans in ["r + gamma times the best Q of the next state", "the average reward", "something with gamma?"]:
        print(ans, "->", grade(fact, q, ans))
