from __future__ import annotations

from typing import List

from .models import Document


def build_citations(docs: List[Document]) -> List[str]:
    return [f"{d.id}: {d.content[:30]}" for d in docs]
