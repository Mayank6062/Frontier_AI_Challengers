"""SVG renderer: wrap source text into a simple SVG representation.

This renderer produces a deterministic, accessible SVG that embeds the
source text. It is intentionally simple and free of external dependencies.
"""

from __future__ import annotations



def render_svg_from_text(source: str, title: str | None = None) -> str:
    """Return an SVG string embedding the provided source text.

    The SVG uses a <foreignObject> to include the preformatted source. This
    is suitable for downstream pipelines that need an SVG representation.
    """
    safe_title = title or "diagram"
    escaped = (
        source.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    svg = f"""<?xml version='1.0' encoding='utf-8'?>
<svg xmlns='http://www.w3.org/2000/svg' width='800' height='600' role='img' aria-label='{safe_title}'>
  <title>{safe_title}</title>
  <rect width='100%' height='100%' fill='white' />
  <foreignObject x='8' y='8' width='784' height='584'>
    <div xmlns='http://www.w3.org/1999/xhtml' style='font-family:monospace;white-space:pre; font-size:12px;'>
{escaped}
    </div>
  </foreignObject>
</svg>"""
    return svg


__all__ = ["render_svg_from_text"]
