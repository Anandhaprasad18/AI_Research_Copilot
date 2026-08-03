import os
from langchain_community.document_loaders import PyPDFLoader


def load_documents(file_path: str = "data/pdfs"):
    os.makedirs(file_path, exist_ok=True)

    documents = []
    for filename in os.listdir(file_path):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(file_path, filename))
            documents.extend(loader.load())
    return documents
