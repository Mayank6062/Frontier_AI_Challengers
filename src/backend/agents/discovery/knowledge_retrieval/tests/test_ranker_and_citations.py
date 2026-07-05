from __future__ import annotations

from backend.agents.discovery.knowledge_retrieval.ranker import length_ranker
from backend.agents.discovery.knowledge_retrieval.citation_builder import (
    build_citations,
)
from backend.agents.discovery.knowledge_retrieval.models import Document


def test_ranker_and_citations() -> None:
    docs = [
        Document(id="1", content="short"),
        Document(id="2", content="a much longer content"),
    ]
    ranked = length_ranker(docs)
    assert ranked[0].id == "2"
    cites = build_citations(ranked)
    assert len(cites) == 2
