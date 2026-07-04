"""
Shared base model utilities using Pydantic as required by architecture.

Provides a canonical Pydantic `BaseModel` subclass with immutable
configuration, stable (de)serialization helpers and bridge methods
to preserve existing callers' expectations (`to_dict`, `from_dict`).
"""

from __future__ import annotations
# pylint: disable=broad-exception-caught

from typing import Any, Dict, Type, TypeVar, Optional
from .identifiers import generate_uuid4
from .timestamps import now_iso

T = TypeVar("T", bound="BaseModel")

try:
    # Prefer Pydantic v2 API; v1 share BaseModel import as well
    from pydantic import BaseModel as _PydanticBaseModel
    from pydantic import Field
    from pydantic import ConfigDict

    _PYDANTIC_V2 = True
except Exception:
    try:
        from pydantic import BaseModel as _PydanticBaseModel
        from pydantic import Field

        _PYDANTIC_V2 = False
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("Pydantic is required for Shared BaseModel") from exc


class BaseModel(_PydanticBaseModel):
    """Canonical shared BaseModel implemented on top of Pydantic.

    Characteristics:
    - Immutable / frozen
    - Provides `to_dict()` / `from_dict()` compatibility shims
    - Uses Pydantic's model dump/validation machinery for correctness
    """

    if _PYDANTIC_V2:  # Pydantic v2 configuration
        model_config = ConfigDict(frozen=True)
    else:  # Pydantic v1 configuration style

        class Config:
            allow_mutation = False

    # Canonical fields required by architecture
    # Use shared utilities for canonical defaults

    id: Optional[str] = Field(default_factory=generate_uuid4)
    created_at: Optional[str] = Field(default_factory=now_iso)
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Return a dict representation using Pydantic's dumping.

        This is a stable API used by existing callers.
        """
        if _PYDANTIC_V2:
            return self.model_dump(exclude_none=True)
        return self.dict(exclude_none=True)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create an instance from a mapping using Pydantic validation.

        Extra keys are rejected by Pydantic by default unless model config allows.
        """
        if _PYDANTIC_V2:
            return cls.model_validate(data)
        return cls.parse_obj(data)
