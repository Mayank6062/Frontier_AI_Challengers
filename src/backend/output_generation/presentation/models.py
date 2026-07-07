from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional, Sequence
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .enums import (
    PresentationFormat,
    SlideType,
    LayoutVariant,
    TransitionType,
)


class PresentationReference(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationAsset(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    uri: Optional[str]
    description: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class MediaReference(BaseModel):
    asset: PresentationAsset
    caption: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class SpeakerNotes(BaseModel):
    text: Optional[str]
    time_hint_seconds: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class AccessibilitySpec(BaseModel):
    alt_text_required: bool = True
    min_contrast_ratio: Optional[float]

    model_config = {"extra": "forbid", "frozen": True}


class SlideContent(BaseModel):
    heading: Optional[str]
    paragraphs: Sequence[str] = ()
    media: Sequence[MediaReference] = ()

    model_config = {"extra": "forbid", "frozen": True}


class Slide(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    type: SlideType
    layout: LayoutVariant
    content: SlideContent
    notes: Optional[SpeakerNotes]
    transition: Optional[TransitionType]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationSection(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: Optional[str]
    slides: Sequence[Slide] = ()

    model_config = {"extra": "forbid", "frozen": True}


class PresentationSequence(BaseModel):
    sections: Sequence[PresentationSection] = ()
    order: Sequence[UUID] = ()

    model_config = {"extra": "forbid", "frozen": True}


class PresentationTheme(BaseModel):
    name: Optional[str]
    colors: Optional[Dict[str, str]]
    fonts: Optional[Dict[str, str]]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationTemplate(BaseModel):
    id: Optional[str]
    name: Optional[str]
    theme: Optional[PresentationTheme]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationMetadata(BaseModel):
    created_at: datetime
    created_by: Optional[str]
    version: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationStatistics(BaseModel):
    slide_count: int
    asset_count: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationSummary(BaseModel):
    reference: PresentationReference
    metadata: Optional[PresentationMetadata]
    statistics: Optional[PresentationStatistics]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationArtifact(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    path: Optional[str]
    format: Optional[PresentationFormat]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationBundle(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    artifacts: Sequence[PresentationArtifact] = ()

    model_config = {"extra": "forbid", "frozen": True}


class PresentationResult(BaseModel):
    artifacts: Sequence[PresentationArtifact] = ()
    warnings: Sequence[str] = ()
    failures: Sequence[str] = ()

    model_config = {"extra": "forbid", "frozen": True}


class PresentationProvenance(BaseModel):
    generated_by: Optional[str]
    generated_at: Optional[datetime]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationVersion(BaseModel):
    major: int
    minor: int
    patch: int

    model_config = {"extra": "forbid", "frozen": True}
