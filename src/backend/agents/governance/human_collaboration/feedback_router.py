from __future__ import annotations

from typing import Any, Dict


def route_feedback(proposal: Any) -> Dict[str, Any]:
    return {"status": "routed", "reviewers": ["architect@example.com"]}
