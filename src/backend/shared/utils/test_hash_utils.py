"""Tests for hash utilities."""

# pylint: disable=missing-function-docstring

from . import hash_utils


def test_stable_hash_changes_with_input() -> None:
    h1 = hash_utils.stable_hash("a", "b")
    h2 = hash_utils.stable_hash("a", "b")
    h3 = hash_utils.stable_hash("b", "a")
    assert h1 == h2
    assert h1 != h3
