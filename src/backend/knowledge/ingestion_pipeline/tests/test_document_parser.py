from __future__ import annotations

from backend.knowledge.ingestion_pipeline.document_parser import simple_document_parser


def test_document_parser_splits() -> None:
    raw = "first---second---"
    parts = simple_document_parser(raw)
    assert parts == ["first", "second"]
