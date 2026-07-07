"""Prepare diagram artifacts for print (paper) layouts."""

from __future__ import annotations

from typing import Dict
from .models import DiagramDefinition


def format_for_print(defn: DiagramDefinition, page_width: int = 1024, page_height: int = 768) -> Dict[str, object]:
    """Return a dict with print layout settings for the diagram."""
    return {
        "page_width": page_width,
        "page_height": page_height,
        "scale": 1.0,
        "margins": {"top": 24, "bottom": 24, "left": 24, "right": 24},
        "center": True,
    }


__all__ = ["format_for_print"]
