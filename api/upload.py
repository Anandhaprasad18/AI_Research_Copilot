from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from rag.chain import get_rag_chain, reset_rag_chain
from rag.vectordb import reset_vector_db
from utils.user_state import add_user_document, get_user_document_folder, get_user_profile, list_user_documents, set_active_document

router = APIRouter()


class SetActiveDocumentRequest(BaseModel):
    username: str
    document_name: str


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), username: str = Form(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    user_name = (username or "").strip() or "guest"
    file_bytes = await file.read()
    saved_name = add_user_document(user_name, file.filename, file_bytes)
    set_active_document(user_name, saved_name)

    reset_vector_db(user_name, saved_name)
    reset_rag_chain(user_name, saved_name)
    get_rag_chain(user_name, saved_name, force_rebuild=True)

    return {
        "status": "success",
        "message": f"{file.filename} uploaded and indexed successfully.",
        "active_document": saved_name,
    }


@router.get("/documents")
async def get_documents(username: str):
    user_name = (username or "").strip() or "guest"
    profile = get_user_profile(user_name)
    return {
        "username": user_name,
        "documents": list_user_documents(user_name),
        "active_document": profile.get("active_document", ""),
        "folder": get_user_document_folder(user_name),
    }


@router.post("/set-active-document")
async def set_active_document_endpoint(payload: SetActiveDocumentRequest):
    user_name = (payload.username or "").strip() or "guest"
    document_name = payload.document_name.strip()
    set_active_document(user_name, document_name)
    reset_vector_db(user_name, document_name)
    reset_rag_chain(user_name, document_name)
    get_rag_chain(user_name, document_name, force_rebuild=True)
    return {"status": "success", "active_document": document_name}