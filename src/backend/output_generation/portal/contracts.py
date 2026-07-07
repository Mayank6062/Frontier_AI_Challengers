"""Contracts (data-only) for portal generation and runtime metadata.

Immutable Pydantic models only. No implementations.
"""

from __future__ import annotations

from typing import Sequence, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class PortalRequest(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    path: str
    user_id: str

    model_config = {"extra": "forbid", "frozen": True}


class PortalResponse(BaseModel):
    request_id: UUID
    status: str
    payload: Dict[str, object]

    model_config = {"extra": "forbid", "frozen": True}


class PortalContext(BaseModel):
    session_id: str
    persona: str
    metadata: Dict[str, object] = Field(default_factory=dict)

    model_config = {"extra": "forbid", "frozen": True}


class PortalGenerationSummary(BaseModel):
    generated_at: str
    duration_seconds: float
    warnings: Sequence[str] = Field(default_factory=list)

    model_config = {"extra": "forbid", "frozen": True}


class PortalMetrics(BaseModel):
    render_time_ms: int
    index_size: int

    model_config = {"extra": "forbid", "frozen": True}


class PortalWarning(BaseModel):
    code: str
    message: str

    model_config = {"extra": "forbid", "frozen": True}


class PortalFailure(BaseModel):
    code: str
    message: str

    model_config = {"extra": "forbid", "frozen": True}


class PortalStatistics(BaseModel):
    active_users: int
    open_views: int

    model_config = {"extra": "forbid", "frozen": True}


class PortalGenerationOptions(BaseModel):
    include_toc: bool = False
    include_index: bool = True

    model_config = {"extra": "forbid", "frozen": True}
