from __future__ import annotations

from typing import List

from .models import Document


def length_ranker(docs: List[Document]) -> List[Document]:
    return sorted(docs, key=lambda d: len(d.content), reverse=True)
