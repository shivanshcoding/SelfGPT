"""
SelfGPT — Feedback Document Model

Captures user feedback on AI responses — used as training signal.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class FeedbackType(str, Enum):
    RATING = "rating"
    REACTION = "reaction"
    CORRECTION = "correction"
    REPORT = "report"


class Feedback(Document):
    """User feedback on a specific message."""

    user_id: Indexed(str)
    message_id: Indexed(str)
    chat_id: str
    identity_id: str
    type: FeedbackType
    value: str  # "5" for rating, "thumbs_up" for reaction, correction text, etc.
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "feedback"
        use_state_management = True
