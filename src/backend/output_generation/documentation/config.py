from __future__ import annotations

from pydantic import BaseModel

from .settings import DocumentationSettings


class DocumentationConfig(BaseModel):
    settings: DocumentationSettings
    enabled: bool = True

    model_config = {"extra": "forbid", "frozen": True}
