"""Registry data models for Portal package.

Data-only models describing registry entries and references.
"""

from __future__ import annotations

from typing import Dict
from pydantic import BaseModel, Field


class PortalRegistryEntry(BaseModel):
    id: str
    name: str
    type: str
    metadata: Dict[str, object] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class PortalComponentReference(BaseModel):
    id: str
    display_name: str | None = None
    manifest_ref: str | None = None

    model_config = {"extra": "forbid", "frozen": True}
