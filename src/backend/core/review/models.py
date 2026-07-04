from __future__ import annotations

from typing import List, Optional, Any
from enum import Enum

from backend.shared.models.base_model import BaseModel
from backend.shared.models.identifiers import generate_uuid4
from backend.shared.models.timestamps import now_iso


class ApprovalDecision(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"


class ApprovalRecord(BaseModel):
    reviewer_id: str
    decision: ApprovalDecision
    reason: Optional[str] = None
    timestamp: Optional[str] = None

    def __init__(self, **data: Any) -> None:
        if "timestamp" not in data or data.get("timestamp") is None:
            data["timestamp"] = now_iso()
        super().__init__(**data)


class Review(BaseModel):
    id: Optional[str] = None
    target_engagement_id: str
    created_at: Optional[str] = None
    approvals: List[ApprovalRecord]
    closed: bool = False

    def __init__(self, **data: Any) -> None:
        if "id" not in data or data.get("id") is None:
            data["id"] = generate_uuid4()
        if "created_at" not in data or data.get("created_at") is None:
            data["created_at"] = now_iso()
        if "approvals" not in data or data.get("approvals") is None:
            data["approvals"] = []
        super().__init__(**data)
