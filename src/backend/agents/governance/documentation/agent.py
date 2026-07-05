from __future__ import annotations

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .hld_generator import generate_hld
from .lld_generator import generate_lld
from .executive_summary_generator import generate_exec
from .risk_register_generator import generate_risk_register
from .assumptions_log_generator import generate_assumptions_log
from .diagram_generator import generate_diagram


class DocumentationAgent(BaseAgent):
    AGENT_ID = "documentation"
    AGENT_NAME = "Documentation"

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        try:
            hld = generate_hld(context.metadata)
            lld = generate_lld(context.metadata)
            execs = generate_exec(context.metadata)
            risk = generate_risk_register(context.metadata)
            assumptions = generate_assumptions_log(context.metadata)
            diagram = generate_diagram(context.metadata)
            payload = {
                "hld": hld,
                "lld": lld,
                "exec": execs,
                "risk": risk,
                "assumptions": assumptions,
                "diagram": diagram,
            }
            return AgentResult.success_result(
                payload=payload, confidence=0.9, citations=["knowledge:docs#v1"]
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR", "documentation.failure", {"error": str(exc)}
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(DocumentationAgent.AGENT_ID, lambda: DocumentationAgent())
