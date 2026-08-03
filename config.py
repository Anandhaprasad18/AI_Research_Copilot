"""
Central configuration for the AI Research Copilot.

Loads environment variables and exposes a single shared `llm` instance
that every node/chain in the app (rag chain, writer node, etc.) imports.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY is not set. Add it to your .env file, e.g.\n"
        "GROQ_API_KEY=gsk_your_key_here"
    )

# llama-3.3-70b-versatile was deprecated by Groq (June 2026); gpt-oss-120b is
# their recommended, currently-supported replacement. Override via env var
# if you'd rather use a different model.
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

llm = ChatGroq(
    model=GROQ_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
)
