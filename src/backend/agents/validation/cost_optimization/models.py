from __future__ import annotations

from pydantic import BaseModel


class CostEstimate(BaseModel):
    annual: float
    citation: str


class OptimizationAdvice(BaseModel):
    action: str
    impact: str
