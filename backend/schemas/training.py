"""
SelfGPT — Pydantic Schemas: Training Data Export
"""

from typing import Optional, List, Dict
from pydantic import BaseModel


class TrainingExportRequest(BaseModel):
    identity_id: Optional[str] = None
    format: str = "chatml"  # chatml, dpo_pair
    min_rating: Optional[int] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


class TrainingExportResponse(BaseModel):
    total_examples: int
    format: str
    download_url: str


class TrainingStatsResponse(BaseModel):
    total_examples: int
    by_identity: Dict[str, int]
    by_format: Dict[str, int]
    avg_quality_score: Optional[float]
