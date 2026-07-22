"""
SelfGPT — Router: Memory

Endpoints for retrieving and managing extracted memories.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from core.dependencies import get_current_user
from models.user import User
from models.memory import Memory
from services.memory_service import MemoryService

router = APIRouter(prefix="/api/memories", tags=["Memory"])


class MemoryResponse(BaseModel):
    id: str
    identity_id: Optional[str] = None
    content: str
    memory_type: str
    created_at: str

    @classmethod
    def from_mongo(cls, mem: Memory):
        return cls(
            id=str(mem.id),
            identity_id=mem.identity_id,
            content=mem.content,
            memory_type=mem.memory_type,
            created_at=mem.created_at.isoformat()
        )


@router.get("/", response_model=List[MemoryResponse])
async def list_memories(
    identity_id: Optional[str] = None,
    user: User = Depends(get_current_user),
):
    """List active memories for the user."""
    memories = await MemoryService.get_memories(user, identity_id)
    return [MemoryResponse.from_mongo(m) for m in memories]


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def forget_memory(
    memory_id: str,
    user: User = Depends(get_current_user),
):
    """Soft delete (forget) a memory."""
    success = await MemoryService.delete_memory(memory_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="Memory not found")
    return
