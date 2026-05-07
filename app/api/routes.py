from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app import db

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


class UserCreate(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    name: str


@router.post("/users", response_model=UserOut, tags=["Users"])
def create_user(payload: UserCreate):
    try:
        user = db.create_user(payload.name)
        return user
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/users/{user_id}", response_model=UserOut, tags=["Users"])
def get_user(user_id: int):
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
