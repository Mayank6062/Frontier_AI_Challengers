"""Collision detection for visualization layouts."""

from __future__ import annotations

from .collision import CollisionReport, CollisionResult, CollisionStatistics, OverlapInformation
from .layout import NodePosition


class CollisionDetector:
    """Detect node collisions using a fixed square hit area."""

    def detect(self, positions: list[NodePosition], node_size: float = 80.0) -> CollisionResult:
        overlaps: list[OverlapInformation] = []
        for index, left in enumerate(positions):
            for right in positions[index + 1 :]:
                dx = abs(left.x - right.x)
                dy = abs(left.y - right.y)
                if dx < node_size and dy < node_size:
                    overlaps.append(
                        OverlapInformation(
                            node_a=left.node_id,
                            node_b=right.node_id,
                            overlap_area=(node_size - dx) * (node_size - dy),
                        )
                    )
        return CollisionResult(
            report=CollisionReport(overlaps=overlaps),
            statistics=CollisionStatistics(overlaps_found=len(overlaps), resolved=0),
        )


__all__ = ["CollisionDetector"]
