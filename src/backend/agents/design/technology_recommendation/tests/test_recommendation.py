from backend.agents.design.technology_recommendation.catalog_searcher import (
    search_catalog,
)
from backend.agents.design.technology_recommendation.scorer import score_technologies
from backend.agents.design.technology_recommendation.build_vs_buy import (
    analyze_build_vs_buy,
)


def test_search_catalog_basic() -> None:
    res = search_catalog(None)
    assert any(r["id"] == "tech-postgres" for r in res)


def test_scoring_and_decision() -> None:
    candidates = search_catalog("analytics")
    scored = score_technologies(candidates)
    decision = analyze_build_vs_buy(scored)
    assert "decision" in decision
