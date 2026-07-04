from __future__ import annotations

from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from backend.shared.models.base_model import BaseModel
from backend.shared.models.identifiers import generate_uuid4
from backend.shared.models.timestamps import now_iso


class Session(BaseModel):
    id: Optional[str] = None
    user_id: str
    created_at: Optional[str] = None
    last_accessed: Optional[str] = None
    expires_at: Optional[str] = None
    data: Dict[str, Any] = {}

    def __init__(self, **data: Any) -> None:
        if "id" not in data or data.get("id") is None:
            data["id"] = generate_uuid4()
        if "created_at" not in data or data.get("created_at") is None:
            data["created_at"] = now_iso()
        if "last_accessed" not in data or data.get("last_accessed") is None:
            data["last_accessed"] = data["created_at"]
        super().__init__(**data)

    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return datetime.fromisoformat(self.expires_at) <= datetime.utcnow()

    def touch(self, ttl_seconds: int | None = None) -> "Session":
        self_dict = self.to_dict()
        self_dict["last_accessed"] = now_iso()
        if ttl_seconds is not None:
            expiry = datetime.utcnow() + timedelta(seconds=ttl_seconds)
            self_dict["expires_at"] = expiry.isoformat()
        return Session.from_dict(self_dict)
