from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .enums import RoutingAlgorithm


class RoutingConfiguration(BaseModel):
    algorithm: RoutingAlgorithm = RoutingAlgorithm.ORTHOGONAL
    parameters: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}


class OrthogonalRouting(BaseModel):
    orthogonal_gap: Optional[int] = None

    model_config = {"extra": "forbid", "frozen": True}


class BezierRouting(BaseModel):
    tension: Optional[float] = None

    model_config = {"extra": "forbid", "frozen": True}


class BundledRouting(BaseModel):
    bundle_tightness: Optional[float] = None

    model_config = {"extra": "forbid", "frozen": True}


class RoutingStatistics(BaseModel):
    routed_edges: int = 0
    skipped_edges: int = 0

    model_config = {"extra": "forbid", "frozen": True}


class RoutingWarning(BaseModel):
    code: str
    message: str

    model_config = {"extra": "forbid", "frozen": True}


class RoutingResult(BaseModel):
    routes: List[Dict[str, object]] = Field(default_factory=list)
    statistics: RoutingStatistics = Field(default_factory=RoutingStatistics)
    warnings: List[RoutingWarning] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}
