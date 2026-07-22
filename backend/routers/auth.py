"""
SelfGPT — Router: Auth

Endpoints for email/password registration, login, token refresh, and Google OAuth.
"""

from fastapi import APIRouter, Depends, status

from schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse,
    RefreshRequest, UserResponse, GoogleAuthRequest,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest):
    """Register a new user with email and password."""
    # Phase 2 implementation
    pass


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    """Login with email and password."""
    pass


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshRequest):
    """Refresh an expired access token."""
    pass


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    """Logout — invalidate refresh token."""
    pass


@router.get("/me", response_model=UserResponse)
async def get_me():
    """Get current authenticated user's profile."""
    pass


@router.post("/google", response_model=TokenResponse)
async def google_auth(data: GoogleAuthRequest):
    """Authenticate via Google OAuth ID token."""
    pass
