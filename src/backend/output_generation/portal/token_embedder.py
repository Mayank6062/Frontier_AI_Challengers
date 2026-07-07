from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BUILD_DIR = ROOT / "config" / "styles" / "build"


def _css_path_for_theme(theme: str) -> Path:
    return BUILD_DIR / f"tokens.{theme}.css"


def get_css_for_theme(theme: str = "light") -> str:
    path = _css_path_for_theme(theme)
    if not path.exists():
        raise FileNotFoundError(f"Theme CSS not found: {path}")
    return path.read_text(encoding="utf-8")


def embed_theme_into_html(html: str, theme: str = "light") -> str:
    """Embed the theme tokens CSS into an HTML string by injecting a <style id='og2-theme-tokens'> block.

    If an existing style tag with id `og2-theme-tokens` is present, it will be replaced.
    """
    css = get_css_for_theme(theme)
    style_tag = f"<style id=\"og2-theme-tokens\">\n{css}\n</style>"
    if "id=\"og2-theme-tokens\"" in html:
        # replace existing block
        html = html.replace(
            html[html.find("<style id=\"og2-theme-tokens\""): html.find("</style>", html.find("<style id=\"og2-theme-tokens\"")) + 8],
            style_tag,
        )
        return html

    # inject before closing </head> if present, else at start
    if "</head>" in html:
        return html.replace("</head>", style_tag + "\n</head>")
    return style_tag + "\n" + html


if __name__ == "__main__":
    # simple CLI for testing
    import sys

    theme = sys.argv[1] if len(sys.argv) > 1 else "light"
    print(get_css_for_theme(theme))
