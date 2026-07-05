from __future__ import annotations

from pydantic import BaseModel


class FrameworkAssessment(BaseModel):
    framework: str
    applicable: bool


class ControlStatus(BaseModel):
    control: str
    status: str
