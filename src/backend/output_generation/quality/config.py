from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel

from .settings import QualitySettings


class QualityConfiguration(BaseModel):
    name: str
    description: Optional[str]
    settings: QualitySettings

    model_config = {"extra": "forbid", "frozen": True}


class QualityGateConfiguration(BaseModel):
    gate_name: str
    thresholds: Optional[Dict[str, float]]

    model_config = {"extra": "forbid", "frozen": True}


class QualityValidatorConfiguration(BaseModel):
    validator_name: str
    enabled: bool = True
    config: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}
