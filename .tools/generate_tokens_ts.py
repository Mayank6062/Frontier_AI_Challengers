"""Generate a TypeScript tokens file from config/styles/tokens.yaml"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
TOKENS_YAML = ROOT / "config" / "styles" / "tokens.yaml"
OUT = ROOT / "src" / "frontend" / "src" / "shared" / "theme"


def camel_case(s: str) -> str:
    return s.replace("-", "_").replace(".", "_")


def ensure_out():
    OUT.mkdir(parents=True, exist_ok=True)


def generate():
    data = yaml.safe_load(TOKENS_YAML.read_text(encoding="utf-8"))
    ensure_out()
    lines = ["// Generated from config/styles/tokens.yaml", "export const tokens = {"]

    # primitives (flatten)
    primitives = data.get("primitives", {})
    for k, v in primitives.items():
        if isinstance(v, dict):
            for subk, subv in v.items():
                name = camel_case(f"{k}.{subk}")
                lines.append(f"  '{name}': '{subv}',")
        else:
            name = camel_case(k)
            lines.append(f"  '{name}': '{v}',")

    # semantic
    semantic = data.get("semantic", {})
    for k, v in semantic.items():
        if isinstance(v, dict):
            for theme, val in v.items():
                name = camel_case(f"semantic.{k}.{theme}")
                lines.append(f"  '{name}': '{val}',")

    lines.append("};")
    out_path = OUT / "tokens.ts"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    generate()
