"""Thin wrapper around the Gemini API (google-genai SDK).

* Reads GEMINI_API_KEY and GEMINI_MODEL from .env
* Falls back to an offline 'echo' model when no key is set, so the app and the
  tests still run (useful on a plane, or when your free quota runs out).
"""
import json
import os

from dotenv import load_dotenv

load_dotenv()
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")


class LLM:
    def __init__(self, model=DEFAULT_MODEL, api_key=None):
        self.model = model
        key = api_key or os.getenv("GEMINI_API_KEY")
        self.offline = not key
        if not self.offline:
            from google import genai
            self.client = genai.Client(api_key=key)

    # ---------- plain text ----------
    def chat(self, messages, system=None):
        """messages: list of {"role": "user"|"assistant", "content": str}"""
        if self.offline:
            return f"(offline mode) You said: {messages[-1]['content']}"
        from google.genai import types
        contents = [types.Content(role="user" if m["role"] == "user" else "model",
                                  parts=[types.Part.from_text(text=m["content"])])
                    for m in messages]
        config = types.GenerateContentConfig(system_instruction=system) if system else None
        resp = self.client.models.generate_content(model=self.model, contents=contents, config=config)
        return resp.text

    # ---------- structured JSON ----------
    def json(self, prompt, fallback):
        """Ask for JSON and parse it. Returns `fallback` on any failure."""
        if self.offline:
            return fallback
        from google.genai import types
        try:
            resp = self.client.models.generate_content(
                model=self.model, contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"))
            return json.loads(resp.text)
        except Exception:
            return fallback
