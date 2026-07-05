from __future__ import annotations

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry



class KnowledgeRetrievalAgent(BaseAgent):
    AGENT_ID = "knowledge_retrieval"
    AGENT_NAME = "Knowledge Retrieval"
    REQUIRED_CONTEXT_KEYS = ["query"]

    def __init__(
        self,
        observability=None,
        validator=None,
        knowledge=None,
    ) -> None:
        super().__init__(observability=observability, validator=validator, knowledge=knowledge)

    async def _resolve_knowledge(self, context: AgentContext) -> None:
        query = context.metadata.get("query", "") if context.metadata else ""
        rc = self._knowledge.retrieve(query)
        context.runtime_vars["retrieved_knowledge"] = rc

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        query = context.metadata.get("query", "") if context.metadata else ""
        # Use KnowledgeInterface for retrieval
        rc = self._knowledge.retrieve(query)
        # Use prefetched retrieval from lifecycle hook
        rc = context.runtime_vars.get("retrieved_knowledge")
        items = rc.items or []
        # simple ranking by excerpt length to preserve previous behavior
        ranked = sorted(items, key=lambda it: len(it.excerpt or ""), reverse=True)
        citations = [c.citation_id for c in rc.citations] if rc.citations else []
        payload = {"count": len(items), "citations": citations}
        return AgentResult.success_result(payload=payload, confidence=0.7, citations=citations)


AgentRegistry().register(
    KnowledgeRetrievalAgent.AGENT_ID, lambda: KnowledgeRetrievalAgent()
)
