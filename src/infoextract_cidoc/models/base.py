"""
Base CRM entity model and core wrappers.
Provides the foundation for all CIDOC CRM E-class models.
"""

import hashlib
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

_UUID_NAMESPACE = UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # DNS namespace


def _deterministic_uuid(value: str) -> UUID:
    """Return a deterministic UUID derived from *value* via MD5."""
    return UUID(
        hashlib.md5(
            f"{_UUID_NAMESPACE}{value}".encode(), usedforsecurity=False
        ).hexdigest()
    )


class CRMEntity(BaseModel):
    """
    Base class for all CIDOC CRM entities.

    Every CRM entity has:
    - id: unique identifier (UUID)
    - class_code: E-number (e.g., "E22")
    - label: human-readable name
    - notes: additional textual information
    - type: list of type assignments
    """

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Base CIDOC CRM entity",
            "examples": [
                {
                    "id": "obj_001",
                    "class_code": "E22",
                    "label": "Ancient Vase",
                    "type": ["E55:Vessel", "E55:Ceramic"],
                }
            ],
        }
    )

    id: UUID = Field(
        default_factory=uuid4, description="Unique identifier for this entity"
    )
    class_code: str = Field(..., description="CIDOC CRM E-class code")
    label: str | None = Field(None, description="Human-readable label")
    notes: str | None = Field(None, description="Additional textual notes")
    source_text: str | None = Field(
        None,
        description="Source text snippet from which this entity was extracted",
    )
    type: list[str] = Field(default_factory=list, description="Type assignments")

    @field_validator("id", mode="before")
    @classmethod
    def convert_string_to_uuid(cls, v: Any) -> Any:
        """Convert string IDs to UUIDs for backward compatibility."""
        if isinstance(v, str):
            try:
                return UUID(v)
            except ValueError:
                return _deterministic_uuid(v)
        return v


class CRMRelation(BaseModel):
    """
    Represents a relationship between two CRM entities.

    Used internally for relationship expansion and Cypher emission.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "description": "CRM relationship between entities",
            "examples": [
                {
                    "src": "obj_001",
                    "type": "P108",
                    "tgt": "prod_001",
                    "props": {"role": "E55:Painter"},
                }
            ],
        }
    )

    src: UUID = Field(..., description="Source entity ID")
    type: str = Field(..., description="P-property code (e.g., 'P108')")
    tgt: UUID = Field(..., description="Target entity ID")
    props: dict[str, Any] | None = Field(
        None, description="Additional relationship properties"
    )
    source_text: str | None = Field(
        None,
        description="Source text snippet from which this relationship was extracted",
    )

    @field_validator("src", "tgt", mode="before")
    @classmethod
    def convert_string_to_uuid(cls, v: Any) -> Any:
        """Convert string IDs to UUIDs for backward compatibility."""
        if isinstance(v, str):
            try:
                return UUID(v)
            except ValueError:
                return _deterministic_uuid(v)
        return v


class CRMValidationError(Exception):
    """Raised when CRM validation rules are violated."""


class CRMValidationWarning(Warning):
    """Issued when CRM validation rules are violated but severity is set to warn."""
