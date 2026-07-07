import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "config" / "styles" / "build"


def test_token_build_generates_files():
    res = subprocess.run(["python", ".tools/token_build.py"], capture_output=True, text=True)
    print(res.stdout)
    assert res.returncode == 0, f"token build failed: {res.stderr}"
    assert (OUT_DIR / "tokens.light.css").exists()
    assert (OUT_DIR / "tokens.dark.css").exists()
    assert (OUT_DIR / "diagram-tokens.yaml").exists()
