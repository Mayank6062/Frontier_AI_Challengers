from __future__ import annotations

from typing import List

from .models import Requirement


def detect_ambiguities(reqs: List[Requirement]) -> List[str]:
    """Return list of requirement texts considered ambiguous.

    Heuristic: short requirements (< 5 chars) or containing 'maybe' are ambiguous.
    """
    amb: List[str] = []
    for r in reqs:
        if len(r.text) < 5 or "maybe" in r.text.lower():
            amb.append(r.text)
    return amb
