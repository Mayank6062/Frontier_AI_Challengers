"""Theme generation for visualization outputs."""

from __future__ import annotations

from .theme import ColorPalette, VisualizationTheme, VisualizationTokens


class ThemeEngine:
    """Create named visualization themes from design tokens."""

    def build(self, name: str = "light", tokens: dict[str, str] | None = None) -> VisualizationTheme:
        token_map = tokens or {"background": "#ffffff", "foreground": "#172033", "accent": "#155eef"}
        return VisualizationTheme(
            name=name,
            tokens=VisualizationTokens(tokens=token_map),
            colors=ColorPalette(primary=token_map.get("accent"), secondary=token_map.get("foreground")),
        )


__all__ = ["ThemeEngine"]
