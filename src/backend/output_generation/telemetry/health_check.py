"""Health check service for output generation telemetry and runtime wiring."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Any


@dataclass(slots=True, frozen=True)
class HealthStatus:
    """Health check response model."""

    ok: bool
    latency_ms: float
    checks: dict[str, bool]


class HealthCheckService:
    """Evaluate core runtime dependencies for operational readiness."""

    def __init__(self, dependencies: dict[str, Any] | None = None) -> None:
        self._dependencies = {} if dependencies is None else dict(dependencies)

    def run_check(self) -> dict[str, Any]:
        """Run health checks and return serializable status payload."""

        start = perf_counter()
        checks: dict[str, bool] = {}
        for name, dependency in self._dependencies.items():
            checks[name] = dependency is not None

        latency_ms = (perf_counter() - start) * 1000.0
        ok = all(checks.values()) if checks else True
        status = HealthStatus(ok=ok, latency_ms=latency_ms, checks=checks)
        return {
            "ok": status.ok,
            "latency_ms": status.latency_ms,
            "checks": status.checks,
        }
