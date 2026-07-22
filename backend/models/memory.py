"""
SelfGPT — Memory Document Model

Three scopes: short_term (conversation), long_term (cross-chat), identity (per-identity).
Users can view, edit, and delete any memory — "forget" is a hard delete.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class MemoryScope(str, Enum):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    IDENTITY = "identity"


class Memory(Document):
    """A single remembered fact or preference."""

    user_id: Indexed(str)
    identity_id: Optional[str] = None  # None = global user memory
    scope: MemoryScope = MemoryScope.LONG_TERM
    key: str  # What was remembered (e.g., "user's favorite color")
    value: str  # The memory content (e.g., "blue")
    source_chat_id: Optional[str] = None
    source_message_id: Optional[str] = None
    confidence: float = 1.0
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None  # For short-term memories

    class Settings:
        name = "memories"
        use_state_management = True
