from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional


class ArchitectureScoreManifestEntry(BaseModel):
    id: str
    name: str
    description: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreManifest(BaseModel):
    manifest_id: str
    version: str
    entries: List[ArchitectureScoreManifestEntry] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}
