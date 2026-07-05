from __future__ import annotations

import asyncio
from typing import List, Callable

from .agent_scheduler import AgentScheduler
from .message_bus import MessageBus
from .models import (
    ExecutionPlan,
    StageDefinition,
    StageResult,
    StageStatus,
    WorkflowContext,
)
from .pipeline_manager import PipelineManager
from .result_aggregator import ResultAggregator


class MasterOrchestrator:
    """Coordinates execution per WORKFLOW_ENGINE.md.

    - Stateless: caller provides WorkflowContext and Engagement Manager handles state.
    - Writes checkpoints by invoking the provided checkpoint_writer callable.
    - Emits progress events via MessageBus.
    """

    def __init__(
        self,
        pipeline_manager: PipelineManager,
        scheduler: AgentScheduler,
        aggregator: ResultAggregator,
        bus: MessageBus,
    ) -> None:
        self._pipeline = pipeline_manager
        self._scheduler = scheduler
        self._aggregator = aggregator
        self._bus = bus

    async def run_phase(
        self,
        ctx: WorkflowContext,
        checkpoint_writer: Callable[[str, List[str], List[StageResult]], None],
    ) -> List[StageResult]:
        plan: ExecutionPlan = self._pipeline.build_execution_plan()
        all_results: List[StageResult] = []

        for group in plan.stage_groups:
            # dispatch group in parallel
            tasks = []
            for stage_id in group:
                sd: StageDefinition = self._pipeline.get_stage_definition(stage_id)
                task = asyncio.create_task(
                    self._scheduler.execute_stage(
                        stage_id, sd.agent_id, ctx, timeout=sd.timeout_seconds
                    )
                )
                tasks.append(task)

            group_results = await asyncio.gather(*tasks)

            # validate structural completeness
            for r in group_results:
                if (
                    r.status == StageStatus.FAILED
                    and self._pipeline.get_stage_definition(r.stage_id).required
                ):
                    # emit progress then raise to caller
                    self._bus.publish(
                        "progress",
                        {
                            "engagement_id": ctx.engagement_id,
                            "stage": r.stage_id,
                            "status": "FAILED",
                            "error": r.error,
                        },
                    )
                    return all_results + list(group_results)

            # aggregate
            self._aggregator.aggregate(ctx, list(group_results))

            # checkpoint
            checkpoint_writer(ctx.engagement_id, group, list(group_results))

            # emit progress
            self._bus.publish(
                "progress",
                {
                    "engagement_id": ctx.engagement_id,
                    "stage_group": group,
                    "status": "COMPLETED",
                },
            )

            all_results.extend(list(group_results))

        return all_results
