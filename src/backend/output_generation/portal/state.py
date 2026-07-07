from __future__ import annotations

from typing import Dict, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field

from ..enums import PersonaType, ThemeType, DensityType


class PortalState(BaseModel):
    state_id: UUID = Field(default_factory=uuid4)
    current_route: str
    active_persona: PersonaType
    theme: ThemeType = ThemeType.LIGHT
    density: DensityType = DensityType.COMFORTABLE
    search_query: Optional[str] = None
    inspector_target: Optional[str] = None
    expanded_sections: Set[str] = Field(default_factory=set)
    diagram_zoom_levels: Dict[str, float] = Field(default_factory=dict)
    table_filters: Dict[str, Dict[str, object]] = Field(default_factory=dict)
    table_sorts: Dict[str, Dict[str, object]] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"extra": "forbid", "frozen": True}
