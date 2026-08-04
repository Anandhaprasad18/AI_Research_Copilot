"""
Central configuration for the AI Research Copilot.

Loads environment variables and exposes a single shared `llm` instance
that every node/chain in the app (rag chain, writer node, etc.) imports.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


class DummyLLM:
    def __init__(self):
        self.model = "dummy"

    def invoke(self, prompt):
        class Response:
            def __init__(self, content):
                self.content = content

        warning = (
            "GROQ_API_KEY is not configured. The backend is running, "
            "but the language model is unavailable."
        )
        return Response(
            f"{warning}\n\nPrompt received:\n{prompt}"
        )


if GROQ_API_KEY:
    try:
        from langchain_groq import ChatGroq

        llm = ChatGroq(
            model=GROQ_MODEL,
            groq_api_key=GROQ_API_KEY,
            temperature=0.3,
        )
    except Exception:
        llm = DummyLLM()
else:
    llm = DummyLLM()
