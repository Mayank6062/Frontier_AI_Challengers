from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel


class SessionCreateRequest(BaseModel):
    user_id: str
    ttl_seconds: Optional[int] = None
    data: Optional[dict[str, Any]] = None


class SessionResponse(BaseModel):
    id: str
    user_id: str
    created_at: Optional[str]
    last_accessed: Optional[str]
    expires_at: Optional[str]
    data: Optional[dict[str, Any]]
    model_config = {"from_attributes": True}
