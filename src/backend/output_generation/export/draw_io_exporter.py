from __future__ import annotations

from .base_exporter import BaseExporter


class DrawIoExporter(BaseExporter):
    """Export a payload as a deterministic draw.io XML document."""

    def export(self, payload: object) -> bytes:
        content = self._coerce_text(payload)
        xml = (
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            "<mxfile host=\"app.diagrams.net\" modified=\"2024-01-01T00:00:00.000Z\">\n"
            f"<diagram>{content}</diagram>\n"
            "</mxfile>\n"
        )
        return xml.encode("utf-8")
