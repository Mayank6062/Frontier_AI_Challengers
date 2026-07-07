from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .models import QualityArtifact


class QualityManifestEntry(BaseModel):
    artifact: QualityArtifact
    metadata: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}


class QualityManifestSummary(BaseModel):
    manifest_id: UUID
    created_at: datetime
    artifact_count: int

    model_config = {"extra": "forbid", "frozen": True}


class QualityManifestBuilderSpec(BaseModel):
    source: str
    include_patterns: List[str] = Field(default_factory=list)
    exclude_patterns: List[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class QualityManifestIndex(BaseModel):
    manifests: Dict[str, QualityManifestSummary] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class QualityManifestIntegrity(BaseModel):
    manifest_id: UUID
    checksum: Optional[str]
    verified_at: Optional[datetime]

    model_config = {"extra": "forbid", "frozen": True}
