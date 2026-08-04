from typing import Dict, Optional, Tuple

from langchain_community.vectorstores import FAISS

from rag.embeddings import get_embeddings
from rag.splitter import split_documents
from utils.user_state import get_user_document_path

# Cache vector stores per user and selected document.
_vector_db: Dict[Tuple[str, str], Optional[FAISS]] = {}


def create_vector_db(username: Optional[str] = None, document_name: Optional[str] = None, force_rebuild: bool = False):
    """Build (or return the cached) FAISS vector store for a user/document pair."""
    key = (username or "", document_name or "")
    if key in _vector_db and not force_rebuild:
        return _vector_db[key]

    file_path = get_user_document_path(username, document_name)
    if not file_path:
        _vector_db[key] = None
        return None

    chunks = split_documents(file_path)
    if not chunks:
        _vector_db[key] = None
        return None

    embeddings = get_embeddings()
    _vector_db[key] = FAISS.from_documents(chunks, embeddings)
    return _vector_db[key]


def reset_vector_db(username: Optional[str] = None, document_name: Optional[str] = None):
    """Force the next create_vector_db() call to rebuild from scratch."""
    key = (username or "", document_name or "")
    _vector_db.pop(key, None)
