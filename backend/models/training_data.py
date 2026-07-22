"""
SelfGPT — Training Data Document Model

Pre-formatted training examples ready for export to ChatML JSONL.
Supports standard SFT, DPO pairs, and ORPO format.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

from beanie import Document, Indexed
from pydantic import Field


class TrainingFormat(str, Enum):
    CHATML = "chatml"
    DPO_PAIR = "dpo_pair"
    ORPO = "orpo"


class TrainingData(Document):
    """
    A single training example, pre-formatted for export.
    Populated from high-quality message turns with user feedback.
    """

    identity_id: Indexed(str)
    source_message_ids: List[str] = Field(default_factory=list)
    format: TrainingFormat = TrainingFormat.CHATML

    # ChatML-ready conversation
    messages: List[Dict] = Field(default_factory=list)  # [{role, content}, ...]

    # DPO fields
    chosen: Optional[str] = None
    rejected: Optional[str] = None

    system_prompt_version: int = 1
    quality_score: Optional[float] = None  # LLM-judge score
    is_exported: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "training_data"
        use_state_management = True
