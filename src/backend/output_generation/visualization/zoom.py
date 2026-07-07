from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class ZoomLimits(BaseModel):
    min_scale: float = 0.25
    max_scale: float = 4.0

    model_config = {"extra": "forbid", "frozen": True}


class ViewBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

    model_config = {"extra": "forbid", "frozen": True}


class ZoomState(BaseModel):
    scale: float = 1.0
    center_x: Optional[float] = None
    center_y: Optional[float] = None

    model_config = {"extra": "forbid", "frozen": True}


class PanState(BaseModel):
    offset_x: float = 0.0
    offset_y: float = 0.0

    model_config = {"extra": "forbid", "frozen": True}


class ZoomConfiguration(BaseModel):
    mode: Optional[str] = None
    limits: ZoomLimits = Field(default_factory=ZoomLimits)

    model_config = {"extra": "forbid", "frozen": True}
