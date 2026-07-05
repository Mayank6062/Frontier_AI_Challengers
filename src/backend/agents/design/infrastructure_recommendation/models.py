from __future__ import annotations

from pydantic import BaseModel
from typing import Dict, List, Any


class Topology(BaseModel):
    type: str
    nodes: int
    citation: str


class LandingZone(BaseModel):
    name: str
    controls: List[str]
    citation: str


class IaCPlan(BaseModel):
    modules: List[Dict[str, Any]]
    landing_zone: str
    citation: str
