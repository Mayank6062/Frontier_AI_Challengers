from __future__ import annotations

from typing import Sequence, Dict
from pydantic import BaseModel, Field

from .models import NarrativeValidationSummary


class ValidationReport(BaseModel):
    summary: NarrativeValidationSummary
    raw_issues: Sequence[Dict[str, object]] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}
