from __future__ import annotations

from typing import Dict, Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class AnimationToken(BaseModel):
    token_id: UUID = Field(default_factory=uuid4)
    element: str
    trigger: str
    duration_token: str
    easing_token: str
    reduced_motion_behavior: str

    model_config = {"extra": "forbid", "frozen": True}


class MotionCatalog(BaseModel):
    animations: List[AnimationToken] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class SpacingScale(BaseModel):
    space_0: str = "0px"
    space_1: str = "4px"
    space_2: str = "8px"
    space_3: str = "12px"
    space_4: str = "16px"
    space_5: str = "20px"
    space_6: str = "24px"
    space_8: str = "32px"
    space_10: str = "40px"
    space_12: str = "48px"
    space_16: str = "64px"

    model_config = {"extra": "forbid", "frozen": True}


class ThemeTokensV2(BaseModel):
    colors: Dict[str, str] = Field(default_factory=dict)
    fonts: Dict[str, str] = Field(default_factory=dict)
    spacing: SpacingScale = Field(default_factory=SpacingScale)
    animation: MotionCatalog = Field(default_factory=MotionCatalog)
    animation_tokens: Optional[Dict[str, str]] = None

    model_config = {"extra": "forbid", "frozen": True}
