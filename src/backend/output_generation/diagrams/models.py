"""Diagram data models (moved from legacy diagram.models).

These Pydantic models represent the canonical diagram definition and
related artifacts used by the diagrams layer.
"""

from __future__ import annotations

from typing import List, Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field


class DiagramNode(BaseModel):
    node_id: str
    label: str
    metadata: Dict[str, str] = Field(default_factory=dict)


class DiagramEdge(BaseModel):
    source: str
    target: str
    label: Optional[str] = None


class DiagramCluster(BaseModel):
    cluster_id: str
    nodes: List[str] = Field(default_factory=list)


class DiagramLegend(BaseModel):
    entries: Dict[str, str] = Field(default_factory=dict)


class DiagramMetadata(BaseModel):
    diagram_id: UUID = Field(default_factory=uuid4)
    title: Optional[str] = None
    description: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class LayoutHints(BaseModel):
    orientation: Optional[str] = None
    padding: Optional[int] = None


class AccessibilitySpec(BaseModel):
    alt_text: Optional[str] = None
    long_description: Optional[str] = None


class DiagramDefinition(BaseModel):
    diagram_id: UUID = Field(default_factory=uuid4)
    diagram_type: str
    nodes: List[DiagramNode] = Field(default_factory=list)
    edges: List[DiagramEdge] = Field(default_factory=list)
    clusters: List[DiagramCluster] = Field(default_factory=list)
    legend: Optional[DiagramLegend] = None
    metadata: Optional[DiagramMetadata] = None
    layout: Optional[LayoutHints] = None
    accessibility: Optional[AccessibilitySpec] = None


__all__ = [
    "DiagramDefinition",
    "DiagramNode",
    "DiagramEdge",
    "DiagramCluster",
    "DiagramLegend",
    "DiagramMetadata",
    "LayoutHints",
    "AccessibilitySpec",
]
