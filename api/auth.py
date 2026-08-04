from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from utils.user_state import authenticate_user, get_user_profile

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    username: str
    personalization: str
    active_document: str = ""


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        profile = authenticate_user(request.username.strip(), request.password)
    except (PermissionError, ValueError) as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    return LoginResponse(
        username=profile.get("username", request.username.strip()),
        personalization=profile.get("personalization", ""),
        active_document=profile.get("active_document", ""),
    )