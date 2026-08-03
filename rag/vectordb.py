from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from rag.embeddings import get_embeddings
from rag.splitter import split_documents

# Module-level cache so we don't re-embed every document on every question.
_vector_db = None


def create_vector_db(force_rebuild: bool = False):
    """Build (or return the cached) FAISS vector store.

    Pass force_rebuild=True after adding new PDFs to data/pdfs to re-index.
    """
    global _vector_db

    if _vector_db is not None and not force_rebuild:
        return _vector_db

    chunks = split_documents()
    embeddings = get_embeddings()
    _vector_db = FAISS.from_documents(chunks, embeddings)
    return _vector_db


def reset_vector_db():
    """Force the next create_vector_db() call to rebuild from scratch."""
    global _vector_db
    _vector_db = None
