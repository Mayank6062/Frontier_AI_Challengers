from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional, Any, Dict


class TechnologyCandidate(BaseModel):
    id: str
    name: str
    maturity: float
    fit: float
    citation: Optional[str]


class TechnologyRecommendationOutput(BaseModel):
    scored: List[TechnologyCandidate]
    decision: Dict[str, Any]
