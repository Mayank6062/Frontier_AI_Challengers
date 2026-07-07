from src.backend.output_generation.portal.token_embedder import embed_theme_into_html, get_css_for_theme


def test_get_css_for_theme_exists():
    css = get_css_for_theme("light")
    assert "--og2-" in css


def test_embed_theme_into_html_injects():
    html = "<html><head><title>Test</title></head><body></body></html>"
    out = embed_theme_into_html(html, "light")
    assert "id=\"og2-theme-tokens\"" in out
    assert "--og2-" in out
