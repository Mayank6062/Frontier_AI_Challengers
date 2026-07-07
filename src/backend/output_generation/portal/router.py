from __future__ import annotations

from typing import Dict, List, Optional, Protocol
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class PortalRoute(BaseModel):
    route_id: UUID = Field(default_factory=uuid4)
    path: str
    name: str
    description: Optional[str] = None
    params: Optional[List[str]] = None

    model_config = {"extra": "forbid", "frozen": True}


class RouteMatch(BaseModel):
    route: PortalRoute
    params: Optional[Dict[str, str]] = None

    model_config = {"extra": "forbid", "frozen": True}


class PortalRouter(Protocol):
    def register_route(self, route: PortalRoute) -> None:
        """Register a portal route."""

    def match(self, path: str) -> Optional[RouteMatch]:
        """Match a path to a registered route."""

    def navigate(self, path: str) -> None:
        """Navigate to the given path (update state/emit events)."""
