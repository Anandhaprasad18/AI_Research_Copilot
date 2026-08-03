from langgraph.graph import StateGraph, START, END
from graph.state import State
from graph.router import route
from graph.nodes import rag, search, both, writter


builder=StateGraph(State)
builder.add_node("rag",rag)
builder.add_node("writter",writter)
builder.add_node("search",search)
builder.add_node("both",both)
builder.add_conditional_edges(START, route,{"rag":"rag","search":"search","both":"both"})
builder.add_edge("rag", "writter")
builder.add_edge("search", "writter")
builder.add_edge("both","search")
graph=builder.compile()