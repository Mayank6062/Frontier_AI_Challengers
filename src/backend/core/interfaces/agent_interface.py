from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum

from ...agents.base.base_agent import AgentContext, AgentResult


class AgentCategory(str, Enum):
    DISCOVERY = "DISCOVERY"
    DESIGN = "DESIGN"
    VALIDATION = "VALIDATION"
    GENERATION = "GENERATION"
    GOVERNANCE = "GOVERNANCE"


class AgentInterface(ABC):
    """Contract every agent implementation must satisfy.

    Concrete agents must define the AGENT_ID/AGENT_VERSION/AGENT_CATEGORY/AGENT_NAME
    class attributes and implement the synchronous `execute` method.
    """

    AGENT_ID: str
    AGENT_VERSION: str
    AGENT_CATEGORY: AgentCategory
    AGENT_NAME: str

    @abstractmethod
    def execute(
        self, context: AgentContext
    ) -> AgentResult:  # pragma: no cover - contract only
        """Execute the agent synchronously and return an AgentResult.

        Implementations must raise a typed exception on unrecoverable failures.
        """

        raise NotImplementedError()
