"""
Output Storage Interface Contract.

Defines the abstraction for all output artifact storage operations. Generated
architecture artifacts (Markdown, HTML, Mermaid, Graphviz, JSON) are stored
through this interface. The storage location and mechanism are infrastructure
concerns — consuming modules only interact with this interface.

Authority:
    BACKEND_MODULE_ARCHITECTURE.md Section 4.6 (interfaces module responsibilities)
    BACKEND_MODULE_ARCHITECTURE.md Section 4.11 (output_packager module)
    BACKEND_MODULE_ARCHITECTURE.md Section 8 (OutputRepository)
    SYSTEM_ARCHITECTURE.md Section 4.11 (Output Generator)

Implementors:
    src/backend/infrastructure/output_storage_service.py

Consumers:
    src/backend/output/ (all format generators)
    src/backend/output/output_packager/ (bundle assembly)
    src/backend/core/ (output bundle reference recording)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Output storage models (interface-local DTOs)
# ---------------------------------------------------------------------------


class OutputFormat(str, Enum):
    """
    Supported output artifact formats.

    Authority: IMPLEMENTATION_SPECIFICATION.md Section 7.2 (MVP In Scope)
    """

    MARKDOWN_HLD = "markdown_hld"
    MARKDOWN_LLD = "markdown_lld"
    MARKDOWN_EXECUTIVE_SUMMARY = "markdown_executive_summary"
    MARKDOWN_RISK_REGISTER = "markdown_risk_register"
    MARKDOWN_ASSUMPTIONS_LOG = "markdown_assumptions_log"
    HTML_REPORT = "html_report"
    MERMAID_DIAGRAM = "mermaid_diagram"
    GRAPHVIZ_DOT = "graphviz_dot"
    SVG_DIAGRAM = "svg_diagram"
    PNG_DIAGRAM = "png_diagram"
    JSON_ARCHITECTURE_STATE = "json_architecture_state"


@dataclass(frozen=True)
class OutputArtifact:
    """
    A single generated output artifact.

    Attributes:
        artifact_id: Unique identifier for this artifact.
        engagement_id: The engagement this artifact belongs to.
        output_version: Output version number (incremented per approval).
        output_format: The format of this artifact.
        storage_path: The implementation-specific path to the stored artifact.
        content_hash: SHA-256 hash of the artifact content for integrity.
        size_bytes: Size of the stored artifact in bytes.
        template_version: The template version used to generate this artifact.
        generated_at_utc: ISO 8601 UTC generation timestamp.
    """

    artifact_id: str
    engagement_id: str
    output_version: int
    output_format: OutputFormat
    storage_path: str
    content_hash: str
    size_bytes: int
    template_version: str
    generated_at_utc: str


@dataclass(frozen=True)
class OutputBundle:
    """
    A versioned collection of all output artifacts for an engagement approval.

    Attributes:
        bundle_id: Unique identifier for this output bundle.
        engagement_id: The engagement this bundle belongs to.
        output_version: Bundle version number (incremented per approval).
        artifacts: List of all artifacts in this bundle.
        manifest_hash: SHA-256 hash of the complete bundle manifest.
        assembled_at_utc: ISO 8601 UTC assembly timestamp.
        metadata: Additional bundle metadata.
    """

    bundle_id: str
    engagement_id: str
    output_version: int
    artifacts: list[OutputArtifact]
    manifest_hash: str
    assembled_at_utc: str
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Interface contract
# ---------------------------------------------------------------------------


class OutputStorageInterface(ABC):
    """
    Abstract contract for output artifact storage.

    Manages the storage and retrieval of generated architecture output
    artifacts. Each output generation run creates a versioned bundle
    associated with an engagement approval event.

    Contract invariants:
        - save_artifact() must confirm durable write before returning.
        - get_artifact() returns None for a non-existent artifact_id.
        - save_bundle() stores the complete bundle manifest.
        - Artifacts are never deleted — they are versioned and retained.
        - list_bundles() returns bundles in descending version order (newest first).

    Raises:
        OutputStorageWriteError: On write failure after retry exhaustion.
        OutputStorageReadError: On read failure.
        OutputStorageConnectionError: When the storage backend is unavailable.
    """

    @abstractmethod
    async def save_artifact(
        self,
        engagement_id: str,
        output_version: int,
        output_format: OutputFormat,
        content: bytes,
        template_version: str,
    ) -> OutputArtifact:
        """
        Store a single generated output artifact.

        Args:
            engagement_id: The engagement this artifact belongs to.
            output_version: The output version number for this generation run.
            output_format: The format of the artifact being stored.
            content: The artifact content as bytes.
            template_version: The template version used to generate this artifact.

        Returns:
            OutputArtifact: The stored artifact record with path and hash.

        Raises:
            OutputStorageWriteError: On storage backend failure.
        """

    @abstractmethod
    async def get_artifact(self, artifact_id: str) -> bytes | None:
        """
        Retrieve the raw content of a stored artifact.

        Args:
            artifact_id: The unique artifact identifier.

        Returns:
            bytes: The artifact content if found, None if not found.

        Raises:
            OutputStorageReadError: On storage backend failure.
        """

    @abstractmethod
    async def save_bundle(self, bundle: OutputBundle) -> OutputBundle:
        """
        Store the output bundle manifest for an engagement version.

        Args:
            bundle: The complete output bundle with all artifact references.

        Returns:
            OutputBundle: The stored bundle record.

        Raises:
            OutputStorageWriteError: On storage backend failure.
        """

    @abstractmethod
    async def get_bundle(
        self, engagement_id: str, output_version: int
    ) -> OutputBundle | None:
        """
        Retrieve the output bundle manifest for a specific version.

        Args:
            engagement_id: The engagement to retrieve the bundle for.
            output_version: The specific output version to retrieve.

        Returns:
            OutputBundle: The bundle if found, None if not found.

        Raises:
            OutputStorageReadError: On storage backend failure.
        """

    @abstractmethod
    async def list_bundles(
        self, engagement_id: str
    ) -> list[OutputBundle]:
        """
        List all output bundles for an engagement.

        Returns bundles in descending version order (most recent first).

        Args:
            engagement_id: The engagement to list bundles for.

        Returns:
            list[OutputBundle]: All output bundles, newest first.

        Raises:
            OutputStorageReadError: On storage backend failure.
        """

    @abstractmethod
    async def check_health(self) -> bool:
        """
        Check whether the output storage backend is currently operational.

        Returns:
            bool: True if the backend is reachable and writable, False otherwise.
        """
