"""
SelfGPT — Pydantic Schemas: Chat
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class CreateChatRequest(BaseModel):
    identity_id: str
    title: Optional[str] = "New Chat"


class UpdateChatRequest(BaseModel):
    title: Optional[str] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    folder: Optional[str] = None


class ChatResponse(BaseModel):
    id: str
    user_id: str
    identity_id: str
    title: str
    is_pinned: bool
    is_archived: bool
    is_deleted: bool
    folder: Optional[str]
    message_count: int
    last_message_at: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ChatListResponse(BaseModel):
    chats: List[ChatResponse]
    total: int
