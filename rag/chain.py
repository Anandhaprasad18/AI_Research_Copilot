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


# Cache the compiled chain so normal questions don't rebuild the retriever
# every time. Call get_rag_chain(force_rebuild=True) after indexing new PDFs.



def get_rag_chain(force_rebuild: bool = False):
    global rag_chain

    if rag_chain is not None and not force_rebuild:
        return rag_chain

    retriever = create_retriever(force_rebuild)

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
    return rag_chain

def reset_rag_chain():
    global rag_chain
    rag_chain = None
# Backward-compatible module-level reference (built on first import, using
# whatever PDFs already exist in data/pdfs at that point).
