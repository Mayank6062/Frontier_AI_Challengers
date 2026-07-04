"""Additional tests for shared utils to cover edge branches."""

from backend.shared.utils import hash_utils, text_utils


def test_stable_hash_with_list_and_tuple() -> None:
    h1 = hash_utils.stable_hash(["a", "b"], ("c",))
    h2 = hash_utils.stable_hash(["a", "b"], ("c",))
    assert isinstance(h1, str)
    assert len(h1) == 64
    assert h1 == h2


def test_from_json_raises_on_non_object() -> None:
    s = "[1,2,3]"
    try:
        text_utils.from_json(s)
    except ValueError:
        # expected
        return
    raise AssertionError("from_json should raise ValueError for non-object JSON")
