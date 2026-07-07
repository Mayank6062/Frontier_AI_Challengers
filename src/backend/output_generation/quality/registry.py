from __future__ import annotations

from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class QualityRegistryEntry(BaseModel):
    id: Optional[UUID]
    name: str
    description: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class QualityValidatorRegistry(BaseModel):
    validators: Dict[str, QualityRegistryEntry] = {}

    model_config = {"extra": "forbid", "frozen": True}


class QualityReportRegistry(BaseModel):
    reports: Dict[str, QualityRegistryEntry] = {}

    model_config = {"extra": "forbid", "frozen": True}


class QualityArtifactRegistry(BaseModel):
    artifacts: Dict[str, QualityRegistryEntry] = {}

    model_config = {"extra": "forbid", "frozen": True}


class QualityMetricsRegistry(BaseModel):
    metrics: Dict[str, QualityRegistryEntry] = {}

    model_config = {"extra": "forbid", "frozen": True}
