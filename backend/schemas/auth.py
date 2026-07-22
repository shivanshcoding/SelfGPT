"""
SelfGPT — Pydantic Schemas: Auth

Request/response schemas for authentication endpoints.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    auth_provider: str
    avatar_url: Optional[str] = None
    role: str
    created_at: str

    class Config:
        from_attributes = True


class GoogleAuthRequest(BaseModel):
    """Token received from Google OAuth on the frontend."""
    id_token: str
