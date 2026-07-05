from __future__ import annotations

import asyncio
from typing import List, Optional

from ..models import StageResult, StageStatus, WorkflowContext
from ..agent_scheduler import AgentScheduler
from ..pipeline_manager import PipelineManager


class OutputStage:
    """Orchestration-only stage that coordinates document generation agents.

    Never generates documents itself.
    """

    def __init__(
        self, scheduler: AgentScheduler, pipeline_manager: PipelineManager
    ) -> None:
        self._scheduler = scheduler
        self._pipeline = pipeline_manager

    async def execute(
        self,
        ctx: WorkflowContext,
        cancellation_event: Optional[asyncio.Event] = None,
        retries: int = 1,
        timeout: Optional[int] = None,
    ) -> List[StageResult]:
        results: List[StageResult] = []

        stage_ids = ["document_generation"]

        for stage_id in stage_ids:
            if cancellation_event and cancellation_event.is_set():
                results.append(
                    StageResult(
                        stage_id=stage_id,
                        status=StageStatus.SKIPPED,
                        output=None,
                        error="cancelled",
                    )
                )
                break

            sd = self._pipeline.get_stage_definition(stage_id)

            attempt = 0
            while attempt <= retries:
                attempt += 1
                res = await self._scheduler.execute_stage(
                    stage_id, sd.agent_id, ctx, timeout=timeout or sd.timeout_seconds
                )
                results.append(res)
                if res.status == StageStatus.SUCCESS:
                    break
                if attempt <= retries:
                    await asyncio.sleep(0)
            if res.status != StageStatus.SUCCESS and sd.required:
                break

        return results
