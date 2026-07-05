from __future__ import annotations


from typing import Optional, Any

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry
from backend.core.interfaces.knowledge_interface import KnowledgeInterface

from .scorer import score_technologies
from .build_vs_buy import analyze_build_vs_buy


class TechnologyRecommendationAgent(BaseAgent):
    AGENT_ID = "technology_recommendation"
    AGENT_NAME = "Technology Recommendation"
    REQUIRED_CONTEXT_KEYS = ["domain"]

    def __init__(
        self,
        observability: Optional[Any] = None,
        validator: Optional[Any] = None,
        knowledge: Optional[KnowledgeInterface] = None,
    ) -> None:
        super().__init__(
            observability=observability, validator=validator, knowledge=knowledge
        )

    async def _resolve_knowledge(self, context: AgentContext) -> None:
        domain = context.metadata.get("domain") if context.metadata else ""
        rc = self._knowledge.retrieve(domain or "")
        context.runtime_vars["retrieved_knowledge"] = rc

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        try:
            # Use prefetched knowledge retrieved in _resolve_knowledge
            rc = context.runtime_vars.get("retrieved_knowledge") or None
            items = getattr(rc, "items", []) or []
            candidates = [
                {
                    "name": getattr(i, "title", None),
                    "entry_id": getattr(i, "entry_id", None),
                    "citation": getattr(i, "entry_id", None),
                    "maturity": getattr(i, "relevance", None),
                    "fit": getattr(i, "relevance", None),
                }
                for i in items
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
