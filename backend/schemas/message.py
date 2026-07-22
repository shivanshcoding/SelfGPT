"""
SelfGPT — Pydantic Schemas: Message
"""

from typing import Optional, List, Dict
from pydantic import BaseModel


class SendMessageRequest(BaseModel):
    content: str
    content_type: str = "text"
    parent_message_id: Optional[str] = None
    attachments: Optional[List[Dict]] = None


class MessageResponse(BaseModel):
    id: str
    chat_id: str
    user_id: str
    identity_id: str
    role: str
    content: str
    content_type: str
    attachments: List[Dict]
    parent_message_id: Optional[str]
    model_id: str
    rating: Optional[int]
    reaction: Optional[str]
    correction: Optional[str]
    is_edited: bool
    is_regenerated: bool
    delivery_status: str
    created_at: str

    class Config:
        from_attributes = True


class MessageFeedbackRequest(BaseModel):
    rating: Optional[int] = None  # 1-5
    reaction: Optional[str] = None  # thumbs_up, thumbs_down
    correction: Optional[str] = None


class EditMessageRequest(BaseModel):
    content: str
