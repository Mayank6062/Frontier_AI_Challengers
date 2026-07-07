from __future__ import annotations

from typing import Optional

from backend.core.interfaces.cache_interface import CacheInterface
from backend.core.interfaces.llm_interface import LLMInterface
from backend.core.interfaces.secrets_interface import SecretsInterface
from backend.core.interfaces.storage_interface import StorageInterface
from backend.core.interfaces.ledger_interface import LedgerInterface

# Infrastructure implementations live here — composition root owns them
from backend.infrastructure.cache.cache_service import CacheService
from backend.infrastructure.llm.llm_client import LLMClient
from backend.infrastructure.llm.anthropic_adapter import AnthropicAdapter
from backend.infrastructure.llm.openai_adapter import OpenAIAdapter
from backend.infrastructure.observability.logger import Logger
from backend.infrastructure.observability.metrics import Metrics
from backend.infrastructure.observability.tracer import start_trace, TraceHandle
from backend.infrastructure.secrets.secrets_manager import SecretsManager
from backend.infrastructure.storage.storage_service import StorageService
from backend.infrastructure.storage.session_store import SessionStore
from backend.infrastructure.storage.engagement_store import EngagementStore
from backend.infrastructure.decision_ledger.ledger_service import LedgerService

# Orchestration components
from backend.orchestration.master_orchestrator import MasterOrchestrator
from backend.orchestration.pipeline_manager import PipelineManager
from backend.orchestration.agent_scheduler import AgentScheduler
from backend.orchestration.result_aggregator import ResultAggregator
from backend.orchestration.message_bus import MessageBus
from backend.agents.base.agent_registry import AgentRegistry


def create_cache_service() -> CacheInterface:
    return CacheService()


def create_storage_service() -> StorageService:
    return StorageService()


def create_session_store(storage: StorageService) -> SessionStore:
    return SessionStore(storage)


def create_engagement_store(storage: StorageService) -> EngagementStore:
    return EngagementStore(storage)


def create_secrets_manager(initial: dict[str, str] | None = None) -> SecretsInterface:
    return SecretsManager(initial)


def create_ledger_service() -> LedgerInterface:
    return LedgerService()


def create_llm_client() -> LLMInterface:
    return LLMClient()


def create_anthropic_adapter() -> LLMInterface:
    return AnthropicAdapter()


def create_openai_adapter() -> LLMInterface:
    return OpenAIAdapter()


def create_logger() -> Logger:
    return Logger()


def create_metrics() -> Metrics:
    return Metrics()


def create_trace_handle(
    name: str, metadata: dict[str, object] | None = None
) -> TraceHandle:
    return start_trace(name, metadata)


def create_bundle_assembler(storage: StorageService | None = None):
    # import here to avoid circular imports at module import time
    from backend.output_generation.bundle.bundle_assembler import BundleAssembler

    fs = None
    try:
        # prefer local filesystem-backed storage for artifact persistence
        from backend.output_generation.bundle.storage import FilesystemOutputStorage

        fs = FilesystemOutputStorage(".output_storage")
    except Exception:
        fs = None

    return BundleAssembler(storage=fs)


def create_message_bus() -> MessageBus:
    """Create the progress event message bus."""
    return MessageBus()


def create_result_aggregator() -> ResultAggregator:
    """Create the stage result aggregator."""
    return ResultAggregator()


def create_pipeline_manager() -> PipelineManager:
    """Create the pipeline manager with 17-stage execution plan from WORKFLOW_ENGINE.md.
    
    Defines all 17 stages:
    - Intake (system)
    - Discovery Stage (2 agents): requirement_intelligence, knowledge_retrieval
    - Design Stage (3 agents): architecture_design, technology_recommendation, infrastructure_recommendation
    - Validation Stage (4 agents in parallel): security, compliance, cost_optimization, risk_assessment
    - Governance Stage (3 agents): governance, human_collaboration, documentation
    - Output Stage (system)
    - Review Stage (system)
    
    For MVP, using a simplified 3-stage pipeline: intake → discovery → design
    """
    from backend.orchestration.models import StageDefinition
    
    # Define all stages
    stages = {
        # Intake (system stage)
        "intake": StageDefinition(stage_id="intake", agent_id=None, required=True),
        
        # Discovery Stage
        "requirement_intelligence": StageDefinition(
            stage_id="requirement_intelligence",
            agent_id="requirement_intelligence",
            timeout_seconds=30,
            required=True
        ),
        "knowledge_retrieval": StageDefinition(
            stage_id="knowledge_retrieval",
            agent_id="knowledge_retrieval",
            timeout_seconds=30,
            required=False
        ),
        
        # Design Stage
        "architecture_design": StageDefinition(
            stage_id="architecture_design",
            agent_id="architecture_design",
            timeout_seconds=60,
            required=True
        ),
        "technology_recommendation": StageDefinition(
            stage_id="technology_recommendation",
            agent_id="technology_recommendation",
            timeout_seconds=60,
            required=False
        ),
        "infrastructure_recommendation": StageDefinition(
            stage_id="infrastructure_recommendation",
            agent_id="infrastructure_recommendation",
            timeout_seconds=60,
            required=False
        ),
        
        # Validation Stage (parallel)
        "security": StageDefinition(
            stage_id="security",
            agent_id="security",
            timeout_seconds=45,
            required=False
        ),
        "compliance": StageDefinition(
            stage_id="compliance",
            agent_id="compliance",
            timeout_seconds=45,
            required=False
        ),
        "cost_optimization": StageDefinition(
            stage_id="cost_optimization",
            agent_id="cost_optimization",
            timeout_seconds=45,
            required=False
        ),
        "risk_assessment": StageDefinition(
            stage_id="risk_assessment",
            agent_id="risk_assessment",
            timeout_seconds=45,
            required=False
        ),
        
        # Governance Stage
        "governance": StageDefinition(
            stage_id="governance",
            agent_id="governance",
            timeout_seconds=30,
            required=False
        ),
        "human_collaboration": StageDefinition(
            stage_id="human_collaboration",
            agent_id="human_collaboration",
            timeout_seconds=30,
            required=False
        ),
        "documentation": StageDefinition(
            stage_id="documentation",
            agent_id="documentation",
            timeout_seconds=30,
            required=False
        ),
    }
    
    # Define execution plan (groups for sequential/parallel execution)
    # MVP: Simple 4-stage pipeline
    # intake (1) → requirement_intelligence (2) → architecture_design (3) → documentation (4)
    groups = [
        ["intake"],  # Stage 1: System intake
        ["requirement_intelligence"],  # Stage 2: Analyze requirements
        ["architecture_design"],  # Stage 3: Design architecture
        ["technology_recommendation", "infrastructure_recommendation"],  # Stage 4: Parallel recommendations
        ["security", "compliance", "cost_optimization", "risk_assessment"],  # Stage 5: Parallel validation
        ["governance", "human_collaboration"],  # Stage 6: Parallel governance
        ["documentation"],  # Stage 7: Document results
    ]
    
    return PipelineManager(stages=stages, groups=groups)


def create_agent_scheduler(registry: AgentRegistry) -> AgentScheduler:
    """Create the agent scheduler with the populated agent registry."""
    return AgentScheduler(registry)


def create_master_orchestrator(
    pipeline_manager: PipelineManager,
    scheduler: AgentScheduler,
    aggregator: ResultAggregator,
    bus: MessageBus,
) -> MasterOrchestrator:
    """Create the master orchestrator that coordinates workflow execution."""
    return MasterOrchestrator(pipeline_manager, scheduler, aggregator, bus)


def bootstrap_agent_registry() -> AgentRegistry:
    """Bootstrap the agent registry by explicitly registering all agent classes.
    
    Rather than relying on module-level AgentRegistry().register() calls,
    we explicitly instantiate and register each agent to ensure they're all
    in the same singleton registry instance.
    """
    registry = AgentRegistry()
    
    try:
        print("  Bootstrapping agents...")
        
        # Discovery stage agents
        from backend.agents.discovery.requirement_intelligence.agent import RequirementIntelligenceAgent
        registry.register(
            RequirementIntelligenceAgent.AGENT_ID,
            lambda: RequirementIntelligenceAgent()
        )
        print("    [OK] Requirement Intelligence Agent")
        
        from backend.agents.discovery.knowledge_retrieval.agent import KnowledgeRetrievalAgent
        registry.register(
            KnowledgeRetrievalAgent.AGENT_ID,
            lambda: KnowledgeRetrievalAgent()
        )
        print("    [OK] Knowledge Retrieval Agent")
        
        # Design stage agents
        from backend.agents.design.architecture_design.agent import ArchitectureDesignAgent
        registry.register(
            ArchitectureDesignAgent.AGENT_ID,
            lambda: ArchitectureDesignAgent()
        )
        print("    [OK] Architecture Design Agent")
        
        from backend.agents.design.technology_recommendation.agent import TechnologyRecommendationAgent
        registry.register(
            TechnologyRecommendationAgent.AGENT_ID,
            lambda: TechnologyRecommendationAgent()
        )
        print("    [OK] Technology Recommendation Agent")
        
        from backend.agents.design.infrastructure_recommendation.agent import InfrastructureRecommendationAgent
        registry.register(
            InfrastructureRecommendationAgent.AGENT_ID,
            lambda: InfrastructureRecommendationAgent()
        )
        print("    [OK] Infrastructure Recommendation Agent")
        
        # Validation stage agents
        from backend.agents.validation.security.agent import SecurityAgent
        registry.register(
            SecurityAgent.AGENT_ID,
            lambda: SecurityAgent()
        )
        print("    [OK] Security Agent")
        
        from backend.agents.validation.compliance.agent import ComplianceAgent
        registry.register(
            ComplianceAgent.AGENT_ID,
            lambda: ComplianceAgent()
        )
        print("    [OK] Compliance Agent")
        
        from backend.agents.validation.cost_optimization.agent import CostOptimizationAgent
        registry.register(
            CostOptimizationAgent.AGENT_ID,
            lambda: CostOptimizationAgent()
        )
        print("    [OK] Cost Optimization Agent")
        
        from backend.agents.validation.risk_assessment.agent import RiskAssessmentAgent
        registry.register(
            RiskAssessmentAgent.AGENT_ID,
            lambda: RiskAssessmentAgent()
        )
        print("    [OK] Risk Assessment Agent")
        
        # Governance stage agents
        from backend.agents.governance.governance.agent import GovernanceAgent
        registry.register(
            GovernanceAgent.AGENT_ID,
            lambda: GovernanceAgent()
        )
        print("    [OK] Governance Agent")
        
        from backend.agents.governance.human_collaboration.agent import HumanCollaborationAgent
        registry.register(
            HumanCollaborationAgent.AGENT_ID,
            lambda: HumanCollaborationAgent()
        )
        print("    [OK] Human Collaboration Agent")
        
        from backend.agents.governance.documentation.agent import DocumentationAgent
        registry.register(
            DocumentationAgent.AGENT_ID,
            lambda: DocumentationAgent()
        )
        print("    [OK] Documentation Agent")
        
        registered_count = len(list(registry.list()))
        print(f"  Agent bootstrap complete: {registered_count} agents registered")
        
    except Exception as e:
        print(f"  [WARN] Agent bootstrap failed: {e}")
        import traceback
        traceback.print_exc()
    
    return registry



class DIContainer:
    def __init__(self, secrets_initial: Optional[dict[str, str]] = None) -> None:
        self._secrets_initial = secrets_initial

    def build(self) -> "DIContainer.Provided":
        # Instrumentation prints help locate blocking constructor during tests
        print("DI: create_cache_service")
        cache = create_cache_service()
        print("DI: create_storage_service")
        storage = create_storage_service()
        print("DI: create_session_store")
        session_store = create_session_store(storage)
        print("DI: create_engagement_store")
        engagement_store = create_engagement_store(storage)
        print("DI: create_secrets_manager")
        secrets = create_secrets_manager(self._secrets_initial)
        print("DI: create_ledger_service")
        ledger = create_ledger_service()
        print("DI: create_llm_client")
        llm = create_llm_client()
        print("DI: create_logger")
        logger = create_logger()
        print("DI: create_metrics")
        metrics = create_metrics()
        print("DI: create_bundle_assembler")
        bundle_assembler = create_bundle_assembler()
        
        # Orchestration components
        print("DI: create_message_bus")
        message_bus = create_message_bus()
        print("DI: create_result_aggregator")
        result_aggregator = create_result_aggregator()
        print("DI: create_pipeline_manager")
        pipeline_manager = create_pipeline_manager()
        print("DI: bootstrap_agent_registry")
        agent_registry = bootstrap_agent_registry()
        print("DI: create_agent_scheduler")
        agent_scheduler = create_agent_scheduler(agent_registry)
        print("DI: create_master_orchestrator")
        master_orchestrator = create_master_orchestrator(
            pipeline_manager, agent_scheduler, result_aggregator, message_bus
        )

        return DIContainer.Provided(
            cache=cache,
            storage=storage,
            session_store=session_store,
            engagement_store=engagement_store,
            secrets=secrets,
            ledger=ledger,
            llm=llm,
            logger=logger,
            metrics=metrics,
            bundle_assembler=bundle_assembler,
            message_bus=message_bus,
            result_aggregator=result_aggregator,
            pipeline_manager=pipeline_manager,
            agent_registry=agent_registry,
            agent_scheduler=agent_scheduler,
            master_orchestrator=master_orchestrator,
        )

    class Provided:
        def __init__(
            self,
            cache: CacheInterface,
            storage: StorageInterface,
            session_store: SessionStore,
            engagement_store: EngagementStore,
            secrets: SecretsInterface,
            ledger: LedgerInterface,
            llm: LLMInterface,
            logger: Logger,
            metrics: Metrics,
            bundle_assembler: object | None = None,
            message_bus: MessageBus | None = None,
            result_aggregator: ResultAggregator | None = None,
            pipeline_manager: PipelineManager | None = None,
            agent_registry: AgentRegistry | None = None,
            agent_scheduler: AgentScheduler | None = None,
            master_orchestrator: MasterOrchestrator | None = None,
        ) -> None:
            self.cache = cache
            self.storage = storage
            self.session_store = session_store
            self.engagement_store = engagement_store
            self.secrets = secrets
            self.ledger = ledger
            self.llm = llm
            self.logger = logger
            self.metrics = metrics
            self.bundle_assembler = bundle_assembler
            self.message_bus = message_bus
            self.result_aggregator = result_aggregator
            self.pipeline_manager = pipeline_manager
            self.agent_registry = agent_registry
            self.agent_scheduler = agent_scheduler
            self.master_orchestrator = master_orchestrator


__all__ = ["DIContainer"]
