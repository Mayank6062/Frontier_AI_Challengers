from __future__ import annotations

from typing import Protocol, Sequence, Dict
from uuid import UUID

from .models import (
    NarrativeAgentInput,
    NarrativeResult,
    NarrativeValidationSummary,
    NarrativeManifestReference,
    NarrativeContext,
    NarrativeStatistics,
    CitationReference,
)


class NarrativeAgent(Protocol):
    def generate(self, inp: NarrativeAgentInput) -> NarrativeResult:
        """Produce a narrative result from input."""


class NarrativeValidator(Protocol):
    def validate(self, result: NarrativeResult) -> NarrativeValidationSummary:
        """Validate a narrative result and return a summary."""


class NarrativeRegistry(Protocol):
    def register(self, manifest_ref: NarrativeManifestReference) -> UUID:
        """Register a narrative manifest and return an id."""


class NarrativeManifestBuilder(Protocol):
    def build(self, reference: NarrativeManifestReference) -> Dict[str, object]:
        """Build a manifest representation for serialization."""


class NarrativeQualityChecker(Protocol):
    def check(self, result: NarrativeResult) -> NarrativeValidationSummary:
        """Run quality checks and return a validation summary."""


class NarrativeCitationResolver(Protocol):
    def resolve(
        self, citations: Sequence[CitationReference]
    ) -> Sequence[CitationReference]:
        """Resolve citations to canonical forms."""


class NarrativeContextProvider(Protocol):
    def provide(self, context: NarrativeContext) -> NarrativeContext:
        """Enrich or resolve context used for generation."""


class NarrativeSerializer(Protocol):
    def serialize(self, result: NarrativeResult) -> str:
        """Serialize a narrative result to a string or document."""


class NarrativeMetricsCollector(Protocol):
    def collect(self, stats: NarrativeStatistics) -> None:
        """Collect metrics for reporting (protocol-only)."""
