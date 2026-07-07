from __future__ import annotations

from typing import List, Optional, Protocol
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class CommandEntry(BaseModel):
    command_id: UUID = Field(default_factory=uuid4)
    title: str
    shortcut: Optional[str] = None
    description: Optional[str] = None
    action: Optional[str] = None

    model_config = {"extra": "forbid", "frozen": True}


class CommandPaletteResult(BaseModel):
    command: CommandEntry
    relevance: float

    model_config = {"extra": "forbid", "frozen": True}


class CommandPaletteEngine(Protocol):
    def register(self, command: CommandEntry) -> None:
        """Register a command."""

    def query(self, q: str, top_k: int = 10) -> List[CommandPaletteResult]:
        """Query command palette for matches."""
