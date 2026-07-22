"""
SelfGPT — Upload Document Model

Tracks file uploads attached to chat messages (images, PDFs, etc.)
separate from RAG documents.
"""

from datetime import datetime, timezone
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class Upload(Document):
    """A file uploaded in a chat conversation."""

    user_id: Indexed(str)
    chat_id: Optional[str] = None
    message_id: Optional[str] = None
    filename: str
    content_type: str
    file_size: int
    storage_path: str
    thumbnail_path: Optional[str] = None
    extracted_text: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "uploads"
        use_state_management = True
