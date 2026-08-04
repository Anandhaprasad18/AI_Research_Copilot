from typing import Optional
from langchain_core.runnables import RunnableLambda

from rag.vectordb import create_vector_db


def create_retriever(username: Optional[str] = None, document_name: Optional[str] = None, force_rebuild: bool = False):
    vector_db = create_vector_db(username=username, document_name=document_name, force_rebuild=force_rebuild)
    if vector_db is None:
        return RunnableLambda(lambda _query: [])
    return vector_db.as_retriever(search_kwargs={"k": 3})
