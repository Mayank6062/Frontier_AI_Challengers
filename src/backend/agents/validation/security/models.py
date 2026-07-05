from __future__ import annotations

from pydantic import BaseModel


class Threat(BaseModel):
    id: str
    description: str
    severity: str
    citation: str


class ControlMapping(BaseModel):
    threat: str
    control: str
    citation: str
