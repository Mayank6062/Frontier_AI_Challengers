from __future__ import annotations

from backend.agents.discovery.requirement_intelligence.extractor import simple_extractor


def test_simple_extractor() -> None:
    r = simple_extractor("Do X. Then do Y.")
    assert len(r.requirements) == 2
    assert r.requirements[0].text == "Do X"
