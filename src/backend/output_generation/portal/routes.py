"""Canonical portal route registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True)
class PortalRoute:
    path: str
    name: str
    description: str | None = None
    params: tuple[str, ...] = ()
    route_id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class RouteMatch:
    route: PortalRoute
    params: dict[str, str] = field(default_factory=dict)


class RouteRegistry:
    """Register and match static portal routes."""

    def __init__(self, routes: list[PortalRoute] | None = None) -> None:
        self._routes: dict[str, PortalRoute] = {}
        for route in routes or self.default_routes():
            self.register_route(route)

    @staticmethod
    def default_routes() -> list[PortalRoute]:
        return [
            PortalRoute("/", "Overview"),
            PortalRoute("/architecture", "Architecture"),
            PortalRoute("/risks", "Risks"),
            PortalRoute("/technology", "Technology"),
            PortalRoute("/citations", "Citations"),
            PortalRoute("/walkthrough", "Walkthrough"),
        ]

    def register_route(self, route: PortalRoute) -> None:
        if not route.path.startswith("/"):
            raise ValueError("route path must start with '/'")
        self._routes[route.path] = route

    def match(self, path: str) -> RouteMatch | None:
        route = self._routes.get(path)
        return RouteMatch(route=route) if route else None

    def list_routes(self) -> list[PortalRoute]:
        return list(self._routes.values())


__all__ = ["PortalRoute", "RouteMatch", "RouteRegistry"]
