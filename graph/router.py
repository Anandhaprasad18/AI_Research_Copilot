from graph.state import State
def route(state: State):
    question=state["question"].lower()
    if ("latest" in question or "recent" in question or "new" in question or "current" in question or "today" in question or "now" in question):
        return "both"
    if ("policy" in question or "pdf" in question or "document" in question or "manual" in question or "report" in question):
        return "rag"
    return "search"