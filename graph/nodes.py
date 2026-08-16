from graph.state import State
from rag.chain import get_rag_chain
from tools.search import search_tool
from config import llm
from utils.user_state import get_active_document, get_user_profile


def rag(state: State):
    question = state["question"]
    username = state.get("username", "")
    active_document = state.get("active_document") or get_active_document(username)
    state["active_document"] = active_document or ""
    state["rag_answer"] = get_rag_chain(username, active_document).invoke(question)
    return state


def search(state: State):
    question = state["question"]
    rag=state.get("rag_answer", "")
    if rag:
        state["web_result"]=search_tool.invoke(f"{question} this is the document = {rag}")
        return state
    state["web_result"] = search_tool.invoke(question)
    return state


def both(state: State):
    question = state["question"]
    username = state.get("username", "")
    active_document = state.get("active_document") or get_active_document(username)
    state["active_document"] = active_document or ""
    state["rag_answer"] = get_rag_chain(username, active_document).invoke(question)
    return state


def writter(state: State):
    username = state.get("username", "")
    profile = get_user_profile(username) if username else {}
    personalization = profile.get("personalization", "No personal instructions yet.")
    active_document = state.get("active_document", "") or profile.get("active_document", "")

    prompt = f"""
You are an AI Research Assistant for {username or 'the current user'}.
User personalization: {personalization}
Selected document: {active_document or 'No document selected yet'}
Question: {state['question']}
PDF context answer: {state.get('rag_answer', 'N/A')}
Web search results: {state.get('web_result', 'N/A')}
Generate a concise, polished answer that is easy to read and answers only what is needed. Do not overwhelm the user.
"""
    state["personalization"] = personalization
    state["final_answer"] = llm.invoke(prompt).content
    return state
