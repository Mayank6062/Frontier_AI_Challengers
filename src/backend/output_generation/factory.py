"""OutputGeneratorFactory per Chapter 18.

This factory holds a registry of generators keyed by stage name. It is
configured at startup via DI and returns concrete generator instances.
"""

from __future__ import annotations

from typing import Dict, Any
from .interfaces import OutputFormatGenerator


class OutputGeneratorFactory:
    """Factory for resolving generators by canonical name.

    The factory takes an optional configuration dict describing which
    generators to enable. Generators may be registered dynamically.
    """

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self._config = config or {}
        self._registry: Dict[str, OutputFormatGenerator] = {}

    def register(self, name: str, generator: OutputFormatGenerator) -> None:
        self._registry[name] = generator

    def get_generator(self, name: str) -> OutputFormatGenerator:
        gen = self._registry.get(name)
        if gen is None:
            raise KeyError(f"generator not registered: {name}")
        return gen

    def list_generators(self) -> list[str]:
        return list(self._registry.keys())


__all__ = ["OutputGeneratorFactory"]
from __future__ import annotations

from backend.di.composition import DIContainer
from .service import OutputGeneratorServiceImpl
from .telemetry import get_metrics


class OutputGeneratorFactory:
    """Factory responsible for creating `OutputGeneratorService` instances.

    The factory wires the service from DI-provided infra implementations to
    avoid duplicating composition logic found elsewhere in the repo.
    """

    def __init__(self, di: DIContainer.Provided | None = None) -> None:
        self._di = di or DIContainer().build()

    def create_service(self) -> OutputGeneratorServiceImpl:
        metrics = get_metrics()
        # Use DI-provided bundle_assembler when available
        bundle_assembler = getattr(self._di, "bundle_assembler", None)
        storage = getattr(self._di, "storage", None)
        logger = getattr(self._di, "logger", None)

        service = OutputGeneratorServiceImpl(
            storage=storage,
            bundle_assembler=bundle_assembler,
            metrics=metrics,
            logger=logger,
        )
        return service


__all__ = ["OutputGeneratorFactory"]
