from __future__ import annotations

from typing import Dict, Any

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry

from .candidate_generator import generate_candidates
from .tradeoff_analyzer import analyze_tradeoffs
from .pattern_composer import compose_patterns


class ArchitectureDesignAgent(BaseAgent):
    AGENT_ID = "architecture_design"
    AGENT_NAME = "Architecture Design"
    REQUIRED_CONTEXT_KEYS = ["requirements"]

    def __init__(self, observability=None, validator=None, knowledge=None) -> None:
        super().__init__(observability=observability, validator=validator, knowledge=knowledge)

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        reqs = context.metadata.get("requirements") if context.metadata else None
        try:
            # Build candidate architectures
            candidates = generate_candidates(reqs)
            # Enrich with pattern knowledge (pattern_composer uses static catalog citations)
            patterns = compose_patterns(context, candidates)
            scored = analyze_tradeoffs(candidates)
            payload: Dict[str, Any] = {
                "candidates": scored,
                "patterns": patterns,
            }
            citations = [
                p.get("citation")
                for p in patterns
                if isinstance(p, dict) and p.get("citation")
            ]
            return AgentResult.success_result(
                payload=payload, confidence=0.8, citations=citations
            )
        except Exception as exc:
            if context.observability:
                context.observability.emit_log(
                    "ERROR", "architecture_design.failure", {"error": str(exc)}
                )
            return AgentResult.internal_error(str(exc))


AgentRegistry().register(
    ArchitectureDesignAgent.AGENT_ID, lambda: ArchitectureDesignAgent()
)
