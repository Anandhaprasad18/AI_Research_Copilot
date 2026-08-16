import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils.supabase_client import get_supabase_client

BASE_DIR = Path("data")
USERS_DIR = BASE_DIR / "users"
PDFS_DIR = BASE_DIR / "pdfs"


def ensure_storage() -> None:
    USERS_DIR.mkdir(parents=True, exist_ok=True)
    PDFS_DIR.mkdir(parents=True, exist_ok=True)


def _user_dir(username: str) -> Path:
    ensure_storage()
    user_dir = USERS_DIR / username
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir


def _documents_dir(username: str) -> Path:
    user_dir = _user_dir(username)
    documents_dir = user_dir / "documents"
    documents_dir.mkdir(parents=True, exist_ok=True)
    return documents_dir


def _profile_path(username: str) -> Path:
    return _user_dir(username) / "profile.json"


def _safe_filename(filename: str) -> str:
    cleaned = (filename or "document.pdf").strip()
    cleaned = cleaned.replace(" ", "_")
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", cleaned)
    if not cleaned.lower().endswith(".pdf"):
        cleaned = f"{cleaned}.pdf"
    return cleaned or "document.pdf"


def _default_profile(username: str) -> Dict[str, Any]:
    return {
        "username": username,
        "password": "admin",
        "personalization": (
            f"{username} prefers concise, well-structured answers and likes clear bullet points."
        ),
        "active_document": "",
    }


def _read_local_profile(username: str) -> Optional[Dict[str, Any]]:
    profile_path = _profile_path(username)
    if not profile_path.exists():
        return None
    try:
        with profile_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return None


def _write_local_profile(username: str, profile: Dict[str, Any]) -> None:
    profile_path = _profile_path(username)
    with profile_path.open("w", encoding="utf-8") as handle:
        json.dump(profile, handle, indent=2)


def _sync_profile_to_supabase(username: str, profile: Dict[str, Any]) -> None:
    client = get_supabase_client()
    if client is None:
        return
    payload = {
        "username": username,
        "personalization": profile.get("personalization", ""),
        "active_document": profile.get("active_document", ""),
    }
    try:
        client.table("profiles").upsert(payload, on_conflict="username").execute()
    except Exception:
        pass


def _fetch_profile_from_supabase(username: str) -> Optional[Dict[str, Any]]:
    client = get_supabase_client()
    if client is None:
        return None
    try:
        response = client.table("profiles").select("*").eq("username", username).maybe_single().execute()
        data = getattr(response, "data", None) or {}
        if not data:
            return None
        profile = {
            "username": username,
            "password": "admin",
            "personalization": data.get("personalization", ""),
            "active_document": data.get("active_document", ""),
        }
        return profile
    except Exception:
        return None


def get_user_profile(username: str) -> Dict[str, Any]:
    username = (username or "").strip() or "guest"

    profile = _fetch_profile_from_supabase(username)
    if profile is not None:
        _write_local_profile(username, profile)
        return profile

    profile = _read_local_profile(username) or _default_profile(username)
    if not _read_local_profile(username):
        _write_local_profile(username, profile)

    _sync_profile_to_supabase(username, profile)
    return profile


def save_user_profile(username: str, profile: Dict[str, Any]) -> None:
    username = (username or "").strip() or "guest"
    _write_local_profile(username, profile)
    _sync_profile_to_supabase(username, profile)


def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    if not username or not password:
        raise ValueError("Username and password are required")
    if password != "admin":
        raise PermissionError("Only the admin password is accepted for new accounts")

    profile = get_user_profile(username)
    profile.setdefault("username", username)
    save_user_profile(username, profile)
    return profile


def list_user_documents(username: str) -> List[str]:
    username = (username or "").strip() or "guest"

    client = get_supabase_client()
    if client is not None:
        try:
            response = client.table("documents").select("file_name").eq("username", username).execute()
            rows = getattr(response, "data", None) or []
            docs = [row.get("file_name", "") for row in rows if row.get("file_name")]
            if docs:
                return sorted(set(docs))
        except Exception:
            pass

    documents_dir = _documents_dir(username)
    return sorted([path.name for path in documents_dir.glob("*.pdf")])


def _upload_pdf_to_supabase(username: str, safe_name: str, file_bytes: bytes) -> None:
    client = get_supabase_client()
    if client is None:
        return

    storage_path = f"{username}/{safe_name}"
    try:
        client.storage.from_("documents").upload(storage_path, file_bytes, {"contentType": "application/pdf", "upsert": True})
    except Exception:
        try:
            client.storage.from_("documents").update(storage_path, file_bytes, {"contentType": "application/pdf"})
        except Exception:
            pass

    try:
        existing = client.table("documents").select("id").eq("username", username).eq("file_name", safe_name).maybe_single().execute()
        doc_data = getattr(existing, "data", None) or {}
        payload = {
            "username": username,
            "file_name": safe_name,
            "storage_path": storage_path,
        }
        if doc_data and doc_data.get("id"):
            client.table("documents").update(payload).eq("id", doc_data["id"]).execute()
        else:
            client.table("documents").insert(payload).execute()
    except Exception:
        pass


def add_user_document(username: str, filename: str, file_bytes: bytes) -> str:
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported")

    username = (username or "").strip() or "guest"
    safe_name = _safe_filename(filename)

    documents_dir = _documents_dir(username)
    target_path = documents_dir / safe_name
    target_path.write_bytes(file_bytes)

    _upload_pdf_to_supabase(username, safe_name, file_bytes)
    return safe_name


def set_active_document(username: str, document_name: str) -> str:
    username = (username or "").strip() or "guest"
    profile = get_user_profile(username)
    profile["active_document"] = document_name
    save_user_profile(username, profile)
    return document_name


def get_active_document(username: str) -> Optional[str]:
    username = (username or "").strip() or "guest"
    profile = get_user_profile(username)
    active_document = profile.get("active_document", "")
    if active_document:
        return active_document

    documents = list_user_documents(username)
    if documents:
        return documents[0]
    return None


def get_user_document_path(username: str, document_name: Optional[str] = None) -> Optional[str]:
    username = (username or "").strip() or "guest"
    documents_dir = _documents_dir(username)
    if document_name:
        target = documents_dir / document_name
        if target.exists():
            return str(target)
        # Optional fallback: if the file is not on disk yet, try to download it from Supabase.
        client = get_supabase_client()
        if client is not None:
            storage_path = f"{username}/{document_name}"
            try:
                file_bytes = client.storage.from_("documents").download(storage_path)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(file_bytes)
                return str(target)
            except Exception:
                pass
        return None

    active_document = get_active_document(username)
    if active_document:
        return get_user_document_path(username, active_document)
    return None


def get_user_document_folder(username: str) -> str:
    return str(_documents_dir((username or "").strip() or "guest"))
