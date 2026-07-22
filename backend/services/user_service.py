"""
SelfGPT — Service: User

Handles user profile updates, settings, and account management.
"""

from typing import Optional
from fastapi import HTTPException, status
from models.user import User, UserSettings


class UserService:
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Fetch user by ID."""
        return await User.get(user_id)

    @staticmethod
    async def update_user(user: User, **kwargs) -> User:
        """Update user fields."""
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await user.save()
        return user

    @staticmethod
    async def get_settings(user_id: str) -> UserSettings:
        """Get or create user settings."""
        settings = await UserSettings.find_one(UserSettings.user_id == user_id)
        if not settings:
            settings = UserSettings(user_id=user_id)
            await settings.insert()
        return settings

    @staticmethod
    async def update_settings(user_id: str, **kwargs) -> UserSettings:
        """Update user settings."""
        settings = await UserService.get_settings(user_id)
        for key, value in kwargs.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        await settings.save()
        return settings
