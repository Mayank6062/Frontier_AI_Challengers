from __future__ import annotations

import asyncio

from backend.agents.discovery.knowledge_retrieval.agent import KnowledgeRetrievalAgent
from backend.agents.base.agent_context import AgentContext
from typing import cast, Any, Dict


def test_knowledge_agent_execution() -> None:
    agent = KnowledgeRetrievalAgent()
    ctx = AgentContext(execution_id="e1", metadata={"query": "term"})
    res = asyncio.get_event_loop().run_until_complete(agent.execute(ctx))
    assert res.success
    payload = cast(Dict[str, Any], res.payload)
    assert payload["count"] == 2
