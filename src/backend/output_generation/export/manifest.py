from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .models import ExportArtifact, ExportMetadata, ExportStatistics


class ExportManifestEntry(BaseModel):
    artifact: ExportArtifact
    metadata: Optional[ExportMetadata]

    model_config = {"extra": "forbid", "frozen": True}


class ExportManifestMetadata(BaseModel):
    created_at: datetime
    created_by: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ExportManifest(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    entries: Sequence[ExportManifestEntry] = ()
    metadata: Optional[ExportManifestMetadata]
    statistics: Optional[ExportStatistics]

    model_config = {"extra": "forbid", "frozen": True}


class ExportArtifactManifest(BaseModel):
    artifact_id: UUID
    manifest_id: UUID

    model_config = {"extra": "forbid", "frozen": True}


class ExportBundleManifest(BaseModel):
    bundle_id: UUID
    manifests: Sequence[ExportManifest]

    model_config = {"extra": "forbid", "frozen": True}
