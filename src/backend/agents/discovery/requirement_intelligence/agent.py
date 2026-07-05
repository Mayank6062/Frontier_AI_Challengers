from __future__ import annotations

from ...base.base_agent import BaseAgent
from ...base.agent_context import AgentContext
from ...base.agent_result import AgentResult
from ...base.agent_registry import AgentRegistry
from .extractor import simple_extractor
from .classifier import simple_classifier
from .ambiguity_detector import detect_ambiguities


class RequirementIntelligenceAgent(BaseAgent):
    AGENT_ID = "requirement_intelligence"
    AGENT_NAME = "Requirement Intelligence"
    REQUIRED_CONTEXT_KEYS = ["text"]

    async def execute_impl(self, context: AgentContext) -> AgentResult:
        text = context.metadata.get("text", "") if context.metadata else ""
        extraction = simple_extractor(text)
        classified = simple_classifier(extraction.requirements)
        ambiguities = detect_ambiguities(classified)
        payload = {
            "requirements_count": len(classified),
            "ambiguities": ambiguities,
        }
        # attach a provenance citation and a conservative confidence estimate
        citations = ["knowledge:requirements#v1"]
        return AgentResult.success_result(
            payload=payload, confidence=0.65, citations=citations
        )


# register with the AgentRegistry
AgentRegistry().register(
    RequirementIntelligenceAgent.AGENT_ID, lambda: RequirementIntelligenceAgent()
)
