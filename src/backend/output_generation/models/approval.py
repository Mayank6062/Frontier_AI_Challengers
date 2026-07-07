from __future__ import annotations

from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .base import TimestampedModel


class ApprovalMetadata(BaseModel):
    approver_id: UUID = Field(default_factory=uuid4)
    approver_name: str
    approval_timestamp: Optional[str] = None
    approval_notes: Optional[str] = None

    model_config = {"extra": "forbid"}


class ProvenanceRecord(TimestampedModel):
    record_id: UUID = Field(default_factory=uuid4)
    source: str
    author: Optional[str] = None
    change_description: Optional[str] = None


class ApprovedSnapshot(TimestampedModel):
    snapshot_id: UUID = Field(default_factory=uuid4)
    bundle_id: UUID
    manifest_version: str
    approvals: List[ApprovalMetadata] = Field(default_factory=list)
    provenance: List[ProvenanceRecord] = Field(default_factory=list)

    model_config = {"extra": "forbid"}
