"""
SelfGPT — Chat Document Model
"""

from datetime import datetime, timezone
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class Chat(Document):
    """A conversation session between a user and an identity."""

    user_id: Indexed(str)
    identity_id: Indexed(str)
    title: str = "New Chat"
    is_pinned: bool = False
    is_archived: bool = False
    is_deleted: bool = False
    folder: Optional[str] = None
    message_count: int = 0
    last_message_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "chats"
        use_state_management = True
