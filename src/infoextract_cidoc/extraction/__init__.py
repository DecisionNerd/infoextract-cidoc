"""
AI-powered information extraction module for CIDOC CRM entities.

Pipeline:
    LangStructExtractor -> resolve_extraction -> map_to_crm_entities
"""

from .crm_mapper import map_to_crm_entities
from .langstruct_extractor import LangStructExtractor
from .lite_schema import LiteEntity, LiteExtractionResult, LiteRelationship
from .models import (
    EventExtraction,
    ExtractedEntity,
    ExtractedRelationship,
    ExtractionResult,
    ObjectExtraction,
    PersonExtraction,
    PlaceExtraction,
    TimeExtraction,
)
from .resolution import EntityRegistry, resolve_extraction

__all__ = [
    "EntityRegistry",
    "EventExtraction",
    # Stable extraction models (output of resolution pipeline)
    "ExtractedEntity",
    "ExtractedRelationship",
    "ExtractionResult",
    # Extraction pipeline
    "LangStructExtractor",
    "LiteEntity",
    # Lite schema (LangStruct output)
    "LiteExtractionResult",
    "LiteRelationship",
    "ObjectExtraction",
    "PersonExtraction",
    "PlaceExtraction",
    "TimeExtraction",
    "map_to_crm_entities",
    "resolve_extraction",
]
