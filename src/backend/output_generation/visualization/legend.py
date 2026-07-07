from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field

from .enums import LegendPosition


class LegendItem(BaseModel):
    key: str
    label: str
    description: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class LegendDefinition(BaseModel):
    items: List[LegendItem] = Field(default_factory=list)
    position: LegendPosition = LegendPosition.BOTTOM_RIGHT

    model_config = {"extra": "forbid", "frozen": True}


class LegendLayout(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None

    model_config = {"extra": "forbid", "frozen": True}


class LegendConfiguration(BaseModel):
    include_border: bool = True
    padding: int = 8

    model_config = {"extra": "forbid", "frozen": True}


class LegendMetadata(BaseModel):
    generated: bool = True

    model_config = {"extra": "forbid", "frozen": True}
