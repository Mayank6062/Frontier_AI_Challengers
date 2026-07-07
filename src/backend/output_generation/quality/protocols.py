from __future__ import annotations

from typing import Protocol, Sequence, Dict, Optional
from uuid import UUID

from .contracts import (
    QualityGenerationRequest,
    QualityGenerationResponse,
    QualityContext,
)


class QualityEngine(Protocol):
    def run(self, request: QualityGenerationRequest) -> QualityGenerationResponse: ...


class QualityGate(Protocol):
    def evaluate(self, bundle: object) -> Sequence[str]: ...


class QualityValidator(Protocol):
    def validate(self, bundle: object) -> object: ...


class CompletenessValidator(Protocol):
    def validate(self, bundle: object) -> object: ...


class SemanticValidator(Protocol):
    def validate(self, bundle: object) -> object: ...


class CitationValidator(Protocol):
    def validate(self, bundle: object) -> object: ...


class DeterminismValidator(Protocol):
    def validate(self, bundle: object) -> object: ...


class AccessibilityValidator(Protocol):
    def validate(self, bundle: object) -> object: ...


class SecurityValidator(Protocol):
    def validate(self, bundle: object) -> object: ...


class PerformanceValidator(Protocol):
    def validate(self, bundle: object) -> object: ...


class ArchitectureScorer(Protocol):
    def score(self, bundle: object) -> object: ...


class QualityRegistry(Protocol):
    def register(self, name: str, entry: object) -> None: ...


class QualityManifestBuilder(Protocol):
    def build(self) -> UUID: ...


class QualityDefinitionProvider(Protocol):
    def provide(self) -> object: ...


class QualityStatisticsProvider(Protocol):
    def collect(self) -> Dict[str, object]: ...


class QualityRecommendationProvider(Protocol):
    def recommend(self, report: object) -> Sequence[str]: ...


class QualityAuditProvider(Protocol):
    def record(self, entry: object) -> None: ...


class QualityReporter(Protocol):
    def report(self, result: object) -> None: ...


class QualitySummaryProvider(Protocol):
    def summarize(self, report: object) -> object: ...


class QualityBundleValidator(Protocol):
    def validate(self, bundle: object) -> bool: ...


class QualityGateOrchestrator(Protocol):
    """Orchestrates quality gates and validators for a generation request.

    Protocol-only: no implementation here. Signatures only, no logic.
    """

    def orchestrate(
        self,
        request: QualityGenerationRequest,
        context: Optional[QualityContext] = None,
    ) -> QualityGenerationResponse: ...
