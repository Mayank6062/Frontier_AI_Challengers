from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class PresentationLimits(BaseModel):
    max_slides: Optional[int]
    max_assets: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationThemeSettings(BaseModel):
    default_theme: Optional[str]
    allow_custom_themes: bool = False

    model_config = {"extra": "forbid", "frozen": True}


class PresentationAccessibilitySettings(BaseModel):
    enforce_alt_text: bool = True
    min_contrast_ratio: Optional[float]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationExportSettings(BaseModel):
    include_notes_in_export: bool = False
    default_format: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationPerformanceSettings(BaseModel):
    max_workers: Optional[int]
    memory_limit_mb: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationValidationSettings(BaseModel):
    strict_mode: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class PresentationGenerationSettings(BaseModel):
    default_timeout_seconds: Optional[int]
    include_notes: bool = False

    model_config = {"extra": "forbid", "frozen": True}


class PresentationRuntimeSettings(BaseModel):
    dry_run: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class PresentationSettings(BaseModel):
    limits: Optional[PresentationLimits]
    theme: Optional[PresentationThemeSettings]
    accessibility: Optional[PresentationAccessibilitySettings]
    export: Optional[PresentationExportSettings]
    performance: Optional[PresentationPerformanceSettings]
    validation: Optional[PresentationValidationSettings]
    generation: Optional[PresentationGenerationSettings]
    runtime: Optional[PresentationRuntimeSettings]

    model_config = {"extra": "forbid", "frozen": True}
