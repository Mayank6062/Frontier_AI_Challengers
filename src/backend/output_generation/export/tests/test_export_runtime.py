from __future__ import annotations

from .. import (
    BaseExporter,
    DocxExporter,
    DrawIoExporter,
    PdfExporter,
    PptxExporter,
    YamlExporter,
)


def test_base_exporter_coerces_text() -> None:
    exporter = BaseExporter()
    assert exporter.export("hello").decode("utf-8") == "hello"


def test_exporters_emit_expected_prefixes() -> None:
    assert PdfExporter().export("hello").startswith(b"%PDF")
    assert DocxExporter().export("hello").startswith(b"PK")
    assert PptxExporter().export("hello").startswith(b"PK")
    assert DrawIoExporter().export("hello").decode("utf-8").startswith("<?xml")
    assert YamlExporter().export("hello").decode("utf-8") == "content: hello\n"
