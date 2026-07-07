from __future__ import annotations

from typing import Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from ..enums import ThemeType, DensityType
from .tokens import ThemeTokensV2


class ThemeMetadata(BaseModel):
    theme_id: UUID = Field(default_factory=uuid4)
    name: str
    mode: ThemeType
    tokens: ThemeTokensV2

    model_config = {"extra": "forbid", "frozen": True}


class ThemeSettings(BaseModel):
    default_theme: ThemeType = ThemeType.LIGHT
    available_themes: Dict[str, ThemeMetadata] = Field(default_factory=dict)
    density_default: DensityType = DensityType.COMFORTABLE

    model_config = {"extra": "forbid", "frozen": True}
