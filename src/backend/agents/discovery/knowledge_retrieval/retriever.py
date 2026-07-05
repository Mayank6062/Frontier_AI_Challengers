from __future__ import annotations

from typing import List

from .models import Document, RetrievalResult


def simple_retriever(query: str) -> RetrievalResult:
    # Return two simple documents containing the query for deterministic tests
    docs: List[Document] = [
        Document(id="d1", content=f"{query} result one"),
        Document(id="d2", content=f"{query} result two"),
    ]
    return RetrievalResult(documents=docs)
