import os
from langchain_community.document_loaders import PyPDFLoader


def load_documents(file_path: str = "data/pdfs"):
    if os.path.isdir(file_path):
        os.makedirs(file_path, exist_ok=True)
        documents = []
        for filename in sorted(os.listdir(file_path)):
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(file_path, filename))
                documents.extend(loader.load())
        return documents

    if file_path.endswith(".pdf"):
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        loader = PyPDFLoader(file_path)
        return loader.load()

    os.makedirs(file_path, exist_ok=True)
    return []
