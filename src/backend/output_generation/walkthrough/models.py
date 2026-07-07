from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Sequence
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ..story.models import (
    CitationReference as StoryCitationReference,
)  # reuse canonical
from ..models.persona import Persona as PersonaModel


class _PydanticConfig:
    model_config = {"extra": "forbid", "frozen": True}


class SpeakerNotes(BaseModel):
    text: str

    model_config = {"extra": "forbid", "frozen": True}


class OpeningStatement(BaseModel):
    title: Optional[str]
    text: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ClosingStatement(BaseModel):
    text: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class TransitionHint(BaseModel):
    hint: Optional[str]
    transition_type: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class TimelineReference(BaseModel):
    start: Optional[datetime]
    end: Optional[datetime]
    label: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


CitationReference = StoryCitationReference


class PersonaReference(PersonaModel):
    # alias the canonical Persona model for walkthrough usage
    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughFocusTarget(BaseModel):
    id: UUID
    type: str
    label: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughStep(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: Optional[str]
    body: Optional[str]
    focus: Optional[WalkthroughFocusTarget]
    notes: Optional[SpeakerNotes]
    citations: Optional[List[CitationReference]]
    duration_seconds: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughScript(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str]
    steps: Sequence[WalkthroughStep]
    mode: Optional[str]
    persona: Optional[PersonaReference]
    metadata: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughMetadata(BaseModel):
    created_at: datetime
    created_by: Optional[str]
    version: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughStatistics(BaseModel):
    total_steps: int
    estimated_duration_seconds: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughSummary(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    statistics: Optional[WalkthroughStatistics]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughReference(BaseModel):
    id: UUID
    title: Optional[str]
    manifest_ref: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughContext(BaseModel):
    snapshot_id: Optional[UUID]
    entities: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughGenerationRequest(BaseModel):
    script: WalkthroughScript
    context: Optional[WalkthroughContext]
    requester_id: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughWarning(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughFailure(BaseModel):
    code: str
    message: str
    severity: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughValidationSummary(BaseModel):
    status: str
    issues: Optional[Sequence[Dict[str, object]]]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughExecutionMetadata(BaseModel):
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    engine_version: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PlayerState(BaseModel):
    playback_state: Optional[str]
    position_seconds: Optional[float]

    model_config = {"extra": "forbid", "frozen": True}


class NavigationState(BaseModel):
    current_step_id: Optional[UUID]
    direction: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ProgressState(BaseModel):
    percent_complete: float

    model_config = {"extra": "forbid", "frozen": True}


class PlaybackOptions(BaseModel):
    speed: Optional[str]
    auto_advance: Optional[bool]
    auto_advance_mode: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class AutoAdvanceConfiguration(BaseModel):
    mode: Optional[str]
    timeout_seconds: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughPlaybackMetadata(BaseModel):
    player_state: Optional[PlayerState]
    navigation_state: Optional[NavigationState]
    progress: Optional[ProgressState]

    model_config = {"extra": "forbid", "frozen": True}


class WalkthroughGenerationResult(BaseModel):
    id: UUID
    summary: WalkthroughSummary
    warnings: Optional[List[WalkthroughWarning]]
    failures: Optional[List[WalkthroughFailure]]
    execution: Optional[WalkthroughExecutionMetadata]

    model_config = {"extra": "forbid", "frozen": True}


# WalkthroughManifest is owned by manifest.py (canonical manifest models).
# Retain other domain models in this module only.


class PortalEmbedMetadata(BaseModel):
    embed_path: Optional[str]
    height_px: Optional[int]
    width_px: Optional[int]
    allow_fullscreen: Optional[bool]

    model_config = {"extra": "forbid", "frozen": True}
