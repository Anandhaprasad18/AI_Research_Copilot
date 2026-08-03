from rag.vectordb import create_vector_db


def create_retriever(force_rebuild: bool = False):
    vector_db = create_vector_db(force_rebuild)
    return vector_db.as_retriever(search_kwargs={"k": 3})
