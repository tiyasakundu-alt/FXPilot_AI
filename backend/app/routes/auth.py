
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, EmailStr

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

# Temporary in-memory storage
users = {}


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    email = str(request.email).lower()

    if email in users:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    users[email] = {
        "email": email,
        "hashed_password": hash_password(request.password),
    }

    return {
        "message": "User registered successfully",
        "email": email,
    }


@router.post("/login")
def login(request: LoginRequest):
    email = str(request.email).lower()
    user = users.get(email)

    if not user or not verify_password(
        request.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(subject=email)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
