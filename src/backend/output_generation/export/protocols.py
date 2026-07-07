from __future__ import annotations

from typing import Protocol, Sequence
from uuid import UUID

from .contracts import (
    ExportGenerationRequest,
    ExportGenerationResponse,
)


class ExportGenerationEngine(Protocol):
    def generate(
        self, request: ExportGenerationRequest
    ) -> ExportGenerationResponse: ...


class PdfConverter(Protocol):
    def convert(self, source: bytes) -> bytes: ...


class DocxConverter(Protocol):
    def convert(self, source: bytes) -> bytes: ...


class PptxGenerator(Protocol):
    def generate(self, slides: Sequence[bytes]) -> bytes: ...


class DrawioXmlGenerator(Protocol):
    def generate(self, diagram_xml: str) -> bytes: ...


class YamlExporter(Protocol):
    def dump(self, data: object) -> str: ...


class CsvExporter(Protocol):
    def dump(self, rows: Sequence[Sequence[str]]) -> str: ...


class ExportValidator(Protocol):
    def validate(self, data: bytes) -> bool: ...


class ExportRegistry(Protocol):
    def register(self, name: str, handler: object) -> None: ...


class ExportManifestBuilder(Protocol):
    def build(self) -> UUID: ...


class ExportSanitizer(Protocol):
    def sanitize(self, data: bytes) -> bytes: ...


class ExportFeatureFlagResolver(Protocol):
    def is_enabled(self, flag: str) -> bool: ...


class ExportPipeline(Protocol):
    def run(self) -> None: ...


class ExportMetricsCollector(Protocol):
    def collect(self, name: str, value: float) -> None: ...
