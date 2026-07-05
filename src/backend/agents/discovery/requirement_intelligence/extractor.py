from __future__ import annotations

from .models import Requirement, ExtractionResult


def simple_extractor(text: str) -> ExtractionResult:
    """Naive extractor splitting text into sentence-like requirements.

    This is intentionally simple for unit testing and to avoid infra.
    """
    parts = [p.strip() for p in text.split(".") if p.strip()]
    reqs = [Requirement(text=p, tags=[]) for p in parts]
    return ExtractionResult(requirements=reqs)
