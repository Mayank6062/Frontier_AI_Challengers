from __future__ import annotations

import asyncio
from pathlib import Path

from ..master_orchestrator import MasterOrchestrator
from ..pipeline_manager import PipelineManager
from ..models import StageDefinition, WorkflowContext, StageResult, StageStatus
from ..agent_scheduler import AgentScheduler
from ..result_aggregator import ResultAggregator
from ..message_bus import MessageBus
from ...core.interfaces.agent_interface import AgentInterface
from ...agents.base.agent_context import AgentContext
from ...agents.base.agent_result import AgentResult


class TestAgent(AgentInterface):
    AGENT_ID = "test"
    AGENT_VERSION = "0.1"
    AGENT_CATEGORY = None
    AGENT_NAME = "test"

    async def execute(self, context: AgentContext) -> AgentResult:
        return AgentResult.success_result(payload={"ok": True})


def test_master_orchestrator_runs_and_checkpoints(tmp_path: Path) -> None:
    # setup simple pipeline: intake (system) -> run test agent
    stages = {
        "intake": StageDefinition(stage_id="intake", agent_id=None, required=True),
        "run_test": StageDefinition(
            stage_id="run_test", agent_id="test_agent", required=True
        ),
    }
    groups = [["intake"], ["run_test"]]
    pm = PipelineManager(stages=stages, groups=groups)

    # AgentRegistry local import
    from ...agents.base.agent_registry import AgentRegistry

    reg = AgentRegistry()
    # register factory returning TestAgent instance
    reg.register("test_agent", lambda: TestAgent())

    scheduler = AgentScheduler(reg)
    agg = ResultAggregator()
    bus = MessageBus()

    orchestrator = MasterOrchestrator(pm, scheduler, agg, bus)

    ctx = WorkflowContext(engagement_id="e1", input_payload={"req": "x"})

    checkpoints = []

    def checkpoint_writer(
        eid: str, group: list[str], results: list[StageResult]
    ) -> None:
        checkpoints.append(
            (eid, tuple(group), tuple((r.stage_id, r.status) for r in results))
        )

    results = asyncio.run(orchestrator.run_phase(ctx, checkpoint_writer))

    # verify checkpoints written for both groups
    assert len(checkpoints) == 2
    # verify aggregated context contains outputs from run_test
    assert "run_test" in ctx.accumulated
    assert ctx.accumulated["run_test"]["ok"] is True
    # verify results include StageResult for run_test
    assert any(
        r.stage_id == "run_test" and r.status == StageStatus.SUCCESS for r in results
    )
