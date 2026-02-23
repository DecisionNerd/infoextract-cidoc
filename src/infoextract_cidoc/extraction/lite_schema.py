"""Lite entity schema for LangStruct extraction output.

These are the schemas the LLM fills in during extraction. They use simple
string ref_ids (not UUIDs) so the LLM can consistently reference entities
in relationship definitions. UUID assignment happens in the resolution layer.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class LiteEntity(BaseModel):
    """A lightweight entity extracted from text, pre-UUID assignment."""

    ref_id: str = Field(
        description="Short identifier for this entity (e.g. 'person_1', 'place_2'). "
        "Used in relationships to reference this entity. Must be unique within an extraction."
    )
    entity_type: str = Field(
        description="CIDOC CRM entity type. One of: Person, Event, Place, Object, TimeSpan"
    )
    label: str = Field(description="Human-readable name or label for this entity.")
    description: str | None = Field(
        default=None,
        description="Optional description or notes about this entity.",
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score for this extraction (0.0 to 1.0). "
        "Use 0.7-1.0 for directly stated facts, 0.3-0.6 for inferences.",
    )
    source_snippet: str | None = Field(
        default=None,
        description="The relevant text snippet from the source that supports this entity.",
    )
    attributes: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional attributes specific to the entity type.",
    )


class LiteRelationship(BaseModel):
    """A lightweight relationship between two extracted entities."""

    source_ref: str = Field(description="The ref_id of the source entity.")
    target_ref: str = Field(description="The ref_id of the target entity.")
    property_code: str = Field(
        description="CIDOC CRM property code (e.g. 'P98', 'P7', 'P14')."
    )
    property_label: str = Field(
        description="Human-readable label for the property (e.g. 'was born', 'took place at')."
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score for this relationship (0.0 to 1.0).",
    )


class LiteExtractionResult(BaseModel):
    """The complete result of a single LangStruct extraction pass."""

    entities: list[LiteEntity] = Field(
        default_factory=list,
        description="All entities extracted from the text.",
    )
    relationships: list[LiteRelationship] = Field(
        default_factory=list,
        description="All relationships between extracted entities.",
    )
    overall_confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Overall confidence score for the entire extraction.",
    )
