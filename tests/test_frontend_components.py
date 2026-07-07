from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP_DIR = ROOT / "src" / "frontend" / "src" / "shared" / "components"


def test_components_exist_and_use_tokens():
    components = [
        "Button/Button.tsx",
        "Card/Card.tsx",
        "Badge/Badge.tsx",
        "Icon/Icon.tsx",
        "Skeleton/Skeleton.tsx",
        "Modal/Modal.tsx",
        "ScoreHeroCard/ScoreHeroCard.tsx",
        "ConfidenceBar/ConfidenceBar.tsx",
        "CitationTag/CitationTag.tsx",
        "EmptyState/EmptyState.tsx",
    ]
    for c in components:
        p = COMP_DIR / c
        assert p.exists(), f"Missing component: {p}"
        content = p.read_text(encoding="utf-8")
        assert "--og2-" in content or "var(--og2-" in content, f"Component {c} not tokenized"
