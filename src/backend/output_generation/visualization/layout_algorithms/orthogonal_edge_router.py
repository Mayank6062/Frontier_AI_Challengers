"""Orthogonal edge routing algorithm."""

from __future__ import annotations

from ...diagrams.models import DiagramDefinition
from ..layout import EdgeRoute, LayoutResult, NodePosition


def route_orthogonal_edges(definition: DiagramDefinition, positions: list[NodePosition]) -> list[EdgeRoute]:
    by_id = {position.node_id: position for position in positions}
    routes: list[EdgeRoute] = []
    for index, edge in enumerate(definition.edges):
        source = by_id.get(edge.source)
        target = by_id.get(edge.target)
        if source and target:
            mid_x = (source.x + target.x) / 2
            routes.append(
                EdgeRoute(
                    edge_id=f"edge-{index}",
                    points=[
                        {"x": source.x, "y": source.y},
                        {"x": mid_x, "y": source.y},
                        {"x": mid_x, "y": target.y},
                        {"x": target.x, "y": target.y},
                    ],
                )
            )
    return routes


def apply_orthogonal_routes(definition: DiagramDefinition, layout: LayoutResult) -> LayoutResult:
    return layout.model_copy(update={"routes": route_orthogonal_edges(definition, layout.positions)})


__all__ = ["apply_orthogonal_routes", "route_orthogonal_edges"]
