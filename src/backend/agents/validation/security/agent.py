from __future__ import annotations


from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .threat_modeler import generate_threat_model
from .control_mapper import map_controls
from .finding_classifier import classify_findings


class SecurityAgent(BaseAgent):
    AGENT_ID = "security"
    AGENT_NAME = "Security Validation"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        artifact = context.metadata.get("artifact") if context.metadata else None
        try:
            threats = generate_threat_model(artifact)
            controls = map_controls(threats)
            findings = classify_findings(threats)
            citations = [t.get("citation") for t in threats if t.get("citation")]
            return AgentResult.success_result(
                payload={
                    "threats": threats,
                    "controls": controls,
                    "findings": findings,
                },
                confidence=0.82,
                citations=citations,
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR", "security.failure", {"error": str(exc)}
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(SecurityAgent.AGENT_ID, lambda: SecurityAgent())
