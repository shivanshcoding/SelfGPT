"""
SelfGPT — Router: Chats

CRUD endpoints for chat sessions.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from schemas.chat import (
    CreateChatRequest, UpdateChatRequest,
    ChatResponse, ChatListResponse,
)
from core.dependencies import get_current_user
from models.user import User
from services.chat_service import ChatService

router = APIRouter(prefix="/api/chats", tags=["Chats"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    data: CreateChatRequest,
    user: User = Depends(get_current_user),
):
    """Create a new chat with an identity."""
    return await ChatService.create_chat(user, data)


@router.get("/", response_model=ChatListResponse)
async def list_chats(
    user: User = Depends(get_current_user),
    folder: Optional[str] = Query(None),
    is_archived: bool = Query(False),
    is_deleted: bool = Query(False),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    """List user's chats with filtering and pagination."""
    chats, total = await ChatService.list_chats(
        user, folder, is_archived, is_deleted, search, skip, limit
    )
    return {"chats": chats, "total": total}


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: str,
    user: User = Depends(get_current_user),
):
    """Get a single chat by ID."""
    return await ChatService.get_chat(chat_id, user)


@router.patch("/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: str,
    data: UpdateChatRequest,
    user: User = Depends(get_current_user),
):
    """Update chat title, pin status, folder, or archive status."""
    return await ChatService.update_chat(chat_id, user, data)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: str,
    user: User = Depends(get_current_user),
):
    """Soft-delete a chat (move to trash)."""
    await ChatService.delete_chat(chat_id, user)
    return


@router.post("/{chat_id}/restore", response_model=ChatResponse)
async def restore_chat(
    chat_id: str,
    user: User = Depends(get_current_user),
):
    """Restore a soft-deleted chat from trash."""
    return await ChatService.restore_chat(chat_id, user)


@router.delete("/{chat_id}/permanent", status_code=status.HTTP_204_NO_CONTENT)
async def permanently_delete_chat(
    chat_id: str,
    user: User = Depends(get_current_user),
):
    """Permanently delete a chat and all its messages."""
    await ChatService.permanently_delete_chat(chat_id, user)
    return
