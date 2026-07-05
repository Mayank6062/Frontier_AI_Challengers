from __future__ import annotations

import asyncio

from backend.knowledge.ingestion_pipeline.embedder import DummyEmbedder


def test_embedder_deterministic() -> None:
    e = DummyEmbedder(dimension=4)
    v1 = asyncio.get_event_loop().run_until_complete(e.embed("abc"))
    v2 = asyncio.get_event_loop().run_until_complete(e.embed("abc"))
    assert v1 == v2
