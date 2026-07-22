"""
SelfGPT — Document Model (RAG knowledge base)
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class EmbeddingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"


class Document(Document):
    """A document uploaded to an identity's knowledge base for RAG."""

    identity_id: Indexed(str)
    user_id: str
    filename: str
    file_type: str
    file_size: int  # bytes
    storage_path: str
    chunk_count: int = 0
    embedding_status: EmbeddingStatus = EmbeddingStatus.PENDING
    version: int = 1
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "documents"
        use_state_management = True
