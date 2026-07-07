from __future__ import annotations

from typing import Dict, Optional
from pydantic import BaseModel, Field


class ARIA(BaseModel):
    role: Optional[str] = None
    label: Optional[str] = None
    describedby: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class KeyboardMap(BaseModel):
    shortcuts: Dict[str, str] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class FocusModel(BaseModel):
    initial_focus: Optional[str] = None
    trap_modals: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class SkipLink(BaseModel):
    href: str
    text: str

    model_config = {"extra": "forbid", "frozen": True}


class AccessibilitySettings(BaseModel):
    aria_defaults: ARIA = Field(default_factory=ARIA)
    keyboard_map: KeyboardMap = Field(default_factory=KeyboardMap)
    focus: FocusModel = Field(default_factory=FocusModel)
    skip_links: Optional[Dict[str, SkipLink]] = None

    model_config = {"extra": "forbid", "frozen": True}
