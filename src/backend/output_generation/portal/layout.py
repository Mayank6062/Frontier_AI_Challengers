from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class TopBar(BaseModel):
    title: Optional[str] = None
    logo_svg: Optional[str] = None
    persona_selector: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class LeftRail(BaseModel):
    collapsed: bool = False
    width_px: int = 240

    model_config = {"extra": "forbid", "frozen": True}


class Inspector(BaseModel):
    width_px: int = 320
    resizable: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class MainCanvas(BaseModel):
    view: Optional[str] = None
    full_width: bool = False

    model_config = {"extra": "forbid", "frozen": True}


class MiniMap(BaseModel):
    visible: bool = True
    scale: float = 0.1

    model_config = {"extra": "forbid", "frozen": True}


class LayoutModel(BaseModel):
    topbar: TopBar
    leftrail: LeftRail
    inspector: Inspector
    main: MainCanvas
    minimap: MiniMap

    model_config = {"extra": "forbid", "frozen": True}
