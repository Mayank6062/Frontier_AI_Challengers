from __future__ import annotations

from threading import RLock
from typing import Callable, Dict, Iterable

from ...core.interfaces.agent_interface import AgentInterface


class AgentRegistry:
    """Thread-safe registry for agent classes or factory callables.

    This registry does not implement a service locator; it only maps string
    identifiers to agent factory callables (callable -> AgentInterface instance).
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._entries: Dict[str, Callable[[], AgentInterface]] = {}

    def register(self, agent_id: str, factory: Callable[[], AgentInterface]) -> None:
        if not callable(factory):
            raise TypeError("factory must be callable")
        with self._lock:
            if agent_id in self._entries:
                raise KeyError(f"Agent already registered: {agent_id}")
            # Validate a sample instance type if possible
            sample = factory()
            if not isinstance(sample, AgentInterface):
                raise TypeError("factory must return an AgentInterface instance")
            # store a lambda that will produce fresh instances
            self._entries[agent_id] = factory

    def unregister(self, agent_id: str) -> None:
        with self._lock:
            if agent_id in self._entries:
                del self._entries[agent_id]

    def exists(self, agent_id: str) -> bool:
        with self._lock:
            return agent_id in self._entries

    def get(self, agent_id: str) -> AgentInterface:
        with self._lock:
            factory = self._entries.get(agent_id)
            if factory is None:
                raise KeyError(f"Agent not found: {agent_id}")
            return factory()

    def list(self) -> Iterable[str]:
        with self._lock:
            return list(self._entries.keys())

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
