"""
SelfGPT — Model: Memory

Stores extracted facts about the user or the identity's state.
"""

from datetime import datetime
from pydantic import Field
from beanie import Document
from typing import Optional

class Memory(Document):
    user_id: str
    identity_id: Optional[str] = None  # None = global memory across all identities
    chat_id: Optional[str] = None
    
    # The actual extracted fact, e.g., "User is learning React."
    content: str
    
    # "user_preference", "user_fact", "identity_state", "relationship"
    memory_type: str = "user_fact" 
    
    # How important is this memory (1-5)
    importance_score: int = 1
    
    is_active: bool = True
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "memories"
