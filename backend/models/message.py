"""
SelfGPT — Message Document Model

Every message carries enough metadata to be directly exported into ChatML
for fine-tuning.  This is the training-data contract from day one.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

from beanie import Document, Indexed
from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    AUDIO = "audio"
    MIXED = "mixed"


class DeliveryStatus(str, Enum):
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"


class Attachment(BaseModel):
    """File or media attachment on a message."""
    filename: str
    content_type: str
    file_size: int
    storage_path: str
    thumbnail_path: Optional[str] = None
    extracted_text: Optional[str] = None


class TokenUsage(BaseModel):
    """LLM token consumption for a single generation."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class Message(Document):
    """
    A single message in a chat conversation.

    Training-ready: every assistant message records the identity_id,
    system_prompt_version, model_id, and user feedback (rating/correction)
    so it can be exported directly into ChatML JSONL.
    """

    chat_id: Indexed(str)
    user_id: Indexed(str)
    identity_id: str
    role: MessageRole
    content: str = ""
    content_type: ContentType = ContentType.TEXT
    attachments: List[Attachment] = Field(default_factory=list)

    # Conversation branching
    parent_message_id: Optional[str] = None

    # Training metadata — snapshot what was used to generate this response
    system_prompt_version: int = 1
    system_prompt_snapshot: str = ""
    model_id: str = ""
    model_params: Dict = Field(default_factory=dict)
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    tool_calls: Optional[List[Dict]] = None

    # User feedback — used as training signal
    rating: Optional[int] = None  # 1-5
    reaction: Optional[str] = None  # thumbs_up, thumbs_down
    correction: Optional[str] = None  # User-provided correction text

    # Edit tracking
    is_edited: bool = False
    edit_history: List[str] = Field(default_factory=list)
    is_regenerated: bool = False

    # WhatsApp-style delivery status
    delivery_status: DeliveryStatus = DeliveryStatus.SENDING

    # Extensible metadata
    metadata: Dict = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "messages"
        use_state_management = True
