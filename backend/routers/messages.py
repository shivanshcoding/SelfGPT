"""
SelfGPT — Router: Messages

Message CRUD and feedback endpoints.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from schemas.message import (
    SendMessageRequest, MessageResponse,
    MessageFeedbackRequest, EditMessageRequest,
)
from core.dependencies import get_current_user
from models.user import User
from services.message_service import MessageService

router = APIRouter(prefix="/api/chats/{chat_id}/messages", tags=["Messages"])


@router.get("/", response_model=list[MessageResponse])
async def list_messages(
    chat_id: str,
    user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: Optional[str] = Query(None),
):
    """List messages in a chat with pagination and search."""
    return await MessageService.list_messages(chat_id, user, skip, limit, search)


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    chat_id: str,
    data: SendMessageRequest,
    user: User = Depends(get_current_user),
):
    """Send a message and get an AI response (non-streaming fallback)."""
    return await MessageService.send_message(chat_id, user, data)


@router.patch("/{message_id}/feedback", response_model=MessageResponse)
async def add_feedback(
    chat_id: str,
    message_id: str,
    data: MessageFeedbackRequest,
    user: User = Depends(get_current_user),
):
    """Add rating, reaction, or correction to a message."""
    return await MessageService.add_feedback(chat_id, message_id, user, data)


@router.patch("/{message_id}/edit", response_model=MessageResponse)
async def edit_message(
    chat_id: str,
    message_id: str,
    data: EditMessageRequest,
    user: User = Depends(get_current_user),
):
    """Edit a user message and regenerate the response (Not implemented yet)."""
    pass


@router.post("/{message_id}/regenerate", response_model=MessageResponse)
async def regenerate_message(
    chat_id: str,
    message_id: str,
    user: User = Depends(get_current_user),
):
    """Regenerate an AI response for a given message (Not implemented yet)."""
    pass
