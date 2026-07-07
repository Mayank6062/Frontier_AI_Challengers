from __future__ import annotations

from typing import Dict, Optional, Sequence
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

from .models import NarrativeProvenanceReference


class NarrativeAgentMetadata(BaseModel):
    agent_id: str
    agent_version: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeGeneratorMetadata(BaseModel):
    generator_name: str
    generator_version: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeVersionMetadata(BaseModel):
    version: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    generator: Optional[NarrativeGeneratorMetadata] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeManifestEntry(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    version: NarrativeVersionMetadata
    provenance: Optional[NarrativeProvenanceReference] = None

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeManifest(BaseModel):
    manifest_id: UUID = Field(default_factory=uuid4)
    entries: Sequence[NarrativeManifestEntry] = Field(default_factory=list)
    metadata: Optional[Dict[str, object]] = None

    model_config = {"extra": "forbid", "frozen": True}
