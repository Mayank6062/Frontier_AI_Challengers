"""Tests for text utilities."""

# pylint: disable=missing-function-docstring

from . import text_utils


def test_normalize_and_truncate() -> None:
    s = "  a   b  c  "
    assert text_utils.normalize_whitespace(s) == "a b c"
    long = "word " * 20
    t = text_utils.safe_truncate(long, 10)
    assert len(t) <= 10


def test_json_roundtrip() -> None:
    d = {"b": 2, "a": 1}
    s = text_utils.to_json(d)
    assert isinstance(s, str)
    dd = text_utils.from_json(s)
    assert dd == d
