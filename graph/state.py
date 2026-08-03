from typing import TypedDict,List
from langchain_core.documents import Document

class State(TypedDict):
    question : str
    documents : List[Document]
    retry_count : int
    reflection : str
    context : str
    route : str
    web_result : str
    final_answer : str
    rag_answer : str
