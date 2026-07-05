from __future__ import annotations

import asyncio
from pathlib import Path

from ..pipeline_stages.discovery_stage import DiscoveryStage
from ..pipeline_manager import PipelineManager
from ..models import StageDefinition, WorkflowContext


def test_discovery_stage_runs(tmp_path: Path) -> None:
    stages = {
        "requirement_intelligence": StageDefinition(
            stage_id="requirement_intelligence", agent_id="req_agent"
        ),
        "knowledge_retrieval": StageDefinition(
            stage_id="knowledge_retrieval", agent_id="kr_agent"
        ),
    }
    groups = [["requirement_intelligence", "knowledge_retrieval"]]
    pm = PipelineManager(stages=stages, groups=groups)

    from ...agents.base.agent_registry import AgentRegistry
    from ...core.interfaces.agent_interface import AgentInterface
    from ...agents.base.agent_context import AgentContext
    from ...agents.base.agent_result import AgentResult

    reg = AgentRegistry()

    class ReqAgent(AgentInterface):
        AGENT_ID = "req"
        AGENT_VERSION = "0.1"
        AGENT_CATEGORY = None
        AGENT_NAME = "req"

        async def execute(self, context: AgentContext) -> AgentResult:
            return AgentResult.success_result(payload={"requirements": ["r1"]})

    class KRAgent(AgentInterface):
        AGENT_ID = "kr"
        AGENT_VERSION = "0.1"
        AGENT_CATEGORY = None
        AGENT_NAME = "kr"

        async def execute(self, context: AgentContext) -> AgentResult:
            return AgentResult.success_result(payload={"knowledge": ["k1"]})

    reg.register("req_agent", lambda: ReqAgent())
    reg.register("kr_agent", lambda: KRAgent())

    from ..agent_scheduler import AgentScheduler

    scheduler = AgentScheduler(reg)
    ds = DiscoveryStage(scheduler, pm)

    ctx = WorkflowContext(engagement_id="e1", input_payload={"text": "hello"})

    results = asyncio.run(ds.execute(ctx))
    assert any(
        r.stage_id == "requirement_intelligence" and r.status == "SUCCESS"
        for r in results
    )
    assert any(
        r.stage_id == "knowledge_retrieval" and r.status == "SUCCESS" for r in results
    )
