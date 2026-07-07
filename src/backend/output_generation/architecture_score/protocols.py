from __future__ import annotations

from typing import Protocol, runtime_checkable, Optional, Dict

from .models import (
    ArchitectureScore,
    ArchitectureScoreInput,
    ArchitectureScoreResult,
    ArchitectureScoreGenerationRequest,
    ArchitectureScoreGenerationResponse,
)


@runtime_checkable
class ArchitectureScoreEngine(Protocol):
    def score(
        self, inp: ArchitectureScoreInput
    ) -> ArchitectureScoreResult:  # pragma: no cover - protocol
        ...


@runtime_checkable
class ArchitectureScoreGenerator(Protocol):
    def generate(
        self, req: ArchitectureScoreGenerationRequest
    ) -> ArchitectureScoreGenerationResponse:  # pragma: no cover - protocol
        ...


@runtime_checkable
class ScoreRenderer(Protocol):
    def render(
        self,
        score: ArchitectureScore,
        mode: Optional[str] = None,
        extras: Optional[Dict[str, object]] = None,
    ) -> str:  # pragma: no cover - protocol
        ...


@runtime_checkable
class ScoreRegistry(Protocol):
    def register(self, score: ArchitectureScore) -> str:  # pragma: no cover - protocol
        ...


@runtime_checkable
class ScoreManifestBuilder(Protocol):
    def build_manifest(
        self, score: ArchitectureScore
    ) -> Dict[str, object]:  # pragma: no cover - protocol
        ...


@runtime_checkable
class ScoreExporter(Protocol):
    def export(
        self, score: ArchitectureScore, format: Optional[str] = None
    ) -> bytes:  # pragma: no cover - protocol
        ...


@runtime_checkable
class ScoreProvider(Protocol):
    def provide(
        self, engagement_id: str
    ) -> Optional[ArchitectureScore]:  # pragma: no cover - protocol
        ...
