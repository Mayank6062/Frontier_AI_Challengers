from __future__ import annotations

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .tco_modeler import model_tco
from .cost_estimator import estimate_costs
from .optimization_advisor import advise_optimizations


class CostOptimizationAgent(BaseAgent):
    AGENT_ID = "cost_optimization"
    AGENT_NAME = "Cost Optimization"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        try:
            tco = model_tco(context.metadata)
            estimates = estimate_costs(context.metadata)
            advice = advise_optimizations(estimates)
            citations = ["knowledge:cost_models#v1"]
            return AgentResult.success_result(
                payload={"tco": tco, "estimates": estimates, "advice": advice},
                confidence=0.75,
                citations=citations,
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR", "cost_optimization.failure", {"error": str(exc)}
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(
    CostOptimizationAgent.AGENT_ID, lambda: CostOptimizationAgent()
)
