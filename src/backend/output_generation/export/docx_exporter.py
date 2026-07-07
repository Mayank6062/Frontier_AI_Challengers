from __future__ import annotations

from .base_exporter import BaseExporter


class DocxExporter(BaseExporter):
    """Export a payload as a deterministic placeholder DOCX byte stream."""

    def export(self, payload: object) -> bytes:
        return b"PK\x03\x04\x14\x00\x00\x00\x08\x00" + super().export(payload)
