from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel

from .models import QualityBundle, QualityResult


class QualityGenerationRequest(BaseModel):
    engagement_id: str
    bundle: QualityBundle
    trace_id: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class QualityGenerationResponse(BaseModel):
    request_id: str
    result: QualityResult

    model_config = {"extra": "forbid", "frozen": True}


class QualityContext(BaseModel):
    trace_id: Optional[str]
    user_id: Optional[str]
    flags: Optional[Dict[str, bool]]

    model_config = {"extra": "forbid", "frozen": True}


class QualityExecutionMetadata(BaseModel):
    started_at: Optional[str]
    ended_at: Optional[str]
    executor_version: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class ValidatorResult(BaseModel):
    name: str
    verdict: str
    issues_found: int

    model_config = {"extra": "forbid", "frozen": True}


class ValidationSummary(BaseModel):
    total_validators: int
    passed: int
    failed: int

    model_config = {"extra": "forbid", "frozen": True}
