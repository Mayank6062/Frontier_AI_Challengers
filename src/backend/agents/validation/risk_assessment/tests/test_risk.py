from backend.agents.validation.risk_assessment.risk_aggregator import aggregate_risks
from backend.agents.validation.risk_assessment.risk_scorer import score_risks
from backend.agents.validation.risk_assessment.mitigation_advisor import (
    recommend_mitigations,
)


def test_risk_flow() -> None:
    agg = aggregate_risks(None)
    scored = score_risks(agg)
    mitigations = recommend_mitigations(scored)
    assert isinstance(agg, list)
    assert isinstance(scored, list)
    assert isinstance(mitigations, list)
