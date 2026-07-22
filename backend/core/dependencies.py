"""
SelfGPT — Core: FastAPI Dependencies

Dependency injection factories used across routers.
"""

from fastapi import Depends, Header
from typing import Optional

from core.security import decode_token
from core.exceptions import UnauthorizedError, ForbiddenError
from models.user import User


async def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """
    Extract and validate JWT from Authorization header.
    Returns the User document or raises 401.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid Authorization header")

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    if payload is None:
        raise UnauthorizedError("Invalid or expired token")

    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")

    user = await User.get(user_id)
    if user is None or not user.is_active:
        raise UnauthorizedError("User not found or deactivated")

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Require the current user to be an admin."""
    if current_user.role != "admin":
        raise ForbiddenError("Admin access required")
    return current_user


async def get_optional_user(
    authorization: Optional[str] = Header(None),
) -> Optional[User]:
    """
    Like get_current_user but returns None instead of raising
    if no token is provided. Useful for public endpoints.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ")[1]
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    user = await User.get(user_id)
    if user and user.is_active:
        return user
    return None
