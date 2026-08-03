"""
Standalone RAG agent.

Wraps the PDF-grounded rag_chain as a LangChain Tool so it can be dropped
into a tool-calling agent (e.g. alongside tools/search.py) if you want an
LLM-driven router instead of the keyword router in graph/router.py.
"""

from langchain_core.tools import tool

from rag.chain import get_rag_chain


@tool
def rag_agent(question: str) -> str:
    """Answer a question using only the content of the indexed PDF documents."""
    return get_rag_chain().invoke(question)
