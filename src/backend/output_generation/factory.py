"""OutputGeneratorFactory per Chapter 18.

This factory holds a registry of generators keyed by stage name and provides
both a simple registry interface and a DI-based factory interface.
"""

from __future__ import annotations

from typing import Any, Dict

from backend.di.composition import DIContainer

from .interfaces import OutputFormatGenerator
from .service import OutputGeneratorServiceImpl
from .telemetry import get_metrics


class OutputGeneratorFactory:
    """Factory for resolving generators by canonical name.

    The factory takes an optional configuration dict describing which
    generators to enable and supports both registry-based lookup and
    DI-based service creation.
    """

    def __init__(self, config: Dict[str, Any] | None = None, di: DIContainer.Provided | None = None) -> None:
        self._config = config or {}
        self._registry: Dict[str, OutputFormatGenerator] = {}
        self._di = di or DIContainer().build()

    def register(self, name: str, generator: OutputFormatGenerator) -> None:
        """Register a generator by stage name."""
        self._registry[name] = generator

    def get_generator(self, name: str) -> OutputFormatGenerator:
        """Get a registered generator by stage name."""
        gen = self._registry.get(name)
        if gen is None:
            raise KeyError(f"generator not registered: {name}")
        return gen

    def list_generators(self) -> list[str]:
        """List all registered generator names."""
        return list(self._registry.keys())

    def create_service(self) -> OutputGeneratorServiceImpl:
        """Create a new OutputGeneratorService instance using DI-provided components."""
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
