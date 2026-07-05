from __future__ import annotations

from backend.agents.base.agent_registry import AgentRegistry
from backend.agents.base.base_agent import BaseAgent
from backend.agents.base.agent_context import AgentContext
from backend.agents.base.agent_result import AgentResult


class DummyAgent(BaseAgent):
    AGENT_ID = "dummy"
    AGENT_NAME = "Dummy"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        return AgentResult.success_result(payload={"ok": True})


def test_registry_register_and_get() -> None:
    registry = AgentRegistry()
    registry.register("dummy", lambda: DummyAgent())
    assert registry.exists("dummy")
    inst = registry.get("dummy")
    assert isinstance(inst, BaseAgent)
    assert list(registry.list()) == ["dummy"]
    registry.unregister("dummy")
    assert not registry.exists("dummy")
