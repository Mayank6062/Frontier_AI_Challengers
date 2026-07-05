from __future__ import annotations

import asyncio

from backend.agents.base.agent_context import AgentContext

from backend.agents.design.architecture_design.agent import ArchitectureDesignAgent
from backend.agents.design.infrastructure_recommendation.agent import (
    InfrastructureRecommendationAgent,
)
from backend.agents.design.technology_recommendation.agent import (
    TechnologyRecommendationAgent,
)
from backend.agents.discovery.knowledge_retrieval.agent import KnowledgeRetrievalAgent
from backend.agents.discovery.requirement_intelligence.agent import (
    RequirementIntelligenceAgent,
)
from backend.agents.governance.documentation.agent import DocumentationAgent
from backend.agents.governance.governance.agent import GovernanceAgent
from backend.agents.governance.human_collaboration.agent import (
    HumanCollaborationAgent,
)
from backend.agents.validation.compliance.agent import ComplianceAgent
from backend.agents.validation.cost_optimization.agent import CostOptimizationAgent
from backend.agents.validation.risk_assessment.agent import RiskAssessmentAgent
from backend.agents.validation.security.agent import SecurityAgent


def test_agents_execute_simple() -> None:
    ctx = AgentContext()
    agents = [
        ArchitectureDesignAgent(),
        InfrastructureRecommendationAgent(),
        TechnologyRecommendationAgent(),
        KnowledgeRetrievalAgent(),
        RequirementIntelligenceAgent(),
        DocumentationAgent(),
        GovernanceAgent(),
        HumanCollaborationAgent(),
        ComplianceAgent(),
        CostOptimizationAgent(),
        RiskAssessmentAgent(),
        SecurityAgent(),
    ]

    loop = asyncio.get_event_loop()
    for a in agents:
        res = loop.run_until_complete(a.execute_impl(ctx))
        assert res is not None
        # basic shape checks
        assert hasattr(res, "success")
        assert hasattr(res, "payload")
