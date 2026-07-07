from __future__ import annotations

from pydantic import BaseModel
from typing import Optional


class DocumentationLimits(BaseModel):
    max_document_size_bytes: int = 10 * 1024 * 1024
    max_word_count: int = 200_000

    model_config = {"extra": "forbid", "frozen": True}


class DocumentationSettings(BaseModel):
    limits: DocumentationLimits
    default_template_version: Optional[str]

    model_config = {"extra": "forbid", "frozen": True}
