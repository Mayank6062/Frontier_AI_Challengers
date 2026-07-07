from __future__ import annotations

from typing import Optional

from backend.di.composition import DIContainer as AppDI
from backend.infrastructure.observability.metrics import Metrics


class OutputDI:
    """Lightweight DI wrapper exposing output-generation scoped providers.

    This wraps the application-level DI container and surfaces only the
    providers used by output_generation consumers to keep coupling low.
    """

    class Provided:
        def __init__(
            self,
            bundle_assembler: object,
            storage: object,
            logger: object,
            metrics: Metrics,
        ) -> None:
            self.bundle_assembler = bundle_assembler
            self.storage = storage
            self.logger = logger
            self.metrics = metrics

    def __init__(self, initial_secrets: Optional[dict[str, str]] = None) -> None:
        self._app_di = AppDI(initial_secrets)

    def build(self) -> Provided:
        provided = self._app_di.build()
        # Reuse app-level bundle_assembler if present; else None
        bundle_assembler = getattr(provided, "bundle_assembler", None)
        return OutputDI.Provided(
            bundle_assembler=bundle_assembler,
            storage=provided.storage,
            logger=provided.logger,
            metrics=provided.metrics,
        )


__all__ = ["OutputDI"]
