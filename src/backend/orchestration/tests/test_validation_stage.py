from __future__ import annotations

import asyncio

from ..pipeline_stages.validation_stage import ValidationStage
from ..pipeline_manager import PipelineManager
from ..models import StageDefinition, WorkflowContext


def test_validation_stage_runs() -> None:
    stages = {
        "security_validation": StageDefinition(
            stage_id="security_validation", agent_id="sec_agent"
        ),
        "compliance_validation": StageDefinition(
            stage_id="compliance_validation", agent_id="comp_agent"
        ),
        "cost_analysis": StageDefinition(
            stage_id="cost_analysis", agent_id="cost_agent"
        ),
        "risk_assessment": StageDefinition(
            stage_id="risk_assessment", agent_id="risk_agent"
        ),
    }
    groups = [
        [
            "security_validation",
            "compliance_validation",
            "cost_analysis",
            "risk_assessment",
        ]
    ]
    pm = PipelineManager(stages=stages, groups=groups)

    from ...agents.base.agent_registry import AgentRegistry
    from ...core.interfaces.agent_interface import AgentInterface
    from ...agents.base.agent_context import AgentContext
    from ...agents.base.agent_result import AgentResult

    reg = AgentRegistry()

    class SimpleAgent(AgentInterface):
        AGENT_ID = "a"
        AGENT_VERSION = "0.1"
        AGENT_CATEGORY = None
        AGENT_NAME = "a"

        async def execute(self, context: AgentContext) -> AgentResult:
            # return a minimal AgentResult for the scheduler
            return AgentResult.success_result(payload={"ok": True})

    reg.register("sec_agent", lambda: SimpleAgent())
    reg.register("comp_agent", lambda: SimpleAgent())
    reg.register("cost_agent", lambda: SimpleAgent())
    reg.register("risk_agent", lambda: SimpleAgent())

    from ..agent_scheduler import AgentScheduler

    scheduler = AgentScheduler(reg)
    vs = ValidationStage(scheduler, pm)

    ctx = WorkflowContext(engagement_id="e3", input_payload={"req": "y"})

    results = asyncio.run(vs.execute(ctx))
    assert len(results) == 4
    assert all(r.status == "SUCCESS" for r in results)
