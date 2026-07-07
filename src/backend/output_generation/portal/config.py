"""Configuration models for the Portal package.

Simple contracts representing portal configuration options.
"""

from __future__ import annotations

from typing import Dict
from pydantic import BaseModel, Field


class PortalLimits(BaseModel):
    max_routes: int = 1000
    max_search_entries: int = 10000

    model_config = {"extra": "forbid", "frozen": True}


class PortalDefaults(BaseModel):
    theme: str = "light"
    locale: str = "en-US"

    model_config = {"extra": "forbid", "frozen": True}


class PortalConfiguration(BaseModel):
    defaults: PortalDefaults = Field(default_factory=PortalDefaults)
    limits: PortalLimits = Field(default_factory=PortalLimits)
    policies: Dict[str, object] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}
