"""
PydanticAI models for information extraction from text.

These models define the structure for extracting CIDOC CRM entities and relationships
from unstructured text using AI-powered analysis.
"""

from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ExtractedEntity(BaseModel):
    """Base class for extracted CRM entities."""

    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    class_code: str = Field(..., description="CIDOC CRM E-class code")
    label: str = Field(..., description="Human-readable label")
    description: str | None = Field(None, description="Detailed description")
    confidence: float = Field(
        0.0, ge=0.0, le=1.0, description="Extraction confidence score"
    )
    source_text: str | None = Field(None, description="Original text snippet")
    properties: dict[str, Any] = Field(
        default_factory=dict, description="Additional properties"
    )


class ExtractedRelationship(BaseModel):
    """Represents a relationship between two extracted entities."""

    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    source_id: UUID = Field(..., description="Source entity ID")
    target_id: UUID = Field(..., description="Target entity ID")
    property_code: str = Field(..., description="CIDOC CRM P-property code")
    property_label: str = Field(..., description="Human-readable property label")
    confidence: float = Field(
        0.0, ge=0.0, le=1.0, description="Extraction confidence score"
    )
    source_text: str | None = Field(None, description="Original text snippet")
    properties: dict[str, Any] = Field(
        default_factory=dict, description="Additional properties"
    )


class ExtractionResult(BaseModel):
    """Complete result of information extraction from text."""

    entities: list[ExtractedEntity] = Field(default_factory=list)
    relationships: list[ExtractedRelationship] = Field(default_factory=list)
    extraction_metadata: dict[str, Any] = Field(default_factory=dict)

    def get_entities_by_class(self, class_code: str) -> list[ExtractedEntity]:
        """Get all entities of a specific CRM class."""
        return [e for e in self.entities if e.class_code == class_code]

    def get_relationships_by_property(
        self, property_code: str
    ) -> list[ExtractedRelationship]:
        """Get all relationships of a specific CRM property."""
        return [r for r in self.relationships if r.property_code == property_code]


# Specialized extraction models for different entity types


class PersonExtraction(ExtractedEntity):
    """Extracted person entity with biographical information."""

    class_code: str = "E21"
    birth_date: str | None = Field(None, description="Birth date")
    death_date: str | None = Field(None, description="Death date")
    birth_place: str | None = Field(None, description="Birth place")
    death_place: str | None = Field(None, description="Death place")
    occupation: str | None = Field(None, description="Primary occupation")
    nationality: str | None = Field(None, description="Nationality")
    parents: list[str] = Field(default_factory=list, description="Parent names")
    children: list[str] = Field(default_factory=list, description="Children names")
    spouses: list[str] = Field(default_factory=list, description="Spouse names")


class EventExtraction(ExtractedEntity):
    """Extracted event entity with temporal and contextual information."""

    class_code: str = "E5"
    event_type: str = Field(..., description="Type of event")
    start_date: str | None = Field(None, description="Event start date")
    end_date: str | None = Field(None, description="Event end date")
    location: str | None = Field(None, description="Event location")
    participants: list[str] = Field(
        default_factory=list, description="Event participants"
    )
    cause: str | None = Field(None, description="Event cause")
    result: str | None = Field(None, description="Event result")


class PlaceExtraction(ExtractedEntity):
    """Extracted place entity with geographical information."""

    class_code: str = "E53"
    place_type: str = Field(..., description="Type of place")
    coordinates: str | None = Field(None, description="Geographical coordinates")
    country: str | None = Field(None, description="Country")
    region: str | None = Field(None, description="Region or state")
    city: str | None = Field(None, description="City")
    address: str | None = Field(None, description="Specific address")


class ObjectExtraction(ExtractedEntity):
    """Extracted object entity with material and cultural information."""

    class_code: str = "E22"
    object_type: str = Field(..., description="Type of object")
    material: str | None = Field(None, description="Primary material")
    creator: str | None = Field(None, description="Creator or maker")
    creation_date: str | None = Field(None, description="Creation date")
    current_location: str | None = Field(None, description="Current location")
    dimensions: str | None = Field(None, description="Physical dimensions")
    condition: str | None = Field(None, description="Current condition")


class TimeExtraction(ExtractedEntity):
    """Extracted time entity with temporal information."""

    class_code: str = "E52"
    time_type: str = Field(..., description="Type of time period")
    start_date: str | None = Field(None, description="Period start")
    end_date: str | None = Field(None, description="Period end")
    duration: str | None = Field(None, description="Duration description")
    calendar: str | None = Field(None, description="Calendar system")
    precision: str | None = Field(None, description="Temporal precision")
