# api/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from graph.graph import graph

router = APIRouter()


# -----------------------------
# Request Schema
# -----------------------------

class ChatRequest(BaseModel):
    question: str


# -----------------------------
# Response Schema
# -----------------------------

class ChatResponse(BaseModel):
    answer: str
    rag_answer: str
    web_result: str


# -----------------------------
# Chat Endpoint
# -----------------------------

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    result = graph.invoke(
        {
            "question": request.question,
            "documents": [],
            "retry_count": 0,
            "reflection": "",
            "context": "",
            "route": "",
            "web_result": "",
            "final_answer": "",
            "rag_answer": "",
        }
    )

    return ChatResponse(
        answer=result["final_answer"],
        rag_answer=result["rag_answer"],
        web_result=result["web_result"]
    )