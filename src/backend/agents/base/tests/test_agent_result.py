from __future__ import annotations

from backend.agents.base.agent_result import AgentResult


def test_agent_result_success_and_helpers() -> None:
    r = AgentResult.success_result(payload={"x": 1}, confidence=0.9, agent_name="A")
    assert r.success
    assert r.status == "SUCCESS"
    assert isinstance(r.payload, dict)
    assert r.payload["x"] == 1
    assert r.confidence == 0.9


def test_agent_result_failure() -> None:
    r = AgentResult.failure_result(["err1"], agent_name="B")
    assert not r.success
    assert r.status == "FAILURE"
    assert r.errors == ["err1"]
