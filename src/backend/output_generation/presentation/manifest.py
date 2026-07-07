from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional, Sequence
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .models import PresentationArtifact, PresentationSummary, PresentationStatistics


class PresentationManifestEntry(BaseModel):
    artifact: PresentationArtifact
    metadata: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationManifestMetadata(BaseModel):
    created_at: datetime
    created_by: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationManifest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    entries: Sequence[PresentationManifestEntry] = ()
    summary: Optional[PresentationSummary]
    statistics: Optional[PresentationStatistics]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationManifestStatistics(BaseModel):
    total_artifacts: int
    total_size_bytes: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationManifestSummary(BaseModel):
    manifest_id: UUID
    created_at: datetime
    entries_count: int

    model_config = {"extra": "forbid", "frozen": True}


class PresentationManifestIntegrity(BaseModel):
    checksum: Optional[str]
    verified: Optional[bool]

    model_config = {"extra": "forbid", "frozen": True}
