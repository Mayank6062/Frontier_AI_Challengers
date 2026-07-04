from dataclasses import dataclass

from .base_model import BaseModel


@dataclass(frozen=True)
class _Sample(BaseModel):
    a: int
    b: str


def test_to_from_dict_roundtrip():
    s = _Sample(1, "x")
    d = s.to_dict()
    assert d == {"a": 1, "b": "x"}
    s2 = _Sample.from_dict({"a": 1, "b": "x", "extra": 5})
    assert s2 == s


def test_immutable():
    s = _Sample(2, "y")
    try:
        s.a = 3  # should raise
        assert False, "dataclass should be frozen"
    except AttributeError:
        pass
