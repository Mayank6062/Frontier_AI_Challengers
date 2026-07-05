from __future__ import annotations

from typing import Any, List, Dict


def check_controls(metadata: Any) -> List[Dict[str, Any]]:
    return [
        {"control": "encryption_at_rest", "status": "ok"},
        {"control": "access_review", "status": "missing"},
    ]
