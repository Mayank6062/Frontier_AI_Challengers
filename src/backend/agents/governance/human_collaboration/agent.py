from __future__ import annotations

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .proposal_packager import package_proposal
from .feedback_router import route_feedback
from .override_recorder import record_override


class HumanCollaborationAgent(BaseAgent):
    AGENT_ID = "human_collaboration"
    AGENT_NAME = "Human Collaboration"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        try:
            proposal = package_proposal(context.metadata)
            routed = route_feedback(proposal)
            record = record_override(context.metadata)
            return AgentResult.success_result(
                payload={
                    "proposal": proposal,
                    "routed": routed,
                    "override_record": record,
                },
                confidence=0.65,
                citations=["knowledge:human-collab#v1"],
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR", "human_collab.failure", {"error": str(exc)}
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(
    HumanCollaborationAgent.AGENT_ID, lambda: HumanCollaborationAgent()
)
