from __future__ import annotations

from backend.agents.discovery.knowledge_retrieval.retriever import simple_retriever


def test_simple_retriever() -> None:
    r = simple_retriever("query")
    assert len(r.documents) == 2
    assert r.documents[0].content.endswith("result one")
