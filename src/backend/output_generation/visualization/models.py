from __future__ import annotations

from typing import List, Optional, Sequence
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field

from ..diagrams.models import DiagramDefinition
from .enums import RendererType, OutputTarget, RenderMode


class VisualizationMetadata(BaseModel):
    visualization_id: UUID = Field(default_factory=uuid4)
    engagement_id: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationStatistics(BaseModel):
    node_count: int = 0
    edge_count: int = 0
    cluster_count: int = 0

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationMetrics(BaseModel):
    elapsed_seconds: float = 0.0
    attempts: int = 0

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationWarning(BaseModel):
    code: str
    message: str

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationFailure(BaseModel):
    code: str
    message: str

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationSummary(BaseModel):
    success: bool = True
    warnings: List[VisualizationWarning] = Field(default_factory=list)
    failures: List[VisualizationFailure] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationRequest(BaseModel):
    definition: DiagramDefinition
    target: OutputTarget = OutputTarget.PORTAL
    preferred_renderer: Optional[RendererType] = None

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationResult(BaseModel):
    metadata: VisualizationMetadata
    statistics: VisualizationStatistics
    metrics: VisualizationMetrics
    summary: VisualizationSummary
    artifacts: Sequence[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationResponse(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    result: VisualizationResult

    model_config = {"extra": "forbid", "frozen": True}


class VisualizationDefinition(BaseModel):
    definition_id: UUID = Field(default_factory=uuid4)
    diagram: DiagramDefinition
    renderer: Optional[RendererType] = None
    mode: RenderMode = RenderMode.VECTOR
    metadata: VisualizationMetadata

    model_config = {"extra": "forbid", "frozen": True}
