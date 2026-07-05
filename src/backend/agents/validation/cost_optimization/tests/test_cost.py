from backend.agents.validation.cost_optimization.tco_modeler import model_tco
from backend.agents.validation.cost_optimization.cost_estimator import estimate_costs
from backend.agents.validation.cost_optimization.optimization_advisor import (
    advise_optimizations,
)


def test_tco_model_returns() -> None:
    t = model_tco(None)
    assert "3y" in t


def test_cost_estimation_and_advice() -> None:
    est = estimate_costs({"scale": "large"})
    advice = advise_optimizations(est)
    assert isinstance(advice, list)
