from __future__ import annotations

import asyncio

from ..pipeline_stages.output_stage import OutputStage
from ..pipeline_manager import PipelineManager
from ..models import StageDefinition, WorkflowContext


def test_output_stage_runs() -> None:
    stages = {
        "document_generation": StageDefinition(
            stage_id="document_generation", agent_id="doc_agent"
        ),
    }
    groups = [["document_generation"]]
    pm = PipelineManager(stages=stages, groups=groups)

    from ...agents.base.agent_registry import AgentRegistry
    from ...core.interfaces.agent_interface import AgentInterface
    from ...agents.base.agent_context import AgentContext
    from ...agents.base.agent_result import AgentResult

    reg = AgentRegistry()

    class DocAgent(AgentInterface):
        AGENT_ID = "doc"
        AGENT_VERSION = "0.1"
        AGENT_CATEGORY = None
        AGENT_NAME = "doc"

        async def execute(self, context: AgentContext) -> AgentResult:
            return AgentResult.success_result(payload={"doc": "generated"})

    reg.register("doc_agent", lambda: DocAgent())

    from ..agent_scheduler import AgentScheduler

    scheduler = AgentScheduler(reg)
    os = OutputStage(scheduler, pm)

    ctx = WorkflowContext(engagement_id="e5", input_payload={"req": "o"})

    results = asyncio.run(os.execute(ctx))
    assert len(results) == 1
    assert results[0].status == "SUCCESS"
