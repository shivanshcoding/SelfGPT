"""
SelfGPT — User Document Model
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field


class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserPreferences(BaseModel):
    """User-configurable preferences."""
    theme: str = "system"
    language: str = "en"
    notifications_enabled: bool = True


class User(Document):
    """User account — supports email/password and Google OAuth."""

    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    hashed_password: Optional[str] = None  # None for OAuth-only users
    auth_provider: AuthProvider = AuthProvider.EMAIL
    avatar_url: Optional[str] = None
    role: UserRole = UserRole.USER
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
        use_state_management = True

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "shivansh",
                "auth_provider": "email",
                "role": "user",
            }
        }
