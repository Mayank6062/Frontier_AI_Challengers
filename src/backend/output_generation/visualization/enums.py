from __future__ import annotations

from enum import StrEnum


class LayoutAlgorithm(StrEnum):
    HIERARCHICAL = "hierarchical"
    FORCE_DIRECTED = "force_directed"
    RADIAL = "radial"
    GRID = "grid"
    SEQUENCE = "sequence"
    PIE = "pie"
    GANTT = "gantt"


class RoutingAlgorithm(StrEnum):
    ORTHOGONAL = "orthogonal"
    BEZIER = "bezier"
    EDGE_BUNDLING = "edge_bundling"


class NodeRankingStrategy(StrEnum):
    DEGREE = "degree"
    CENTRALITY = "centrality"
    CUSTOM = "custom"


class CollisionStrategy(StrEnum):
    REPULSION = "repulsion"
    INCREASE_SEPARATION = "increase_separation"
    IGNORE = "ignore"


class LegendPosition(StrEnum):
    BOTTOM_RIGHT = "bottom_right"
    BOTTOM = "bottom"
    TOP_RIGHT = "top_right"
    LEFT = "left"


class ThemeMode(StrEnum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class ViewportBreakpoint(StrEnum):
    DESKTOP = "desktop"
    LAPTOP = "laptop"
    TABLET = "tablet"
    MOBILE = "mobile"


class ZoomMode(StrEnum):
    CONTINUOUS = "continuous"
    STEP = "step"


class PrintMode(StrEnum):
    A4 = "a4"
    LETTER = "letter"


class RenderMode(StrEnum):
    VECTOR = "vector"
    RASTER = "raster"


class RendererType(StrEnum):
    MERMAID = "mermaid"
    DOT = "dot"
    SVG = "svg"
    PNG = "png"


class OutputTarget(StrEnum):
    PORTAL = "portal"
    WORKSPACE = "workspace"
    PRINT = "print"


class DiagramViewport(StrEnum):
    FULL = "full"
    FIT = "fit"


class ScalingMode(StrEnum):
    ASPECT_FIT = "aspect_fit"
    FILL = "fill"


class InteractionMode(StrEnum):
    PAN = "pan"
    ZOOM = "zoom"
    SELECT = "select"
