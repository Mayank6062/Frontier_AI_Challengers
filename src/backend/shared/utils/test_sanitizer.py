from . import sanitizer


def test_ensure_non_empty_string():
    assert sanitizer.ensure_non_empty_string("x") == "x"
    try:
        sanitizer.ensure_non_empty_string("  ")
        assert False, "should raise"
    except ValueError:
        pass

def test_sanitize_whitespace():
    assert sanitizer.sanitize_whitespace(" a   b ") == "a b"
