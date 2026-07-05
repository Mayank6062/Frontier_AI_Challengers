from __future__ import annotations

from backend.knowledge.rag_engine.structured_filter import apply_metadata_filter
from backend.knowledge.knowledge_base.entry_model import EntryModel


def test_filter_by_metadata() -> None:
    entries = [
        EntryModel(id="1", text="a", metadata={"type": "doc"}),
        EntryModel(id="2", text="b", metadata={}),
    ]
    out = apply_metadata_filter(entries, {"type": "doc"})
    assert len(out) == 1
