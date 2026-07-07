import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "frontend" / "src"


def test_no_hardcoded_hex_or_px_in_components():
    files = list((SRC / "shared" / "components").rglob("*.tsx"))
    hex_re = re.compile(r"#[0-9a-fA-F]{3,6}")
    px_re = re.compile(r"\b\d+px\b")
    violations = []
    for f in files:
        txt = f.read_text(encoding="utf-8")
        if hex_re.search(txt) or px_re.search(txt):
            violations.append(f)
    assert not violations, f"Hardcoded values found in: {violations}"
