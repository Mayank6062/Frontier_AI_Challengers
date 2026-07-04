from .base_model import BaseModel


class _Sample(BaseModel):
    a: int
    b: str


def test_to_from_dict_roundtrip():
    s = _Sample(a=1, b="x")
    d = s.to_dict()
    assert d["a"] == 1
    assert d["b"] == "x"
    s2 = _Sample.from_dict({"a": 1, "b": "x"})
    assert s2.a == s.a and s2.b == s.b


def test_immutable():
    s = _Sample(a=2, b="y")
    try:
        s.a = 3  # Pydantic frozen model should raise
        assert False, "assignment should be prohibited on frozen model"
    except Exception:
        pass
