from __future__ import annotations

from typing import Any, Dict


def estimate_costs(metadata: Any) -> Dict[str, Any]:
    """Estimate annual costs based on basic parameters."""
    size = metadata.get("scale", "small") if isinstance(metadata, dict) else "small"
    factor = {"small": 1, "medium": 3, "large": 10}.get(size, 1)
    return {"annual": 10000 * factor, "citation": "knowledge:costs#estimator"}
