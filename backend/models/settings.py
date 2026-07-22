"""
SelfGPT — User Settings Document Model
"""

from datetime import datetime, timezone
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class UserSettings(Document):
    """Per-user application settings."""

    user_id: Indexed(str, unique=True)
    theme: str = "system"  # light, dark, system
    default_model: Optional[str] = None
    voice_enabled: bool = False
    speech_rate: float = 1.0
    notification_prefs: dict = Field(default_factory=lambda: {
        "email": True,
        "push": False,
    })
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "settings"
        use_state_management = True
