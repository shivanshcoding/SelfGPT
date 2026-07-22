"""
SelfGPT — Router: Auth

Endpoints for email/password registration, login, token refresh, and Google OAuth.
"""

from fastapi import APIRouter, Depends, status, HTTPException

from schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse,
    RefreshRequest, UserResponse, GoogleAuthRequest,
)
from services.auth_service import AuthService
from core.security import decode_token, create_access_token, create_refresh_token
from core.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest):
    """Register a new user with email and password."""
    user, access_token, refresh_token = await AuthService.register(data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    """Login with email and password."""
    user, access_token, refresh_token = await AuthService.login(data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshRequest):
    """Refresh an expired access token."""
    payload = decode_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
        
    access_token = create_access_token(data={"sub": user_id})
    new_refresh_token = create_refresh_token(data={"sub": user_id})
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    """Logout — client side clears tokens."""
    return


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    """Get current authenticated user's profile."""
    return user


@router.post("/google", response_model=TokenResponse)
async def google_auth(data: GoogleAuthRequest):
    """Authenticate via Google OAuth ID token."""
    raise HTTPException(status_code=501, detail="Google OAuth not yet implemented")
