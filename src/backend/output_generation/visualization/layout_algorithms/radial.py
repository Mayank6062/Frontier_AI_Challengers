"""Radial layout algorithm."""

from __future__ import annotations

from .force_directed import force_directed_layout
from ...diagrams.models import DiagramDefinition
from ..layout import LayoutResult


def radial_layout(definition: DiagramDefinition) -> LayoutResult:
    return force_directed_layout(definition, radius=180.0)


__all__ = ["radial_layout"]
