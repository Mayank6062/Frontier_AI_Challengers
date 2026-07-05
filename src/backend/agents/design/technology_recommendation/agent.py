from __future__ import annotations


from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .scorer import score_technologies
from .build_vs_buy import analyze_build_vs_buy


class TechnologyRecommendationAgent(BaseAgent):
    AGENT_ID = "technology_recommendation"
    AGENT_NAME = "Technology Recommendation"
    REQUIRED_CONTEXT_KEYS = ["domain"]

    def __init__(self, observability=None, validator=None, knowledge=None) -> None:
        super().__init__(observability=observability, validator=validator, knowledge=knowledge)

    async def _resolve_knowledge(self, context: AgentContext) -> None:
        domain = context.metadata.get("domain") if context.metadata else ""
        rc = self._knowledge.retrieve(domain or "")
        context.runtime_vars["retrieved_knowledge"] = rc

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        domain = context.metadata.get("domain") if context.metadata else None
        try:
            # Use prefetched knowledge retrieved in _resolve_knowledge
            rc = context.runtime_vars.get("retrieved_knowledge")
            candidates = [
                {
                    "name": i.title,
                    "entry_id": i.entry_id,
                    "citation": i.entry_id,
                    "maturity": i.relevance,
                    "fit": i.relevance,
                }
                for i in rc.items
            ]
            scored = score_technologies(candidates)
            decision = analyze_build_vs_buy(scored)
            citations = [c.get("citation") for c in scored if c.get("citation")]
            return AgentResult.success_result(
                payload={"scored": scored, "decision": decision},
                confidence=0.85,
                citations=citations,
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR", "technology_recommendation.failure", {"error": str(exc)}
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(
    TechnologyRecommendationAgent.AGENT_ID, lambda: TechnologyRecommendationAgent()
)
