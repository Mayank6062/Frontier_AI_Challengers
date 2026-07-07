from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel


class QualityLimits(BaseModel):
    max_bundle_size_mb: Optional[float]
    max_artifact_count: Optional[int]

    model_config = {"extra": "forbid", "frozen": True}


class QualityValidationSettings(BaseModel):
    run_completeness: bool = True
    run_semantic: bool = True
    run_citation: bool = True
    run_determinism: bool = True
    run_accessibility: bool = True
    run_security: bool = True
    run_performance: bool = True

    model_config = {"extra": "forbid", "frozen": True}


class QualityRuntimeSettings(BaseModel):
    parallel_validators: int = 1
    timeout_seconds: Optional[int]
    resource_limits: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class QualitySettings(BaseModel):
    limits: Optional[QualityLimits]
    validation: QualityValidationSettings
    runtime: QualityRuntimeSettings

    model_config = {"extra": "forbid", "frozen": True}
