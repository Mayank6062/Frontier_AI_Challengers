from __future__ import annotations

from typing import Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from .models import NarrativeManifestReference


class NarrativeRegistryEntry(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    manifest: NarrativeManifestReference

    model_config = {"extra": "forbid", "frozen": True}


class NarrativeRegistryIndex(BaseModel):
    entries: Dict[str, NarrativeRegistryEntry] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}
