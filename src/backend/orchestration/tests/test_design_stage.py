from __future__ import annotations

import asyncio

from ..pipeline_stages.design_stage import DesignStage
from ..pipeline_manager import PipelineManager
from ..models import StageDefinition, WorkflowContext


def test_design_stage_runs() -> None:
    stages = {
        "architecture_design": StageDefinition(
            stage_id="architecture_design", agent_id="arch_agent"
        ),
        "technology_recommendation": StageDefinition(
            stage_id="technology_recommendation", agent_id="tech_agent"
        ),
        "infrastructure_recommendation": StageDefinition(
            stage_id="infrastructure_recommendation", agent_id="infra_agent"
        ),
    }
    groups = [
        [
            "architecture_design",
            "technology_recommendation",
            "infrastructure_recommendation",
        ]
    ]
    pm = PipelineManager(stages=stages, groups=groups)

    from ...agents.base.agent_registry import AgentRegistry
    from ...core.interfaces.agent_interface import AgentInterface
    from ...agents.base.agent_context import AgentContext
    from ...agents.base.agent_result import AgentResult

    reg = AgentRegistry()

    class ArchAgent(AgentInterface):
        AGENT_ID = "arch"
        AGENT_VERSION = "0.1"
        AGENT_CATEGORY = None
        AGENT_NAME = "arch"

        async def execute(self, context: AgentContext) -> AgentResult:
            return AgentResult.success_result(payload={"candidates": ["a"]})

    class TechAgent(AgentInterface):
        AGENT_ID = "tech"
        AGENT_VERSION = "0.1"
        AGENT_CATEGORY = None
        AGENT_NAME = "tech"

        async def execute(self, context: AgentContext) -> AgentResult:
            return AgentResult.success_result(payload={"techs": ["t"]})

    class InfraAgent(AgentInterface):
        AGENT_ID = "infra"
        AGENT_VERSION = "0.1"
        AGENT_CATEGORY = None
        AGENT_NAME = "infra"

        async def execute(self, context: AgentContext) -> AgentResult:
            return AgentResult.success_result(payload={"infra": ["i"]})

    reg.register("arch_agent", lambda: ArchAgent())
    reg.register("tech_agent", lambda: TechAgent())
    reg.register("infra_agent", lambda: InfraAgent())

    from ..agent_scheduler import AgentScheduler

    scheduler = AgentScheduler(reg)
    ds = DesignStage(scheduler, pm)

    ctx = WorkflowContext(engagement_id="e2", input_payload={"req": "x"})

    results = asyncio.run(ds.execute(ctx))
    assert len(results) == 3
    assert any(
        r.stage_id == "architecture_design" and r.status == "SUCCESS" for r in results
    )
