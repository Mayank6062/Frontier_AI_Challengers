from __future__ import annotations

from pydantic import BaseModel


class RiskItem(BaseModel):
    risk_id: str
    description: str
    likelihood: float
    impact: float
    score: float | None = None
