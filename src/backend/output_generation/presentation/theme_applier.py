from __future__ import annotations

from typing import Any, Dict
from pathlib import Path


class ThemeArtifact:
    def __init__(self, tokens: Dict[str, str]) -> None:
        self.tokens = tokens


class ThemeApplier:
    """Load simple theme tokens from the template pack and expose an artifact

    This implementation uses a minimal parser for the project's YAML-style
    `theme_tokens.yaml` to avoid adding external dependencies.
    """

    def apply(self, template_pack: Any, persona: str) -> ThemeArtifact:
        tokens: Dict[str, str] = {}
        # template_pack may be a path or object with `root` attribute
        base = None
        if template_pack is None:
            # default tokens
            tokens = {"primary": "#003366", "accent": "#0077CC", "font": "Arial"}
            return ThemeArtifact(tokens)

        if isinstance(template_pack, (str, Path)):
            base = Path(template_pack)
        else:
            base = getattr(template_pack, "root", None)

        tokens_file = None
        if base:
            p = Path(base) / "theme_tokens.yaml"
            if p.exists():
                tokens_file = p

        if not tokens_file:
            # fallback defaults
            tokens = {"primary": "#003366", "accent": "#0077CC", "font": "Arial"}
            return ThemeArtifact(tokens)

        # lightweight YAML-ish parser (supports simple key: value pairs)
        with open(tokens_file, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" not in line:
                    continue
                k, v = line.split(":", 1)
                tokens[k.strip()] = v.strip()

        return ThemeArtifact(tokens)


__all__ = ["ThemeApplier", "ThemeArtifact"]
