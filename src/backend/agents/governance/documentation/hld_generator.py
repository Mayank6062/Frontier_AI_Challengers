from __future__ import annotations

from typing import Any, Dict


def generate_hld(metadata: Any) -> Dict[str, Any]:
    return {
        "title": "High Level Design",
        "sections": ["overview", "components"],
        "citation": "knowledge:docs#hld",
    }
