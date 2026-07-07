from __future__ import annotations

from pydantic import BaseModel


class PrintSettings(BaseModel):
    page_size: str = "A4"
    margins_mm: int = 20

    model_config = {"extra": "forbid", "frozen": True}


class PrintLayout(BaseModel):
    fit_to_page: bool = True
    include_legend: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class ScreenshotSettings(BaseModel):
    retina_scale: int = 2
    include_legend: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class ExportResolution(BaseModel):
    dpi: int = 300

    model_config = {"extra": "forbid", "frozen": True}
