from __future__ import annotations

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .risk_aggregator import aggregate_risks
from .risk_scorer import score_risks
from .mitigation_advisor import recommend_mitigations


class RiskAssessmentAgent(BaseAgent):
    AGENT_ID = "risk_assessment"
    AGENT_NAME = "Risk Assessment"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        try:
            agg = aggregate_risks(context.metadata)
            scored = score_risks(agg)
            mitigations = recommend_mitigations(scored)
            return AgentResult.success_result(
                payload={
                    "aggregated": agg,
                    "scored": scored,
                    "mitigations": mitigations,
                },
                confidence=0.77,
                citations=["knowledge:risk#v1"],
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR", "risk_assessment.failure", {"error": str(exc)}
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(RiskAssessmentAgent.AGENT_ID, lambda: RiskAssessmentAgent())
