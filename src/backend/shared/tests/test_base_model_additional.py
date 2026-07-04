"""Additional tests for BaseModel to cover defaults and export behavior."""

from backend.shared.models.base_model import BaseModel


class _Sample(BaseModel):
    a: int
    b: str


def test_defaults_and_to_dict_excludes_none() -> None:
    s = _Sample(a=5, b="z")
    d = s.to_dict()
    # id and created_at should be present and be strings
    assert isinstance(d.get("id"), str)
    assert isinstance(d.get("created_at"), str)
    # updated_at defaults to None and should be excluded from dumped dict
    assert "updated_at" not in d


def test_from_dict_ignores_extra_keys() -> None:
    payload = {"a": 1, "b": "x", "extra": "ignored"}
    s = _Sample.from_dict(payload)
    # extra keys are not added as attributes
    assert not hasattr(s, "extra")
    assert s.a == 1 and s.b == "x"
