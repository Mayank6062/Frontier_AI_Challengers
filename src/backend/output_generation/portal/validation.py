"""Validation models for Portal package.

Only Pydantic immutable models are defined here.
"""

from __future__ import annotations

from typing import Sequence, Dict
from pydantic import BaseModel, Field


class PortalValidationIssue(BaseModel):
    code: str
    message: str
    field: str | None = None

    model_config = {"extra": "forbid", "frozen": True}


class PortalValidationResult(BaseModel):
    is_valid: bool
    errors: Sequence[PortalValidationIssue] = Field(default_factory=list)
    warnings: Sequence[PortalValidationIssue] = Field(default_factory=list)
    metadata: Dict[str, object] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}
