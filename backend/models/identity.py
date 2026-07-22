"""
SelfGPT — Identity Document Model

Every identity — built-in and custom — shares this schema.
The only difference is that custom identities have an owner_id.
Built-in identities are seed data rows, not code.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from beanie import Document, Indexed
from pydantic import BaseModel, Field


class IdentityCategory(str, Enum):
    FAMOUS_PERSONALITY = "famous_personality"
    FAMOUS_BOOK = "famous_book"
    FICTIONAL_CHARACTER = "fictional_character"
    HISTORICAL_FIGURE = "historical_figure"
    CARTOON_CHARACTER = "cartoon_character"
    CUSTOM = "custom"


class ResponseLength(str, Enum):
    CONCISE = "concise"
    BALANCED = "balanced"
    DETAILED = "detailed"


class EmojiUsage(str, Enum):
    NONE = "none"
    MINIMAL = "minimal"
    MODERATE = "moderate"
    FREQUENT = "frequent"


class ExampleExchange(BaseModel):
    """A single example conversation turn."""
    user: str
    assistant: str


class IdentityProfile(BaseModel):
    """
    Structured personality/style profile. This is what makes each identity
    unique — compiled into a system prompt, never hardcoded.
    """
    age: Optional[str] = None
    gender: Optional[str] = None
    profession: str = ""
    expertise: List[str] = Field(default_factory=list)
    background_story: str = ""
    personality_traits: dict = Field(
        default_factory=lambda: {
            "humor": 0.5,
            "empathy": 0.5,
            "strictness": 0.5,
            "creativity": 0.5,
            "confidence": 0.5,
        }
    )
    values: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    beliefs: List[str] = Field(default_factory=list)
    speaking_style: str = "conversational"
    tone: str = "friendly"
    response_length: ResponseLength = ResponseLength.BALANCED
    emoji_usage: EmojiUsage = EmojiUsage.MINIMAL
    reasoning_style: str = "logical"
    teaching_style: str = "socratic"
    languages: List[str] = Field(default_factory=lambda: ["English"])
    catchphrase: Optional[str] = None
    example_exchanges: List[ExampleExchange] = Field(default_factory=list)
    rules_restrictions: List[str] = Field(default_factory=list)
    domain_knowledge: List[str] = Field(default_factory=list)
    internet_access: bool = False


class ModelConfig(BaseModel):
    """Per-identity model preferences."""
    model_id: Optional[str] = None  # Falls back to global default
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 4096
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


class Identity(Document):
    """
    An AI identity / persona. Built-in identities and custom user identities
    share the same schema — the only difference is owner_id being set for
    custom ones.
    """

    slug: Indexed(str, unique=True)
    category: IdentityCategory
    name: str
    tagline: str = ""
    avatar_url: str = ""
    owner_id: Optional[str] = None  # None for built-in, user ObjectId string for custom

    profile: IdentityProfile = Field(default_factory=IdentityProfile)
    system_prompt_template: str = ""  # Jinja2 template
    system_prompt_version: int = 1
    model_config_override: ModelConfig = Field(default_factory=ModelConfig)

    lora_adapter_id: Optional[str] = None
    rag_enabled: bool = False
    memory_enabled: bool = True
    is_published: bool = True
    is_coming_soon: bool = False

    disclaimer: str = (
        "This is an AI simulation inspired by publicly available information. "
        "It is not affiliated with, endorsed by, or representative of the real "
        "person, work, or character."
    )

    usage_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "identities"
        use_state_management = True
