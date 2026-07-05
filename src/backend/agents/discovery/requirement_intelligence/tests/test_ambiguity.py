from __future__ import annotations

from backend.agents.discovery.requirement_intelligence.ambiguity_detector import (
    detect_ambiguities,
)
from backend.agents.discovery.requirement_intelligence.models import Requirement


def test_detect_ambiguities() -> None:
    reqs = [Requirement(text="maybe", tags=[]), Requirement(text="Do X", tags=[])]
    amb = detect_ambiguities(reqs)
    assert "maybe" in amb
