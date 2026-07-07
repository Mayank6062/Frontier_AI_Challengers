from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .enums import LayoutAlgorithm


class NodePosition(BaseModel):
    node_id: str
    x: float
    y: float

    model_config = {"extra": "forbid", "frozen": True}


class EdgeRoute(BaseModel):
    edge_id: str
    points: List[Dict[str, float]] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class ClusterLayout(BaseModel):
    cluster_id: str
    bbox: Optional[Dict[str, float]] = None

    model_config = {"extra": "forbid", "frozen": True}


class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

    model_config = {"extra": "forbid", "frozen": True}


class Viewport(BaseModel):
    width: int
    height: int
    scale: float = 1.0

    model_config = {"extra": "forbid", "frozen": True}


class LayoutConfiguration(BaseModel):
    algorithm: LayoutAlgorithm = LayoutAlgorithm.HIERARCHICAL
    parameters: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}


class LayoutMetadata(BaseModel):
    algorithm: LayoutAlgorithm
    computed_at: float

    model_config = {"extra": "forbid", "frozen": True}


class LayoutResult(BaseModel):
    positions: List[NodePosition] = Field(default_factory=list)
    routes: List[EdgeRoute] = Field(default_factory=list)
    clusters: List[ClusterLayout] = Field(default_factory=list)
    viewport: Optional[Viewport] = None
    metadata: Optional[LayoutMetadata] = None

    model_config = {"extra": "forbid", "frozen": True}


class HierarchicalLayoutConfig(BaseModel):
    rankdir: Optional[str] = None
    ranksep: Optional[int] = None
    nodesep: Optional[int] = None

    model_config = {"extra": "forbid", "frozen": True}


class ForceLayoutConfig(BaseModel):
    iterations: int = 300
    repulsion: Optional[float] = None

    model_config = {"extra": "forbid", "frozen": True}


class RadialLayoutConfig(BaseModel):
    ring_spacing: Optional[int] = None
    max_rings: Optional[int] = None

    model_config = {"extra": "forbid", "frozen": True}


class GridLayoutConfig(BaseModel):
    cell_width: Optional[int] = None
    cell_height: Optional[int] = None

    model_config = {"extra": "forbid", "frozen": True}


class PieLayoutConfig(BaseModel):
    inner_radius: Optional[int] = None
    outer_radius: Optional[int] = None

    model_config = {"extra": "forbid", "frozen": True}


class GanttLayoutConfig(BaseModel):
    time_unit: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}
