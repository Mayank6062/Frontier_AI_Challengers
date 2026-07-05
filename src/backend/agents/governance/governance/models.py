from __future__ import annotations

from pydantic import BaseModel
from typing import List


class GovernanceReport(BaseModel):
    policies: List[str]
    guardrails: List[str]
