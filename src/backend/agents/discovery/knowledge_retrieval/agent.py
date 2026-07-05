from __future__ import annotations

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry
from .retriever import simple_retriever
from .ranker import length_ranker
from .citation_builder import build_citations


class KnowledgeRetrievalAgent(BaseAgent):
    AGENT_ID = "knowledge_retrieval"
    AGENT_NAME = "Knowledge Retrieval"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        query = context.metadata.get("query", "") if context.metadata else ""
        res = simple_retriever(query)
        ranked = length_ranker(res.documents)
        citations = build_citations(ranked)
        payload = {"count": len(ranked), "citations": citations}
        return AgentResult.success_result(payload=payload)


AgentRegistry().register(
    KnowledgeRetrievalAgent.AGENT_ID, lambda: KnowledgeRetrievalAgent()
)
