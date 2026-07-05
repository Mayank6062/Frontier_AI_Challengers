from __future__ import annotations

import asyncio

from ..pipeline_stages.review_stage import ReviewStage
from ..pipeline_manager import PipelineManager
from ..models import StageDefinition, WorkflowContext


def test_review_stage_runs() -> None:
    stages = {
        "governance_check": StageDefinition(
            stage_id="governance_check", agent_id="gov_agent"
        ),
        "human_review": StageDefinition(
            stage_id="human_review", agent_id="human_agent"
        ),
    }
    groups = [["governance_check", "human_review"]]
    pm = PipelineManager(stages=stages, groups=groups)

    from ...agents.base.agent_registry import AgentRegistry
    from ...core.interfaces.agent_interface import AgentInterface
    from ...agents.base.agent_context import AgentContext
    from ...agents.base.agent_result import AgentResult

    reg = AgentRegistry()

    class GovAgent(AgentInterface):
        AGENT_ID = "gov"
        AGENT_VERSION = "0.1"
        AGENT_CATEGORY = None
        AGENT_NAME = "gov"

        async def execute(self, context: AgentContext) -> AgentResult:
            return AgentResult.success_result(payload={"governance": "ok"})

    class HumanAgent(AgentInterface):
        AGENT_ID = "human"
        AGENT_VERSION = "0.1"
        AGENT_CATEGORY = None
        AGENT_NAME = "human"

        async def execute(self, context: AgentContext) -> AgentResult:
            return AgentResult.success_result(payload={"approved": True})

    reg.register("gov_agent", lambda: GovAgent())
    reg.register("human_agent", lambda: HumanAgent())

    from ..agent_scheduler import AgentScheduler

    scheduler = AgentScheduler(reg)
    rs = ReviewStage(scheduler, pm)

    ctx = WorkflowContext(engagement_id="e4", input_payload={"req": "z"})

    results = asyncio.run(rs.execute(ctx))
    assert len(results) == 2
    assert any(r.stage_id == "human_review" and r.status == "SUCCESS" for r in results)
