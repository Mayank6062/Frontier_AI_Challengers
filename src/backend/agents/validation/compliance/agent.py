from __future__ import annotations

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .framework_evaluator import evaluate_frameworks
from .control_checker import check_controls
from .residency_validator import validate_residency


class ComplianceAgent(BaseAgent):
    AGENT_ID = "compliance"
    AGENT_NAME = "Compliance"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        try:
            frameworks = evaluate_frameworks(context.metadata)
            controls_ok = check_controls(context.metadata)
            residency = validate_residency(context.metadata)
            return AgentResult.success_result(
                payload={
                    "frameworks": frameworks,
                    "controls": controls_ok,
                    "residency": residency,
                },
                confidence=0.8,
                citations=["knowledge:compliance#baseline"],
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR", "compliance.failure", {"error": str(exc)}
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(ComplianceAgent.AGENT_ID, lambda: ComplianceAgent())
