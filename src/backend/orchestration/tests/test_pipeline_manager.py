from __future__ import annotations

from ..pipeline_manager import PipelineManager
from ..models import StageDefinition


def test_pipeline_manager_builds_plan() -> None:
    stages = {
        "s1": StageDefinition(stage_id="s1", agent_id=None),
        "s2": StageDefinition(stage_id="s2", agent_id="agent_x"),
    }
    groups = [["s1"], ["s2"]]
    pm = PipelineManager(stages=stages, groups=groups)
    plan = pm.build_execution_plan()
    assert len(plan.stage_groups) == 2
    assert plan.stage_groups[0] == ["s1"]
    assert pm.get_stage_definition("s2").agent_id == "agent_x"
