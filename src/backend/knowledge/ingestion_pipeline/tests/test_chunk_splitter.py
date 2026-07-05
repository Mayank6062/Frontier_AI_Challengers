from __future__ import annotations

from backend.knowledge.ingestion_pipeline.chunk_splitter import simple_chunk_splitter


def test_chunk_splitter_limits() -> None:
    text = "word " * 100
    chunks = simple_chunk_splitter(text, max_size=50)
    assert all(len(c) <= 50 for c in chunks)
