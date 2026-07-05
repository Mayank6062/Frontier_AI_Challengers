from __future__ import annotations


from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .topology_designer import design_topology
from .iac_scaffolder import generate_iac_plan
from .landing_zone_mapper import map_landing_zone


class InfrastructureRecommendationAgent(BaseAgent):
    AGENT_ID = "infrastructure_recommendation"
    AGENT_NAME = "Infrastructure Recommendation"
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
            topo = design_topology(domain)
            lz = map_landing_zone(domain)
            iac = generate_iac_plan(topo, lz)
            # prefer citations from knowledge retrieval when available
            citations = [c.citation_id for c in rc.citations] if rc.citations else [topo.get("citation"), lz.get("citation")]
            return AgentResult.success_result(
                payload={"topology": topo, "landing_zone": lz, "iac": iac},
                confidence=0.78,
                citations=[c for c in citations if c],
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR",
                    "infrastructure_recommendation.failure",
                    {"error": str(exc)},
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(
    InfrastructureRecommendationAgent.AGENT_ID,
    lambda: InfrastructureRecommendationAgent(),
)
