"""Public interface contracts for format generators, renderers, and storage.

These interfaces mirror Chapter 18 §18.5 and are frozen by the Bible.
Do not change method signatures without ADR (FR-IFACE-01).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from .schemas import FormatGenerationResult, GenerationContext


class OutputFormatGenerator(ABC):
    """Base contract for all format generators.

    Generators are deterministic and perform no external network I/O.
    """

    @abstractmethod
    async def generate(self, context: GenerationContext) -> FormatGenerationResult:
        """Generate format artifacts from approved snapshot."""

    @abstractmethod
    def get_output_file_type(self) -> str:
        """File type identifier (e.g. 'text/markdown', 'text/html')."""

    @abstractmethod
    def get_generator_version(self) -> str:
        """Semver string of this generator implementation."""

    @abstractmethod
    def is_optional(self) -> bool:
        """If True, failures are WARN; otherwise BLOCKER."""


class DiagramRenderer(ABC):
    """Contract for diagram renderers (SVG/PNG)."""

    @abstractmethod
    async def render(self, definition, theme: str, output_format: str):
        """Render a diagram definition to a render result object."""


class QualityValidator(ABC):
    """Contract for quality gate validators."""

    @abstractmethod
    async def validate(self, bundle_content: dict, approved_snapshot: dict):
        """Return validation result object."""

    @abstractmethod
    def get_validator_name(self) -> str:
        ...

    @abstractmethod
    def get_severity_on_failure(self) -> str:
        """Returns BLOCKER | ERROR | WARN | INFO"""


class OutputStorageService(ABC):
    """Contract for all storage backends used by output generation."""

    @abstractmethod
    async def write(self, path: str, content: bytes, metadata: dict | None = None) -> str:
        """Write bytes and return a storage reference (e.g. URL or key)."""

    @abstractmethod
    async def read(self, path: str) -> bytes:
        ...

    @abstractmethod
    async def exists(self, path: str) -> bool:
        ...

    @abstractmethod
    async def delete(self, path: str) -> None:
        ...

    @abstractmethod
    async def list_prefix(self, prefix: str) -> list[str]:
        ...

    @abstractmethod
    async def make_immutable(self, path: str) -> None:
        """Mark path as read-only. Called after BUNDLE_COMPLETE."""


__all__ = [
    "OutputFormatGenerator",
    "DiagramRenderer",
    "QualityValidator",
    "OutputStorageService",
]
from __future__ import annotations

from typing import Any, Iterable, Mapping, Protocol

# Re-export canonical protocol definitions where appropriate to avoid
# duplicate definitions across the package. Canonical generation and
# manifest protocols live in `contracts.py`.

from pydantic import BaseModel

# Re-export canonical VisualizationEngine Protocol from the visualization
# package to avoid duplicate protocol definitions across the output_generation
# package.


class DocumentationEngine(Protocol):
    def render_document(self, sections: Iterable[BaseModel]) -> str:
        """Render documentation content as a string."""


class ExportEngine(Protocol):
    def export(self, bundle: BaseModel, fmt: str) -> bytes:
        """Export a bundle to a target format (e.g., zip, tar, pdf)."""


class BundleEngine(Protocol):
    def assemble(self, manifest: BaseModel) -> BaseModel:
        """Assemble a bundle manifest into an in-memory bundle representation."""


class TemplateResolver(Protocol):
    def resolve(self, template_name: str, context: Mapping[str, Any]) -> str:
        """Resolve a template by name with provided context and return rendered string."""


class SanitizerInterface(Protocol):
    def sanitize(self, content: str) -> str:
        """Sanitize content for safe inclusion in outputs."""


class OutputStorageInterface(Protocol):
    def save(self, path: str, data: bytes) -> str:
        """Persist bytes to storage and return a stable reference/URI."""

    def retrieve(self, reference: str) -> bytes:
        """Retrieve persisted bytes by reference."""
