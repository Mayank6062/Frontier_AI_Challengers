"""Diagrams package — canonical Chapter 18 diagrams layer.

This package mirrors the canonical structure from the Bible (Chapter 18).
It re-uses existing data models and provides concrete generators and renderers.
"""

from .models import (
    DiagramDefinition,
    DiagramNode,
    DiagramEdge,
    DiagramCluster,
    DiagramLegend,
    DiagramMetadata,
    LayoutHints,
    AccessibilitySpec,
)

from .enums import DiagramType, DiagramFormat
from .diagram_engine import DiagramEngine, DiagramRenderResult
from .dot_generator import DotGenerator
from .mermaid_generator import MermaidGenerator

__all__ = [
    "DiagramDefinition",
    "DiagramNode",
    "DiagramEdge",
    "DiagramCluster",
    "DiagramLegend",
    "DiagramMetadata",
    "LayoutHints",
    "AccessibilitySpec",
    "DiagramType",
    "DiagramFormat",
    "DiagramEngine",
    "DiagramRenderResult",
    "DotGenerator",
    "MermaidGenerator",
]
