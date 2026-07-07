from __future__ import annotations

from typing import Dict, Optional
from pydantic import BaseModel, Field

from .enums import ViewportBreakpoint


class ResponsiveBreakpoint(BaseModel):
    breakpoint: ViewportBreakpoint
    max_width: Optional[int] = None

    model_config = {"extra": "forbid", "frozen": True}


class ResponsiveLayout(BaseModel):
    breakpoint: ViewportBreakpoint
    layout_overrides: Dict[str, object] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class ResponsiveConfiguration(BaseModel):
    breakpoints: Dict[str, ResponsiveBreakpoint] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class ScalingConfiguration(BaseModel):
    scaling_mode: Optional[str] = None
    max_scale: Optional[float] = None

    model_config = {"extra": "forbid", "frozen": True}


class ViewportConfiguration(BaseModel):
    default_width: int = 1024
    default_height: int = 768

    model_config = {"extra": "forbid", "frozen": True}
