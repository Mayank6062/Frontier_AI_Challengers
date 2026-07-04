"""Tests for identifier utilities."""

# pylint: disable=missing-function-docstring

from . import identifiers


def test_uuid_generation_and_validation() -> None:
    u = identifiers.generate_uuid4()
    assert isinstance(u, str) and identifiers.is_valid_uuid(u)

    assert not identifiers.is_valid_uuid("not-a-uuid")
