from __future__ import annotations

import asyncio

from backend.agents.discovery.requirement_intelligence.agent import (
    RequirementIntelligenceAgent,
)
from backend.agents.base.agent_context import AgentContext
from typing import cast, Any, Dict


def test_agent_execution() -> None:
    agent = RequirementIntelligenceAgent()
    ctx = AgentContext(
        execution_id="e1", metadata={"text": "Must do this. Maybe do that."}
    )
    res = asyncio.get_event_loop().run_until_complete(agent.execute(ctx))
    assert res.success
    payload = cast(Dict[str, Any], res.payload)
    assert payload["requirements_count"] == 2
