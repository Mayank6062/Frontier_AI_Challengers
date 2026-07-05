from backend.agents.governance.governance.policy_enforcer import enforce_policies
from backend.agents.governance.governance.guardrail_checker import check_guardrails
from backend.agents.governance.governance.catalog_validator import validate_catalog


def test_governance_helpers() -> None:
    assert enforce_policies(None)["status"] == "passed"
    assert isinstance(check_guardrails(None), list)
    assert validate_catalog(None)["catalog_valid"] is True
