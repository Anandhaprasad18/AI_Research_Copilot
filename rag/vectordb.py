from typing import Dict, Optional, Tuple
import os

from langchain_community.vectorstores import FAISS

from rag.embeddings import get_embeddings
from rag.splitter import split_documents
from utils.user_state import get_user_document_path

# Cache vector stores per user and selected document.
_vector_db: Dict[Tuple[str, str], Optional[FAISS]] = {}


def _vectordb_folder(username: Optional[str], document_name: Optional[str]) -> str:
    base = os.path.join("data", "vectordb")
    user = (username or "guest").strip() or "guest"
    doc = (document_name or "default").strip() or "default"
    return os.path.join(base, user, doc)


def create_vector_db(username: Optional[str] = None, document_name: Optional[str] = None, force_rebuild: bool = False):
    """Build (or return the cached) FAISS vector store for a user/document pair.
    Tries to load a persisted index from disk; if not present it builds
    from document chunks and saves the index for future reuse.
    """
    key = (username or "", document_name or "")
    if key in _vector_db and not force_rebuild:
        return _vector_db[key]

    folder = _vectordb_folder(username, document_name)
    embeddings = get_embeddings()

    # Try to load an existing persisted index (best-effort)
    try:
        if os.path.isdir(folder):
            store = FAISS.load_local(folder, embeddings)
            _vector_db[key] = store
            return store
    except Exception:
        pass

    # Build from source documents
    file_path = get_user_document_path(username, document_name)
    if not file_path:
        _vector_db[key] = None
        return None

    chunks = split_documents(file_path)
    if not chunks:
        _vector_db[key] = None
        return None

    store = FAISS.from_documents(chunks, embeddings)
    try:
        os.makedirs(folder, exist_ok=True)
        store.save_local(folder)
    except Exception:
        # best-effort: if saving fails, continue without persistence
        pass

    _vector_db[key] = store
    return store


def reset_vector_db(username: Optional[str] = None, document_name: Optional[str] = None):

    key = (username or "", document_name or "")
    _vector_db.pop(key, None)

    folder = _vectordb_folder(username, document_name)
    try:
        if os.path.isdir(folder):
            for fname in os.listdir(folder):
                try:
                    os.remove(os.path.join(folder, fname))
                except Exception:
                    pass
    except Exception:
        pass
