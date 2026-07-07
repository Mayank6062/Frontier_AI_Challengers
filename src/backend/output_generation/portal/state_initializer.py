"""Portal state initialization."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PortalInitialState:
    current_route: str = "/"
    active_persona: str = "executive"
    theme: str = "light"
    density: str = "comfortable"
    expanded_sections: tuple[str, ...] = field(default_factory=tuple)
    diagram_zoom_levels: dict[str, float] = field(default_factory=dict)


class StateInitializer:
    """Create deterministic initial portal state dictionaries."""

    def initialize(self, persona: str = "executive", theme: str = "light") -> PortalInitialState:
        if not persona.strip():
            raise ValueError("persona must not be empty")
        if theme not in {"light", "dark"}:
            raise ValueError("theme must be 'light' or 'dark'")
        return PortalInitialState(active_persona=persona, theme=theme)


__all__ = ["PortalInitialState", "StateInitializer"]
