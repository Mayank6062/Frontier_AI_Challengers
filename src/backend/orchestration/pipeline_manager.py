from __future__ import annotations

from typing import Dict, List

from .models import ExecutionPlan, StageDefinition


class PipelineManager:
    """Loads static pipeline configuration and exposes execution plans.

    For now this manager accepts a plan dict during construction. In production
    the plan would be loaded from configuration storage.
    """

    def __init__(
        self, stages: Dict[str, StageDefinition], groups: List[List[str]]
    ) -> None:
        self._stages = stages
        self._groups = groups

    def get_stage_definition(self, stage_id: str) -> StageDefinition:
        return self._stages[stage_id]

    def build_execution_plan(self) -> ExecutionPlan:
        return ExecutionPlan(stage_groups=self._groups)
