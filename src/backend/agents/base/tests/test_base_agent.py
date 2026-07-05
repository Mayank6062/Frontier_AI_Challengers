import asyncio

from backend.agents.base.base_agent import BaseAgent
from backend.agents.base.agent_context import AgentContext
from backend.agents.base.agent_result import AgentResult


class NoopAgent(BaseAgent):
    AGENT_ID = "noop"
    AGENT_NAME = "Noop"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        return AgentResult.success_result(payload={"noop": True})


async def run_agent() -> AgentResult:
    agent = NoopAgent()
    ctx = AgentContext(execution_id="e1")
    res = await agent.execute(ctx)
    return res


def test_base_agent_lifecycle() -> None:
    res = asyncio.get_event_loop().run_until_complete(run_agent())
    assert res.success
    assert isinstance(res.payload, dict)
    assert res.payload.get("noop") is True
