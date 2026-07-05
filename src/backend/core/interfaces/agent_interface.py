from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from ...agents.base.agent_context import AgentContext
from ...agents.base.agent_result import AgentResult


class AgentCategory(str, Enum):
    DISCOVERY = "DISCOVERY"
    DESIGN = "DESIGN"
    VALIDATION = "VALIDATION"
    GENERATION = "GENERATION"
    GOVERNANCE = "GOVERNANCE"


class AgentInterface(ABC):
    """Asynchronous contract every agent implementation must satisfy.

    Concrete agents must define the AGENT_ID/AGENT_VERSION/AGENT_CATEGORY/AGENT_NAME
    class attributes and implement the asynchronous `execute` method.
    """

    AGENT_ID: str
    AGENT_VERSION: str
    AGENT_CATEGORY: Optional[AgentCategory]
    AGENT_NAME: str

    @abstractmethod
    async def execute(
        self, context: AgentContext
    ) -> AgentResult:  # pragma: no cover - contract only
        """Execute the agent asynchronously and return an AgentResult.

        Implementations must raise a typed exception on unrecoverable failures.
        """

        raise NotImplementedError()
