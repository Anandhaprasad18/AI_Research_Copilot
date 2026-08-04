from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import llm
from rag.retriever import create_retriever

prompt = ChatPromptTemplate.from_template(
    """
You are an AI Research Assistant.
Answer ONLY from the given context.
If the answer is not available,
say you don't know.
Context:
{context}
Question:
{question}
Answer:
"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Cache chains per user and selected document.
rag_chains = {}


def get_rag_chain(username: Optional[str] = None, document_name: Optional[str] = None, force_rebuild: bool = False):
    key = (username or "", document_name or "")
    if key in rag_chains and not force_rebuild:
        return rag_chains[key]

    retriever = create_retriever(username=username, document_name=document_name, force_rebuild=force_rebuild)
    rag_chain = (
        RunnableParallel(
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    rag_chains[key] = rag_chain
    return rag_chain


def reset_rag_chain(username: Optional[str] = None, document_name: Optional[str] = None):
    key = (username or "", document_name or "")
    rag_chains.pop(key, None)