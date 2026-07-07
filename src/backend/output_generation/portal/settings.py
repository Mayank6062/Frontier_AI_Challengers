from __future__ import annotations

from typing import Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class PortalSettings(BaseModel):
    portal_id: UUID = Field(default_factory=uuid4)
    title: Optional[str] = None
    description: Optional[str] = None
    default_route: Optional[str] = None
    theme_settings: Optional[Dict[str, object]] = None
    accessibility: Optional[Dict[str, object]] = None
    search_enabled: bool = True
    command_palette_enabled: bool = True

    model_config = {"extra": "forbid", "frozen": True}
