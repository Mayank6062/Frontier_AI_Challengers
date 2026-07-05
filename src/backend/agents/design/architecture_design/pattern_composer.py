from __future__ import annotations

from typing import Any, List, Dict


def compose_patterns(
    context: Any, candidates: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Attach pattern guidance and citations to candidates.

    This function is intentionally lightweight: it synthesizes pattern
    recommendations based on candidate patterns and uses static citations
    that reference the knowledge catalog.
    """
    result = []
    for c in candidates:
        pattern = c.get("pattern", "unknown")
        rec = {
            "candidate_id": c.get("id"),
            "pattern": pattern,
            "rationale": f"Selected pattern {pattern} for candidate {c.get('id')}",
            "confidence": 0.75,
            "citation": f"knowledge:patterns/{pattern}#v1",
        }
        result.append(rec)
    return result
