from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional


class Candidate(BaseModel):
    id: str
    pattern: str
    score: float
    cost_estimate: Optional[float] = Field(default=1000)


class PatternRecommendation(BaseModel):
    candidate_id: str
    pattern: str
    rationale: str
    confidence: float
    citation: str


class ArchitectureDesignOutput(BaseModel):
    candidates: List[Candidate]
    patterns: List[PatternRecommendation]
