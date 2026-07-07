from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class OverlapInformation(BaseModel):
    node_a: str
    node_b: str
    overlap_area: float

    model_config = {"extra": "forbid", "frozen": True}


class BoundingInformation(BaseModel):
    node_id: str
    bbox: Dict[str, float]

    model_config = {"extra": "forbid", "frozen": True}


class CollisionStatistics(BaseModel):
    overlaps_found: int = 0
    resolved: int = 0

    model_config = {"extra": "forbid", "frozen": True}


class CollisionResolution(BaseModel):
    strategy: str
    details: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}


class CollisionReport(BaseModel):
    overlaps: List[OverlapInformation] = Field(default_factory=list)
    bounding_info: List[BoundingInformation] = Field(default_factory=list)
    resolution: Optional[CollisionResolution] = None

    model_config = {"extra": "forbid", "frozen": True}


class CollisionResult(BaseModel):
    report: CollisionReport
    statistics: CollisionStatistics

    model_config = {"extra": "forbid", "frozen": True}
