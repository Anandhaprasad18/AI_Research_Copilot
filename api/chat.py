# api/chat.py

from fastapi import APIRouter
from pydantic import BaseModel

from graph.graph import graph
from utils.user_state import get_active_document, get_user_profile

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    username: str = ""
    active_document: str = ""


class ChatResponse(BaseModel):
    answer: str
    rag_answer: str
    web_result: str
    active_document: str = ""
    personalization: str = ""


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    username = (request.username or "").strip() or "guest"
    profile = get_user_profile(username)
    requested_document = (request.active_document or "").strip()
    active_document = requested_document or profile.get("active_document", "") or get_active_document(username) or ""

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
            "username": username,
            "personalization": profile.get("personalization", ""),
            "active_document": active_document,
        }
    )

    return ChatResponse(
        answer=result["final_answer"],
        rag_answer=result["rag_answer"],
        web_result=result["web_result"],
        active_document=result.get("active_document", active_document),
        personalization=result.get("personalization", profile.get("personalization", "")),
    )