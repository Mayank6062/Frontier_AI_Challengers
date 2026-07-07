"""Token build tool: validate tokens.yaml and generate CSS token files."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys

import yaml
from jsonschema import validate, ValidationError

ROOT = Path(__file__).resolve().parents[1]
TOKENS_YAML = ROOT / "config" / "styles" / "tokens.yaml"
SCHEMA_JSON = ROOT / "config" / "styles" / "tokens.schema.json"
OUT_DIR = ROOT / "config" / "styles" / "build"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_out():
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def flatten_primitives(primitives: dict) -> dict:
    flat = {}
    for k, v in primitives.items():
        if isinstance(v, dict):
            for subk, subv in v.items():
                flat[f"{k}.{subk}"] = subv
        else:
            flat[k] = v
    return flat


def resolve_ref(value: str, primitives_flat: dict) -> str:
    # pattern {primitives.colors.gray-90}
    matches = re.findall(r"\{([^}]+)\}", str(value))
    out = str(value)
    for m in matches:
        if m in primitives_flat:
            out = out.replace("{" + m + "}", primitives_flat[m])
    return out


def gen_css_for_theme(tokens: dict, theme: str, primitives_flat: dict) -> str:
    lines = [":root {", f"  /* theme: {theme} */"]
    # semantic
    semantic = tokens.get("semantic", {})
    for k, v in semantic.items():
        if isinstance(v, dict):
            val = v.get(theme, None) or v.get("light")
            if val is not None:
                resolved = resolve_ref(val, primitives_flat)
                prop = f"--og2-{k.replace('.', '-') }"
                lines.append(f"  {prop}: {resolved};")
    # components (numbers -> px for CSS)
    components = tokens.get("components", {})
    for comp_k, comp_v in components.items():
        if isinstance(comp_v, dict):
            for prop_k, prop_v in comp_v.items():
                css_name = f"--og2-{comp_k.replace('.', '-')}-{prop_k}"
                if isinstance(prop_v, (int, float)):
                    lines.append(f"  {css_name}: {prop_v}px;")
                else:
                    lines.append(f"  {css_name}: {prop_v};")

    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    try:
        tokens = load_yaml(TOKENS_YAML)
    except Exception as e:
        print(f"Failed to load {TOKENS_YAML}: {e}")
        return 2

    try:
        schema = load_json(SCHEMA_JSON)
    except Exception as e:
        print(f"Failed to load schema {SCHEMA_JSON}: {e}")
        return 2

    try:
        validate(instance=tokens, schema=schema)
    except ValidationError as e:
        print("Token schema validation failed:")
        print(e)
        return 3

    primitives_flat = flatten_primitives(tokens.get("primitives", {}))
    ensure_out()

    themes = ["light", "dark", "print", "presentation"]
    for t in themes:
        css = gen_css_for_theme(tokens, t, primitives_flat)
        out_path = OUT_DIR / f"tokens.{t}.css"
        out_path.write_text(css, encoding="utf-8")
        print(f"Wrote {out_path}")

    # write diagram-tokens.yaml (semantic subset)
    diag = {"diagram": tokens.get("semantic", {})}
    (OUT_DIR / "diagram-tokens.yaml").write_text(yaml.safe_dump(diag), encoding="utf-8")
    print("Wrote diagram-tokens.yaml")

    print("Token build succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
