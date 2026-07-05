from __future__ import annotations

from typing import List

from .models import Requirement


def simple_classifier(reqs: List[Requirement]) -> List[Requirement]:
    """Attach a trivial tag based on keyword presence."""
    out: List[Requirement] = []
    for r in reqs:
        tags: List[str] = []
        txt = r.text.lower()
        if "must" in txt or "shall" in txt:
            tags.append("MUST")
        if "should" in txt:
            tags.append("SHOULD")
        out.append(Requirement(text=r.text, tags=tags))
    return out
