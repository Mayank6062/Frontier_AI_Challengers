from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .enums import (
    ScoreGrade,
    ScoreHealthStatus,
    ScoreTrend,
    EvidenceStrength,
    ScoreSchemaVersion,
)


class ScoreEvidence(BaseModel):
    citation_ids: List[str] = Field(default_factory=list)
    reasoning: str
    strength: EvidenceStrength

    model_config = {"extra": "forbid", "frozen": True}


class ScoreDimension(BaseModel):
    dimension_id: str
    dimension_name: str
    category: str
    weight: float

    raw_score: Optional[float] = None
    normalized_score: Optional[float] = None
    confidence: Optional[float] = None

    grade: Optional[ScoreGrade] = None
    rationale: Optional[str] = None
    evidence: List[ScoreEvidence] = Field(default_factory=list)

    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

    trend: Optional[ScoreTrend] = None

    model_config = {"extra": "forbid", "frozen": True}


class ScoreCategory(BaseModel):
    category_id: str
    category_name: str
    dimensions: List[ScoreDimension] = Field(default_factory=list)
    category_score: Optional[float] = None
    category_weight: float = 0.0

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreMetadata(BaseModel):
    score_id: str = Field(default_factory=lambda: str(uuid4()))
    engagement_id: Optional[str]
    engagement_version: Optional[int]
    produced_by: Optional[str]
    produced_at: Optional[datetime]
    model_version: Optional[str]
    score_schema_version: ScoreSchemaVersion = ScoreSchemaVersion.V2

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScore(BaseModel):
    metadata: ArchitectureScoreMetadata

    composite_score: float
    composite_grade: ScoreGrade
    health_status: ScoreHealthStatus
    confidence: float

    categories: List[ScoreCategory] = Field(default_factory=list)
    all_dimensions: List[ScoreDimension] = Field(default_factory=list)

    top_strengths: List[str] = Field(default_factory=list)
    top_risks: List[str] = Field(default_factory=list)
    critical_improvements: List[str] = Field(default_factory=list)

    previous_composite: Optional[float] = None
    score_delta: Optional[float] = None
    trend_narrative: Optional[str] = None

    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreInput(BaseModel):
    engagement_id: str
    engagement_version: int

    candidate_architectures: List[dict[str, object]] = Field(default_factory=list)
    selected_architecture: dict[str, object]
    technology_selections: List[dict[str, object]] = Field(default_factory=list)

    security_assessment: Optional[dict[str, object]] = None
    cost_assessment: Optional[dict[str, object]] = None
    compliance_assessment: Optional[dict[str, object]] = None
    risk_register: List[dict[str, object]] = Field(default_factory=list)

    hld_sections: Dict[str, object] = Field(default_factory=dict)
    lld_sections: Dict[str, object] = Field(default_factory=dict)

    citation_index: Dict[str, dict[str, object]] = Field(default_factory=dict)

    previous_score: Optional[ArchitectureScore] = None

    domain: str
    scale: str
    team_size: int
    timeline_weeks: int

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreArtifact(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    path: Optional[str]
    description: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreBundle(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    artifacts: List[ArchitectureScoreArtifact] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreResult(BaseModel):
    score: ArchitectureScore
    bundle: Optional[ArchitectureScoreBundle]

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreGenerationRequest(BaseModel):
    engagement_id: str
    bundle: ArchitectureScoreBundle
    trace_id: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreGenerationResponse(BaseModel):
    request_id: str
    result: ArchitectureScoreResult

    model_config = {"extra": "forbid", "frozen": True}


class TrendAnalysis(BaseModel):
    previous: Optional[float]
    current: Optional[float]
    delta: Optional[float]
    narrative: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}
