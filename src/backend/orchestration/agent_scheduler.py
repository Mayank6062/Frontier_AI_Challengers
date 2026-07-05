from __future__ import annotations

import asyncio
from typing import List, Optional

from ..agents.base.agent_registry import AgentRegistry
from ..agents.base.agent_context import AgentContext
from ..agents.base.agent_result import AgentResult
from .models import StageResult, StageStatus, WorkflowContext


class AgentScheduler:
    """Schedules and executes agent stages.

    The scheduler only interacts with agents via the AgentRegistry, producing
    `StageResult` objects. It enforces timeouts but does not interpret agent
    outputs beyond structural success/failure.
    """

    def __init__(self, registry: AgentRegistry) -> None:
        self._registry = registry

    async def execute_stage(
        self,
        stage_id: str,
        agent_id: Optional[str],
        ctx: WorkflowContext,
        timeout: Optional[int] = None,
    ) -> StageResult:
        if agent_id is None:
            # system-level stage; scheduler returns success with input echo
            return StageResult(
                stage_id=stage_id,
                status=StageStatus.SUCCESS,
                output={"echo": ctx.input_payload},
            )

        if not self._registry.exists(agent_id):
            return StageResult(
                stage_id=stage_id,
                status=StageStatus.FAILED,
                error=f"agent_not_registered:{agent_id}",
            )

        agent = self._registry.get(agent_id)

        async def run_agent() -> StageResult:
            try:
                # build a minimal AgentContext from WorkflowContext
                agent_ctx = AgentContext(
                    engagement_id=ctx.engagement_id, metadata=ctx.input_payload
                )
                result = await agent.execute(agent_ctx)

                # If agent returned a dict - normalize
                if isinstance(result, dict):
                    return StageResult(
                        stage_id=stage_id, status=StageStatus.SUCCESS, output=result
                    )

                # If agent returned an AgentResult, convert to StageResult
                if isinstance(result, AgentResult):
                    status = (
                        StageStatus.SUCCESS if result.success else StageStatus.FAILED
                    )
                    output = result.payload or {}
                    error = ", ".join(result.errors) if result.errors else None
                    citations: List[str] = []
                    # AgentResult may contain citations in its metadata or fields
                    if hasattr(result, "citations") and result.citations:
                        citations = list(result.citations)
                    return StageResult(
                        stage_id=stage_id,
                        status=status,
                        output=output,
                        error=error,
                        confidence=result.confidence,
                        citations=citations,
                        errors=result.errors,
                    )

                # Fallback: unexpected return type
                return StageResult(
                    stage_id=stage_id,
                    status=StageStatus.FAILED,
                    error="invalid_agent_result_type",
                )
            except Exception as exc:  # pragma: no cover - defensive
                return StageResult(
                    stage_id=stage_id, status=StageStatus.FAILED, error=str(exc)
                )

        task = asyncio.create_task(run_agent())
        try:
            done = await asyncio.wait_for(task, timeout=timeout)
            return done
        except asyncio.TimeoutError:
            task.cancel()
            return StageResult(
                stage_id=stage_id, status=StageStatus.FAILED, error="timeout"
            )
