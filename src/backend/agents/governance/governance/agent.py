from __future__ import annotations

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .policy_enforcer import enforce_policies
from .guardrail_checker import check_guardrails
from .catalog_validator import validate_catalog


class GovernanceAgent(BaseAgent):
    AGENT_ID = "governance"
    AGENT_NAME = "Governance"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        try:
            policies = enforce_policies(context.metadata)
            guardrails = check_guardrails(context.metadata)
            catalog = validate_catalog(context.metadata)
            return AgentResult.success_result(
                payload={
                    "policies": policies,
                    "guardrails": guardrails,
                    "catalog": catalog,
                },
                confidence=0.86,
                citations=["knowledge:governance#v1"],
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR", "governance.failure", {"error": str(exc)}
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(GovernanceAgent.AGENT_ID, lambda: GovernanceAgent())
