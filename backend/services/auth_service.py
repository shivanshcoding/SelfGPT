"""
SelfGPT — Service: Auth

Handles user registration, login, and token generation.
"""

from typing import Tuple
from fastapi import HTTPException, status
from models.user import User
from schemas.auth import RegisterRequest, LoginRequest
from core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token
)


class AuthService:
    @staticmethod
    async def register(data: RegisterRequest) -> Tuple[User, str, str]:
        """
        Register a new user.
        Returns: (user, access_token, refresh_token)
        """
        # Check if email or username exists
        existing_email = await User.find_one(User.email == data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        existing_username = await User.find_one(User.username == data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Create user
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
            auth_provider="email"
        )
        await user.insert()

        # Generate tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return user, access_token, refresh_token

    @staticmethod
    async def login(data: LoginRequest) -> Tuple[User, str, str]:
        """
        Authenticate user.
        Returns: (user, access_token, refresh_token)
        """
        user = await User.find_one(User.email == data.email)
        if not user or not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return user, access_token, refresh_token
