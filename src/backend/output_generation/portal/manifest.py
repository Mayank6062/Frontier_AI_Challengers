"""Manifest models for the Portal package.

Contracts-only representations of portal manifests and entries.
"""

from __future__ import annotations

from typing import Sequence, Dict
from pydantic import BaseModel, Field


class PortalManifestEntry(BaseModel):
    id: str
    path: str
    title: str | None = None
    metadata: Dict[str, object] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class PortalManifest(BaseModel):
    name: str
    version: str
    entries: Sequence[PortalManifestEntry] = Field(default_factory=list)
    metadata: Dict[str, object] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}
