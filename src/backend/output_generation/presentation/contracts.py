from __future__ import annotations

from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel

from .models import (
    PresentationReference,
    PresentationResult,
    PresentationSummary,
)


class PresentationGenerationRequest(BaseModel):
    reference: PresentationReference
    template_id: Optional[str]
    options: Optional[Dict[str, object]]
    requester_id: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationGenerationResponse(BaseModel):
    request_id: UUID
    result: PresentationResult
    summary: Optional[PresentationSummary]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationGenerationContext(BaseModel):
    trace_id: Optional[str]
    user_id: Optional[str]
    flags: Optional[Dict[str, bool]]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationGenerationOptions(BaseModel):
    timeout_seconds: Optional[int]
    include_notes: Optional[bool]

    model_config = {"extra": "forbid", "frozen": True}


class PresentationGenerationStatus(BaseModel):
    status: str
    detail: Optional[Dict[str, object]]

    model_config = {"extra": "forbid", "frozen": True}
