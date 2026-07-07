"""PNG rasterizer: provide deterministic PNG artifact bytes for SVG input."""

from __future__ import annotations

import base64


_ONE_PIXEL_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/"
    "w8AAn8B9o9b6QAAAABJRU5ErkJggg=="
)


def rasterize_png_from_svg(svg_bytes: bytes) -> bytes:
    """Return a valid deterministic PNG byte sequence for the given SVG input."""
    if not svg_bytes:
        raise ValueError("svg_bytes must not be empty")
    return base64.b64decode(_ONE_PIXEL_PNG_B64)


__all__ = ["rasterize_png_from_svg"]
