from __future__ import annotations

from typing import Optional

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry
from ...base.agent_validator import AgentValidator
from backend.core.interfaces.observability_interface import ObservabilityInterface
from backend.core.interfaces.knowledge_interface import KnowledgeInterface


class KnowledgeRetrievalAgent(BaseAgent):
    AGENT_ID = "knowledge_retrieval"
    AGENT_NAME = "Knowledge Retrieval"
    REQUIRED_CONTEXT_KEYS = ["query"]

    def __init__(
        self,
        observability: Optional[ObservabilityInterface] = None,
        validator: Optional[AgentValidator] = None,
        knowledge: Optional[KnowledgeInterface] = None,
    ) -> None:
        super().__init__(
            observability=observability, validator=validator, knowledge=knowledge
        )

    async def _resolve_knowledge(self, context: AgentContext) -> None:
        query = context.metadata.get("query", "") if context.metadata else ""
        rc = self._knowledge.retrieve(query) if self._knowledge is not None else None
        context.runtime_vars["retrieved_knowledge"] = rc

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        query = context.metadata.get("query", "") if context.metadata else ""
        # Use KnowledgeInterface for retrieval
        # Attempt direct retrieval; if a prefetched result exists in runtime_vars
        # (populated by the lifecycle hook), prefer that.
        prefetched = context.runtime_vars.get("retrieved_knowledge")
        rc = (
            prefetched
            if prefetched is not None
            else (
                self._knowledge.retrieve(query) if self._knowledge is not None else None
            )
        )
        items = getattr(rc, "items", []) or []
        # simple ranking by excerpt length was previously used (no-op retained)
        citations = [
            getattr(c, "citation_id", None)
            for c in getattr(rc, "citations", [])
            if getattr(c, "citation_id", None)
        ]
        payload = {"count": len(items), "citations": citations}
        return AgentResult.success_result(
            payload=payload, confidence=0.7, citations=citations
        )


AgentRegistry().register(
    KnowledgeRetrievalAgent.AGENT_ID, lambda: KnowledgeRetrievalAgent()
)
