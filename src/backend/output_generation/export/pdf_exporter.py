from __future__ import annotations

from .base_exporter import BaseExporter


class PdfExporter(BaseExporter):
    """Export a payload as a deterministic placeholder PDF byte stream."""

    def export(self, payload: object) -> bytes:
        return b"%PDF-1.4\n% placeholder pdf\n" + super().export(payload)
