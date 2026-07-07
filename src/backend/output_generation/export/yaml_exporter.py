from __future__ import annotations

from .base_exporter import BaseExporter


class YamlExporter(BaseExporter):
    """Export a payload as a deterministic YAML-like text document."""

    def export(self, payload: object) -> bytes:
        content = self._coerce_text(payload)
        return f"content: {content}\n".encode("utf-8")
