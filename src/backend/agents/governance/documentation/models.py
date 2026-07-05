from __future__ import annotations

from pydantic import BaseModel


class DocumentArtifact(BaseModel):
    title: str
    content: str
    citation: str
