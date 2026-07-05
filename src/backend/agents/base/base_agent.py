from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Optional

from ...core.interfaces.agent_interface import AgentInterface
from .agent_context import AgentContext
from .agent_result import AgentResult
from ...core.interfaces.observability_interface import ObservabilityInterface
from .agent_validator import AgentValidator, ValidationResult


class BaseAgent(AgentInterface, ABC):
    """Abstract base agent providing standardized lifecycle, logging, metrics,
    tracing hooks, and exception handling. Concrete agents implement `execute_impl`.

    All dependencies must be constructor-injected.
    """

    AGENT_ID: str = "BASE"
    AGENT_VERSION: str = "0.0"
    AGENT_CATEGORY = None
    AGENT_NAME: str = "BaseAgent"

    def __init__(
        self,
        observability: Optional[ObservabilityInterface] = None,
        validator: Optional[AgentValidator] = None,
    ) -> None:
        self._observability = observability
        self._validator = validator

    async def execute(self, context: AgentContext) -> AgentResult:
        start = time.perf_counter()
        trace_id = context.correlation_id or context.execution_id
        try:
            await self.before_execute(context)
            result = await self.execute_impl(context)
            await self.after_execute(context, result)
        except Exception as exc:  # noqa: BLE001 - convert to AgentResult
            if self._observability:
                self._observability.emit_log(
                    "ERROR",
                    "Agent exception",
                    {"error": str(exc), "agent": self.AGENT_NAME, "trace_id": trace_id},
                )
            result = AgentResult.internal_error(
                str(exc), agent_name=self.AGENT_NAME, trace_id=trace_id
            )
            await self.on_exception(context, exc, result)

        end = time.perf_counter()
        exec_ms = (end - start) * 1000.0
        # populate execution time immutably by creating a new model
        result = result.copy(
            update={
                "execution_time_ms": exec_ms,
                "agent_name": self.AGENT_NAME,
                "trace_id": trace_id,
            }
        )

        # metrics hooks
        if self._observability:
            try:
                self._observability.emit_metric(
                    "agent.execution.duration_ms", exec_ms, {"agent": self.AGENT_NAME}
                )
                self._observability.emit_metric(
                    "agent.execution.count", 1.0, {"agent": self.AGENT_NAME}
                )
                if result.success:
                    self._observability.emit_metric(
                        "agent.execution.success", 1.0, {"agent": self.AGENT_NAME}
                    )
                else:
                    self._observability.emit_metric(
                        "agent.execution.failure", 1.0, {"agent": self.AGENT_NAME}
                    )
            except Exception:
                # Observability implementations must not break agent execution
                pass

        # optional validation
        if self._validator:
            try:
                validation: ValidationResult = self._validator.validate(result)
                if not validation.passed:
                    # attach validator warnings
                    warnings = list(result.warnings) + validation.warnings
                    result = result.copy(update={"warnings": warnings})
            except Exception:
                # validator failures should not break execution
                pass

        await self.cleanup(context)
        return result

    async def before_execute(self, context: AgentContext) -> None:
        if self._observability:
            self._observability.emit_log(
                "INFO",
                "before_execute",
                {"agent": self.AGENT_NAME, "execution_id": context.execution_id},
            )

    @abstractmethod
    async def execute_impl(self, context: AgentContext) -> AgentResult:
        """Concrete agents implement this method with business-agnostic logic."""

    async def after_execute(self, context: AgentContext, result: AgentResult) -> None:
        if self._observability:
            self._observability.emit_log(
                "INFO",
                "after_execute",
                {"agent": self.AGENT_NAME, "success": result.success},
            )

    async def on_exception(
        self, context: AgentContext, exc: Exception, result: AgentResult
    ) -> None:
        if self._observability:
            self._observability.emit_log(
                "ERROR", "on_exception", {"agent": self.AGENT_NAME, "error": str(exc)}
            )

    async def cleanup(self, context: AgentContext) -> None:
        if self._observability:
            self._observability.emit_log("DEBUG", "cleanup", {"agent": self.AGENT_NAME})
