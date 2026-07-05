from __future__ import annotations

from pydantic import BaseModel


class Proposal(BaseModel):
    title: str
    summary: str
    citation: str
