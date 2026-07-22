"""
SelfGPT — Router: Identities

Browse built-in identities and manage custom identities.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from schemas.identity import (
    CreateCustomIdentityRequest, UpdateCustomIdentityRequest,
    IdentityResponse, IdentityListResponse,
)
from core.dependencies import get_current_user, get_optional_user
from models.user import User

router = APIRouter(prefix="/api/identities", tags=["Identities"])


@router.get("/", response_model=IdentityListResponse)
async def list_identities(
    user: Optional[User] = Depends(get_optional_user),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    include_coming_soon: bool = Query(True),
):
    """List all published identities. Includes coming-soon placeholders."""
    pass


@router.get("/{slug}", response_model=IdentityResponse)
async def get_identity(
    slug: str,
    user: Optional[User] = Depends(get_optional_user),
):
    """Get a single identity by slug, including full profile."""
    pass


@router.post("/custom", response_model=IdentityResponse, status_code=status.HTTP_201_CREATED)
async def create_custom_identity(
    data: CreateCustomIdentityRequest,
    user: User = Depends(get_current_user),
):
    """Create the user's custom identity (one per user)."""
    pass


@router.patch("/custom", response_model=IdentityResponse)
async def update_custom_identity(
    data: UpdateCustomIdentityRequest,
    user: User = Depends(get_current_user),
):
    """Update the user's custom identity. Re-compiles system prompt."""
    pass


@router.get("/custom/mine", response_model=IdentityResponse)
async def get_my_custom_identity(
    user: User = Depends(get_current_user),
):
    """Get the current user's custom identity."""
    pass
