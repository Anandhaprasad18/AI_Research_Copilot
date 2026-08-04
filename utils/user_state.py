import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def get_user_profile(username: str) -> Dict[str, Any]:
    profile_path = _profile_path(username)
    if not profile_path.exists():
        profile = {
            "username": username,
            "password": "admin",
            "personalization": (
                f"{username} prefers concise, well-structured answers and likes clear bullet points."
            ),
            "active_document": "",
        }
        save_user_profile(username, profile)
        return profile

    with profile_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_user_profile(username: str, profile: Dict[str, Any]) -> None:
    profile_path = _profile_path(username)
    with profile_path.open("w", encoding="utf-8") as handle:
        json.dump(profile, handle, indent=2)


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
    documents_dir = _documents_dir(username)
    return sorted([path.name for path in documents_dir.glob("*.pdf")])


def add_user_document(username: str, filename: str, file_bytes: bytes) -> str:
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported")

    documents_dir = _documents_dir(username)
    safe_name = filename.replace(" ", "_")
    target_path = documents_dir / safe_name
    target_path.write_bytes(file_bytes)
    return safe_name


def set_active_document(username: str, document_name: str) -> str:
    profile = get_user_profile(username)
    profile["active_document"] = document_name
    save_user_profile(username, profile)
    return document_name


def get_active_document(username: str) -> Optional[str]:
    profile = get_user_profile(username)
    active_document = profile.get("active_document", "")
    if active_document:
        return active_document

    documents = list_user_documents(username)
    if documents:
        return documents[0]
    return None


def get_user_document_path(username: str, document_name: Optional[str] = None) -> Optional[str]:
    documents_dir = _documents_dir(username)
    if document_name:
        target = documents_dir / document_name
        if target.exists():
            return str(target)
        return None

    active_document = get_active_document(username)
    if active_document:
        target = documents_dir / active_document
        if target.exists():
            return str(target)
    return None


def get_user_document_folder(username: str) -> str:
    return str(_documents_dir(username))
