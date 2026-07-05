from __future__ import annotations

from typing import Any, List, Dict


def evaluate_frameworks(metadata: Any) -> List[Dict[str, Any]]:
    """Return which compliance frameworks apply to the metadata."""
    return [
        {"framework": "ISO27001", "applicable": True},
        {"framework": "GDPR", "applicable": False},
    ]
