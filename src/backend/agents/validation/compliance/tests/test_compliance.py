from backend.agents.validation.compliance.framework_evaluator import evaluate_frameworks
from backend.agents.validation.compliance.control_checker import check_controls
from backend.agents.validation.compliance.residency_validator import validate_residency


def test_frameworks_and_controls() -> None:
    f = evaluate_frameworks(None)
    c = check_controls(None)
    r = validate_residency(None)
    assert isinstance(f, list)
    assert isinstance(c, list)
    assert isinstance(r, dict)
