"""Dependency injection container for Chapter 18 output-generation runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.di.composition import DIContainer as AppDIContainer

from ..orchestration.generation_event_handlers import GenerationEventHandlers
from ..orchestration.generation_orchestrator import (
    GenerationOrchestrator,
    GenerationOrchestratorConfig,
)
from ..orchestration.telemetry import OrchestrationTelemetry
from ..telemetry.health_check import HealthCheckService
from ..telemetry.metrics import MetricsCollector
from ..telemetry.structured_logging import StructuredLogger
from ..telemetry.tracing import TracingService
from .settings import OutputGenerationSettings


@dataclass(slots=True, frozen=True)
class OutputGenerationProviders:
    """Resolved output-generation dependencies."""

    settings: OutputGenerationSettings
    app: Any
    metrics: MetricsCollector
    tracer: TracingService
    logger: StructuredLogger
    health: HealthCheckService
    orchestration_telemetry: OrchestrationTelemetry
    event_handlers: GenerationEventHandlers
    orchestrator: GenerationOrchestrator


class OutputGenerationContainer:
    """Singleton/factory DI container for orchestration, telemetry, and config."""

    def __init__(
        self,
        settings: OutputGenerationSettings | None = None,
        app_di: AppDIContainer | None = None,
    ) -> None:
        self._settings = settings or OutputGenerationSettings.from_env()
        self._app_di = app_di or AppDIContainer()
        self._singletons: dict[str, Any] = {}
        self._stage_factories: dict[str, Any] = {}

    def register_stage_factory(self, stage: str, factory: Any) -> None:
        """Register a stage factory callable used by the orchestrator."""

        self._stage_factories[stage] = factory

    def build(self) -> OutputGenerationProviders:
        """Build and return all core output-generation providers."""

        app = self._app_di.build()
        metrics = self._resolve_singleton("metrics", lambda: MetricsCollector())
        tracer = self._resolve_singleton("tracer", lambda: TracingService())
        logger = self._resolve_singleton(
            "logger",
            lambda: StructuredLogger(self._settings.telemetry.logger_name),
        )
        health = self._resolve_singleton(
            "health",
            lambda: HealthCheckService(
                dependencies={
                    "app_storage": getattr(app, "storage", None),
                    "app_bundle_assembler": getattr(app, "bundle_assembler", None),
                    "metrics": metrics,
                    "tracer": tracer,
                    "logger": logger,
                }
            ),
        )
        orchestration_telemetry = OrchestrationTelemetry(
            metrics=metrics,
            tracer=tracer,
            logger=logger,
            health=health,
        )
        event_handlers = GenerationEventHandlers(orchestration_telemetry)
        orchestrator = GenerationOrchestrator(
            telemetry=orchestration_telemetry,
            event_handlers=event_handlers,
            stage_executors=self._build_stage_executors(),
            config=GenerationOrchestratorConfig(
                retry_attempts=self._settings.retry.attempts,
                retry_backoff_seconds=self._settings.retry.backoff_seconds,
            ),
        )
        return OutputGenerationProviders(
            settings=self._settings,
            app=app,
            metrics=metrics,
            tracer=tracer,
            logger=logger,
            health=health,
            orchestration_telemetry=orchestration_telemetry,
            event_handlers=event_handlers,
            orchestrator=orchestrator,
        )

    def _build_stage_executors(self) -> dict[str, Any]:
        """Build stage executors from registered factories."""

        return {
            stage: factory() if callable(factory) else factory
            for stage, factory in self._stage_factories.items()
        }

    def _resolve_singleton(self, key: str, builder: Any) -> Any:
        """Resolve singleton value from cache or create lazily."""

        existing = self._singletons.get(key)
        if existing is not None:
            return existing
        created = builder()
        self._singletons[key] = created
        return created


class OutputDI:
    """Backward-compatible wrapper over Chapter 18 container build output."""

    @dataclass(slots=True, frozen=True)
    class Provided:
        bundle_assembler: object | None
        storage: object | None
        logger: object
        metrics: MetricsCollector

    def __init__(self, initial_secrets: dict[str, str] | None = None) -> None:
        self._app_di = AppDIContainer(initial_secrets)
        self._container = OutputGenerationContainer(app_di=self._app_di)

    def build(self) -> "OutputDI.Provided":
        providers = self._container.build()
        app = providers.app
        return OutputDI.Provided(
            bundle_assembler=getattr(app, "bundle_assembler", None),
            storage=getattr(app, "storage", None),
            logger=providers.logger,
            metrics=providers.metrics,
        )


__all__ = ["OutputDI", "OutputGenerationContainer", "OutputGenerationProviders"]
