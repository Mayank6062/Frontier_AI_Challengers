"""
Base Model — Canonical serialization and validation foundation.

Provides framework-level serialization and validation contracts for shared types across all layers.
Responsibility: Define serializable, validatable base type used by all domain models.
"""

from dataclasses import asdict, fields, is_dataclass
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="BaseModel")


class BaseModel:
    """
    Canonical base model providing serialization and validation contracts.

    Features:
    - Supports dataclass-based models with to_dict() / from_dict() serialization.
    - Provides immutability support for models requiring it.
    - Type-safe construction and field validation.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize model to dictionary.

        Returns:
            Dictionary representation of model fields.

        Raises:
            TypeError: If model is not a dataclass.
        """
        if not is_dataclass(self):
            raise TypeError(f"{self.__class__.__name__} must be a dataclass to use to_dict()")
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Deserialize model from dictionary.

        Args:
            data: Dictionary containing model fields.

        Returns:
            Constructed model instance.

        Raises:
            TypeError: If cls is not a dataclass.
            ValueError: If required fields are missing.
        """
        if not is_dataclass(cls):
            raise TypeError(f"{cls.__name__} must be a dataclass to use from_dict()")

        field_names = {f.name for f in fields(cls)}
        missing_required = field_names - set(data.keys())
        if missing_required:
            raise ValueError(
                f"Missing required fields for {cls.__name__}: {missing_required}"
            )

        return cls(**{k: data[k] for k in field_names if k in data})

    def __eq__(self, other: Any) -> bool:
        """Equality by value."""
        if not isinstance(other, self.__class__):
            return False
        return self.to_dict() == other.to_dict()

    def __repr__(self) -> str:
        """Representation showing class name and fields."""
        if is_dataclass(self):
            field_values = ", ".join(
                f"{f.name}={getattr(self, f.name)!r}" for f in fields(self)
            )
            return f"{self.__class__.__name__}({field_values})"
        return super().__repr__()
