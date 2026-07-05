from backend.agents.design.infrastructure_recommendation.topology_designer import (
    design_topology,
)
from backend.agents.design.infrastructure_recommendation.iac_scaffolder import (
    generate_iac_plan,
)


def test_design_topology_default() -> None:
    t = design_topology(None)
    assert t["type"] in ("single-region", "multi-region")


def test_generate_iac_plan() -> None:
    topo = {"nodes": 2}
    lz = {"name": "standard"}
    plan = generate_iac_plan(topo, lz)
    assert "modules" in plan
