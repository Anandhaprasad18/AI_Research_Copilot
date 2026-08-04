from rag.loader import load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(file_path: str = "data/pdfs"):
    documents = load_documents(file_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return text_splitter.split_documents(documents)