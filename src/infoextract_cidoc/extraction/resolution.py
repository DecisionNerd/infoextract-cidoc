"""Entity and relationship resolution pipeline.

Two-stage pipeline:
  Stage A: Register all LiteEntities, assign stable UUIDs, produce ExtractedEntity list
  Stage B: Resolve LiteRelationships against the registry, reject broken links
"""

from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING

from infoextract_cidoc.extraction.models import (
    EventExtraction,
    ExtractedEntity,
    ExtractedRelationship,
    ExtractionResult,
    ObjectExtraction,
    PersonExtraction,
    PlaceExtraction,
    TimeExtraction,
)

if TYPE_CHECKING:
    from infoextract_cidoc.extraction.lite_schema import (
        LiteEntity,
        LiteExtractionResult,
    )

logger = logging.getLogger(__name__)

# Stable namespace for UUID5 generation
_EXTRACTION_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

# Map entity_type strings to ExtractedEntity subclasses and class_codes
_ENTITY_TYPE_MAP: dict[str, tuple[type[ExtractedEntity], str]] = {
    "Person": (PersonExtraction, "E21"),
    "Event": (EventExtraction, "E5"),
    "Place": (PlaceExtraction, "E53"),
    "Object": (ObjectExtraction, "E22"),
    "TimeSpan": (TimeExtraction, "E52"),
}

# Default values for required fields on ExtractedEntity subclasses
_SUBCLASS_DEFAULTS: dict[type[ExtractedEntity], dict[str, str]] = {
    EventExtraction: {"event_type": "unknown"},
    PlaceExtraction: {"place_type": "unknown"},
    ObjectExtraction: {"object_type": "unknown"},
    TimeExtraction: {"time_type": "unknown"},
}


def _stable_uuid(ref_id: str, label: str) -> uuid.UUID:
    """Generate a stable UUID5 from ref_id and label."""
    return uuid.uuid5(_EXTRACTION_NAMESPACE, f"{ref_id}:{label}")


def _make_extracted_entity(lite: LiteEntity) -> ExtractedEntity:
    """Convert a LiteEntity to an ExtractedEntity subclass."""
    entity_cls, class_code = _ENTITY_TYPE_MAP.get(
        lite.entity_type, (ExtractedEntity, "E55")
    )
    stable_id = _stable_uuid(lite.ref_id, lite.label)

    # Build kwargs, supplying defaults for required subclass fields
    kwargs: dict = {
        "id": stable_id,
        "class_code": class_code,
        "label": lite.label,
        "description": lite.description,
        "confidence": lite.confidence,
        "source_text": lite.source_snippet,
        "properties": lite.attributes,
    }

    # Merge defaults for required fields, allowing attributes to override
    defaults = _SUBCLASS_DEFAULTS.get(entity_cls, {})
    for field_name, default_value in defaults.items():
        kwargs[field_name] = lite.attributes.get(field_name, default_value)

    return entity_cls(**kwargs)


class EntityRegistry:
    """Maps ref_ids to stable ExtractedEntity instances."""

    def __init__(self) -> None:
        self._by_ref_id: dict[str, ExtractedEntity] = {}
        self._by_label: dict[str, ExtractedEntity] = {}

    def register(self, lite: LiteEntity) -> ExtractedEntity:
        """Register a LiteEntity, deduplicating by label if needed."""
        # Deduplication: if same label exists, return existing entity
        if lite.label in self._by_label:
            existing = self._by_label[lite.label]
            self._by_ref_id[lite.ref_id] = existing
            return existing

        entity = _make_extracted_entity(lite)
        self._by_ref_id[lite.ref_id] = entity
        self._by_label[lite.label] = entity
        return entity

    def resolve(self, ref_id: str) -> ExtractedEntity | None:
        """Resolve a ref_id to an ExtractedEntity, or None if not found."""
        return self._by_ref_id.get(ref_id)

    @property
    def entities(self) -> list[ExtractedEntity]:
        """Return all unique registered entities."""
        # Use label dedup: _by_label values are unique
        seen_ids: set[uuid.UUID] = set()
        result: list[ExtractedEntity] = []
        for entity in self._by_label.values():
            if entity.id not in seen_ids:
                seen_ids.add(entity.id)
                result.append(entity)
        return result


def resolve_extraction(lite_result: LiteExtractionResult) -> ExtractionResult:
    """Resolve a LiteExtractionResult into a full ExtractionResult.

    Stage A: Register all entities, assign stable UUIDs.
    Stage B: Resolve relationships, log and exclude broken links.

    Args:
        lite_result: The raw LangStruct extraction output.

    Returns:
        ExtractionResult with stable UUIDs and resolved relationships.
    """
    registry = EntityRegistry()

    # Stage A: Register all entities
    for lite_entity in lite_result.entities:
        registry.register(lite_entity)

    entities = registry.entities

    # Stage B: Resolve relationships
    relationships: list[ExtractedRelationship] = []
    for lite_rel in lite_result.relationships:
        source = registry.resolve(lite_rel.source_ref)
        target = registry.resolve(lite_rel.target_ref)

        if source is None:
            logger.warning(
                "Broken relationship: source_ref %r not found in registry. Skipping.",
                lite_rel.source_ref,
            )
            continue

        if target is None:
            logger.warning(
                "Broken relationship: target_ref %r not found in registry. Skipping.",
                lite_rel.target_ref,
            )
            continue

        relationships.append(
            ExtractedRelationship(
                source_id=source.id,
                target_id=target.id,
                property_code=lite_rel.property_code,
                property_label=lite_rel.property_label,
                confidence=lite_rel.confidence,
                source_text=lite_rel.source_snippet,
            )
        )

    return ExtractionResult(entities=entities, relationships=relationships)
