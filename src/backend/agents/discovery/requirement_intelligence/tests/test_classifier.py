from __future__ import annotations

from backend.agents.discovery.requirement_intelligence.classifier import (
    simple_classifier,
)
from backend.agents.discovery.requirement_intelligence.models import Requirement


def test_simple_classifier() -> None:
    reqs = [Requirement(text="System must store data", tags=[])]
    out = simple_classifier(reqs)
    assert out[0].tags == ["MUST"]
