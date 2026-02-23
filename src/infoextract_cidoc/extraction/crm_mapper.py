"""CRM mapping layer: ExtractedEntity/ExtractedRelationship -> CRMEntity/CRMRelation."""

from __future__ import annotations

from infoextract_cidoc.extraction.models import (
    EventExtraction,
    ExtractedEntity,
    ExtractionResult,
    ObjectExtraction,
    PersonExtraction,
    PlaceExtraction,
    TimeExtraction,
)
from infoextract_cidoc.models.base import CRMEntity, CRMRelation


def _entity_to_crm(entity: ExtractedEntity) -> CRMEntity:
    """Map an ExtractedEntity to a CRMEntity."""
    return CRMEntity(
        id=str(entity.id),
        class_code=entity.class_code,
        label=entity.label,
        notes=entity.description,
        type=[entity.class_code],
    )


def map_to_crm_entities(
    result: ExtractionResult,
) -> tuple[list[CRMEntity], list[CRMRelation]]:
    """Map an ExtractionResult to CRM entities and relations.

    Args:
        result: Resolved ExtractionResult from resolve_extraction().

    Returns:
        Tuple of (crm_entities, crm_relations).
    """
    crm_entities = [_entity_to_crm(e) for e in result.entities]

    crm_relations = [
        CRMRelation(
            src=rel.source_id,
            type=rel.property_code,
            tgt=rel.target_id,
        )
        for rel in result.relationships
    ]

    return crm_entities, crm_relations
