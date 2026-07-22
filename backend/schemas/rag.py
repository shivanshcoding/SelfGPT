"""
SelfGPT — Pydantic Schemas: RAG
"""

from typing import Optional, List
from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    id: str
    identity_id: str
    filename: str
    file_type: str
    file_size: int
    chunk_count: int
    embedding_status: str
    created_at: str

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    documents: List[DocumentUploadResponse]
    total: int
