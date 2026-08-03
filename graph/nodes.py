from graph.state import State
from rag.chain import get_rag_chain
from tools.search import search_tool
from config import llm


def rag(state: State):
    question = state["question"]
    state["rag_answer"] = get_rag_chain(force_rebuild=False).invoke(question)
    return state


def search(state: State):
    question = state["question"]
    state["web_result"] = search_tool.invoke(question)
    return state


def both(state: State):
    question = state["question"]
    state["rag_answer"] = get_rag_chain(force_rebuild=False).invoke(question)
    return state


def writter(state: State):
    prompt = f"""
You are an AI Research assistant who is the greatest of all llms these are the contents
Question: {state["question"]} Pdf context answer: {state.get("rag_answer", "N/A")} and web search results: {state.get("web_result", "N/A")} generate a complete answer so the user should be satisfied. give a complete answer"""
    state["final_answer"] = llm.invoke(prompt).content
    return state
