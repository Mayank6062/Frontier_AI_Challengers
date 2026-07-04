"""
Shared base model utilities.

Provides a lightweight, dataclass-based base model with
serialization helpers used across the backend.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="BaseModel")


@dataclass(frozen=True)
class BaseModel:
    """Immutable base model with simple (de)serialization helpers.

    Subclass this for plain-data DTOs that must be immutable and
    serializable to dictionaries.

    Usage:
        @dataclass(frozen=True)
        class Foo(BaseModel):
            a: int
            b: str

        f = Foo(1, "x")
        d = f.to_dict()
        f2 = Foo.from_dict(d)
    """

    def to_dict(self) -> Dict[str, Any]:
        """Return a shallow dictionary representation of the dataclass.

        Returns:
            dict: mapping of field name to value.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create an instance from a dictionary.

        Extra keys in ``data`` that do not map to dataclass fields are ignored.

        Args:
            data: dictionary of values to map to dataclass fields.

        Returns:
            Instance of the dataclass.
        """
        field_names = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered)  # type: ignore
