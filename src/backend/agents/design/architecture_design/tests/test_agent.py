from backend.agents.design.architecture_design.candidate_generator import (
    generate_candidates,
)
from backend.agents.design.architecture_design.tradeoff_analyzer import (
    analyze_tradeoffs,
)
from backend.agents.design.architecture_design.pattern_composer import compose_patterns


def test_generate_candidates_small() -> None:
    req = {"scale": "small"}
    candidates = generate_candidates(req)
    assert len(candidates) >= 1
    assert any(c["pattern"] for c in candidates)


def test_analyze_tradeoffs_ranking() -> None:
    cands = [
        {"id": "a", "score": 0.1, "cost_estimate": 10},
        {"id": "b", "score": 0.9, "cost_estimate": 1000},
    ]
    ranked = analyze_tradeoffs(cands)
    assert ranked[0]["id"] == "a" or ranked[0]["id"] == "b"


def test_compose_patterns_structure() -> None:
    cands = [{"id": "x", "pattern": "microservices"}]
    patterns = compose_patterns(None, cands)
    assert isinstance(patterns, list)
    assert patterns[0]["candidate_id"] == "x"
