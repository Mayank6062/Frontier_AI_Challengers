from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class ArchitectureScoreContext(BaseModel):
    trace_id: Optional[str]
    user_id: Optional[str]
    flags: Optional[dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}


class ArchitectureScoreExecutionMetadata(BaseModel):
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
