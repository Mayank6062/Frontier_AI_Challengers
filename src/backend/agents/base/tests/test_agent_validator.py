from __future__ import annotations

from backend.agents.base.agent_validator import AgentValidator
from backend.agents.base.agent_result import AgentResult


def test_validator_confidence_range() -> None:
    val = AgentValidator()
    r = AgentResult.success_result(payload={})
    r = r.copy(update={"confidence": 1.2})
    res = val.validate(r)
    assert not res.passed
    assert any("confidence_out_of_range" in e for e in res.errors)


def test_validator_payload_type() -> None:
    val = AgentValidator()
    r = AgentResult.success_result(payload={})
    r = r.copy(update={"payload": "not-a-dict"})
    res = val.validate(r)
    assert not res.passed
    assert "payload_not_dict" in res.errors
