# api/upload.py
import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from rag.vectordb import reset_vector_db
from rag.chain import get_rag_chain, reset_rag_chain

router = APIRouter()

PDF_FOLDER = "data/pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join(PDF_FOLDER, file.filename)
    with open(file_path, "wb") as pdf:
        pdf.write(await file.read())

    # Clear old FAISS cache and rebuild FAISS + retriever + rag chain
    reset_vector_db()
    reset_rag_chain()
    r=get_rag_chain(force_rebuild=True)

    return {
        "status": "success",
        "message": f"{file.filename} uploaded and indexed successfully.",
    }