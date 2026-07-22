"""
SelfGPT — Pydantic Schemas: Memory
"""

from typing import Optional, List
from pydantic import BaseModel


class MemoryResponse(BaseModel):
    id: str
    user_id: str
    identity_id: Optional[str]
    scope: str
    key: str
    value: str
    confidence: float
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True


class UpdateMemoryRequest(BaseModel):
    value: Optional[str] = None
    is_active: Optional[bool] = None


class MemoryListResponse(BaseModel):
    memories: List[MemoryResponse]
    total: int
