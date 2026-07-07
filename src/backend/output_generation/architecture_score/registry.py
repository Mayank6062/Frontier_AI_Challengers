from __future__ import annotations

from typing import Protocol, runtime_checkable

from .models import ArchitectureScore


@runtime_checkable
class ArchitectureScoreRegistry(Protocol):
    def register(self, score: ArchitectureScore) -> str:  # pragma: no cover - protocol
        ...
