"""
SelfGPT — Pydantic Schemas: Identity
"""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class IdentityProfileRequest(BaseModel):
    age: Optional[str] = None
    gender: Optional[str] = None
    profession: str = ""
    expertise: List[str] = Field(default_factory=list)
    background_story: str = ""
    personality_traits: Dict[str, float] = Field(
        default_factory=lambda: {
            "humor": 0.5, "empathy": 0.5, "strictness": 0.5,
            "creativity": 0.5, "confidence": 0.5,
        }
    )
    values: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    beliefs: List[str] = Field(default_factory=list)
    speaking_style: str = "conversational"
    tone: str = "friendly"
    response_length: str = "balanced"
    emoji_usage: str = "minimal"
    reasoning_style: str = "logical"
    teaching_style: str = "socratic"
    languages: List[str] = Field(default_factory=lambda: ["English"])
    catchphrase: Optional[str] = None
    example_exchanges: List[Dict[str, str]] = Field(default_factory=list)
    rules_restrictions: List[str] = Field(default_factory=list)
    domain_knowledge: List[str] = Field(default_factory=list)
    internet_access: bool = False


class CreateCustomIdentityRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    tagline: str = ""
    avatar_url: Optional[str] = None
    profile: IdentityProfileRequest = Field(default_factory=IdentityProfileRequest)
    memory_enabled: bool = True
    rag_enabled: bool = False


class UpdateCustomIdentityRequest(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    avatar_url: Optional[str] = None
    profile: Optional[IdentityProfileRequest] = None
    memory_enabled: Optional[bool] = None
    rag_enabled: Optional[bool] = None


class IdentityResponse(BaseModel):
    id: str
    slug: str
    category: str
    name: str
    tagline: str
    avatar_url: str
    is_published: bool
    is_coming_soon: bool
    disclaimer: str
    usage_count: int
    memory_enabled: bool
    rag_enabled: bool
    profile: Optional[Dict] = None  # Only included in detail views
    created_at: str

    class Config:
        from_attributes = True


class IdentityListResponse(BaseModel):
    identities: List[IdentityResponse]
    total: int
