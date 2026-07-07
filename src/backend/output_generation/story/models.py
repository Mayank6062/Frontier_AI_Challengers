from __future__ import annotations

from typing import Dict, List, Optional, Sequence
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

from .enums import (
    NarrativeDepth,
    NarrativeTone,
    NarrativeSectionType,
    NarrativeStatus,
    NarrativeConfidenceLevel,
)


class NarrativeMetadata(BaseModel):
    narrative_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    status: NarrativeStatus = NarrativeStatus.DRAFT

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeAgentInput(BaseModel):
    prompt: str
    context: Optional[Dict[str, object]] = None
    depth: NarrativeDepth = NarrativeDepth.SUMMARY
    tone: NarrativeTone = NarrativeTone.NEUTRAL

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeConfig(BaseModel):
    mode: Optional[str] = None
    max_sections: int = 10
    preferred_tone: NarrativeTone = NarrativeTone.NEUTRAL

    model_config = {"extra": "forbid", "frozen": True}


class CitationReference(BaseModel):
    source: str
    reference_id: Optional[str] = None
    excerpt: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughScriptReference(BaseModel):
    script_id: str
    description: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class DecisionNarrativeEntry(BaseModel):
    decision_id: str
    rationale: str
    citations: Sequence[CitationReference] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class AlternativeSummary(BaseModel):
    title: str
    summary: str

    model_config = {"extra": "forbid", "frozen": True}


class ComponentNarrativeEntry(BaseModel):
    component_id: str
    description: str
    impacts: Optional[List[str]] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeSection(BaseModel):
    section_id: UUID = Field(default_factory=uuid4)
    title: str
    type: NarrativeSectionType
    content: str
    citations: Sequence[CitationReference] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeSectionBundle(BaseModel):
    sections: Sequence[NarrativeSection] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeGenerationMetadata(BaseModel):
    generator_version: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    mode: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeStatistics(BaseModel):
    sections_generated: int = 0
    words: int = 0

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeConfidence(BaseModel):
    level: NarrativeConfidenceLevel
    score: Optional[float] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativePersonaVisibility(BaseModel):
    persona: str
    visible: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeAgentOutput(BaseModel):
    sections: NarrativeSectionBundle
    metadata: NarrativeGenerationMetadata
    statistics: NarrativeStatistics
    confidence: Optional[NarrativeConfidence] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeWarning(BaseModel):
    code: str
    message: str

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeFailure(BaseModel):
    code: str
    message: str
    severity: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeValidationSummary(BaseModel):
    status: str
    warnings: Sequence[NarrativeWarning] = Field(default_factory=list)
    failures: Sequence[NarrativeFailure] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeResult(BaseModel):
    metadata: NarrativeMetadata
    output: NarrativeAgentOutput
    validation: Optional[NarrativeValidationSummary] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeContext(BaseModel):
    context_id: Optional[str] = None
    payload: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeProvenanceReference(BaseModel):
    source: str
    timestamp: Optional[datetime] = None
    details: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeManifestReference(BaseModel):
    manifest_id: UUID
    version: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}
