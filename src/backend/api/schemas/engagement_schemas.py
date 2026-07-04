from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class EngagementCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None


class EngagementUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class EngagementResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    state: str
    created_at: Optional[str]
    updated_at: Optional[str]
    model_config = {"from_attributes": True}
