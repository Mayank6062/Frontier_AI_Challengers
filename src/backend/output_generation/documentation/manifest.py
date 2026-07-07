from __future__ import annotations

from datetime import datetime
from typing import Sequence, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .models import DocumentFileMetadata, DocumentVersionMetadata


class DocumentationManifest(BaseModel):
    manifest_id: UUID = Field(default_factory=uuid4)
    created_at: datetime
    files: Sequence[DocumentFileMetadata]
    versions: Optional[Sequence[DocumentVersionMetadata]]

    model_config = {"extra": "forbid", "frozen": True}
