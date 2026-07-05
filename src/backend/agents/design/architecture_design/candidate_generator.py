from __future__ import annotations

from typing import Any, List, Dict, Optional


def generate_candidates(
    requirements: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Generate architecture candidate proposals from requirements.

    This function implements a deterministic, testable candidate generator.
    It intentionally avoids external calls and relies only on the provided
    requirements structure.
    """
    base = requirements or {}
    size = base.get("scale", "small")
    candidates: List[Dict[str, Any]] = []
    if size == "small":
        candidates.append({"id": "cand-1", "pattern": "monolith", "score": 0.4})
        candidates.append({"id": "cand-2", "pattern": "modular-monolith", "score": 0.6})
    elif size == "medium":
        candidates.append({"id": "cand-1", "pattern": "modular-monolith", "score": 0.5})
        candidates.append({"id": "cand-2", "pattern": "microservices", "score": 0.5})
    else:
        candidates.append({"id": "cand-1", "pattern": "microservices", "score": 0.7})
        candidates.append({"id": "cand-2", "pattern": "serverless", "score": 0.3})

    # add deterministic metadata
    for c in candidates:
        c.setdefault("cost_estimate", 1000)
        c.setdefault("citation", "knowledge:architecture_patterns#v1")

    return candidates
