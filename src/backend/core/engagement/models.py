from __future__ import annotations

from typing import Optional, Any
from enum import Enum

from backend.shared.models.base_model import BaseModel
from backend.shared.models.identifiers import generate_uuid4
from backend.shared.models.timestamps import now_iso


class EngagementState(str, Enum):
    DRAFT = "draft"
    DESIGN = "design"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Engagement(BaseModel):
    """Domain model representing an Engagement.

    Immutable after creation to preserve auditability; updates return new
    model instances.
    """

    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    state: EngagementState = EngagementState.DRAFT
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __init__(self, **data: Any) -> None:
        if "id" not in data or data.get("id") is None:
            data["id"] = generate_uuid4()
        if "created_at" not in data or data.get("created_at") is None:
            data["created_at"] = now_iso()
        super().__init__(**data)

    def with_state(self, new_state: EngagementState) -> "Engagement":
        d = self.to_dict()
        d["state"] = new_state
        d["updated_at"] = now_iso()
        return self.from_dict(d)
