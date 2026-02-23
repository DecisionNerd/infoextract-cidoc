"""Unit tests for CRM mapping layer."""

import uuid

import pytest

from infoextract_cidoc.extraction.lite_schema import (
    LiteEntity,
    LiteExtractionResult,
    LiteRelationship,
)
from infoextract_cidoc.extraction.crm_mapper import map_to_crm_entities
from infoextract_cidoc.extraction.resolution import resolve_extraction
from infoextract_cidoc.models.base import CRMEntity, CRMRelation


@pytest.fixture()
def sample_extraction_result():
    lite_result = LiteExtractionResult(
        entities=[
            LiteEntity(ref_id="person_1", entity_type="Person", label="Einstein"),
            LiteEntity(ref_id="place_1", entity_type="Place", label="Ulm"),
        ],
        relationships=[
            LiteRelationship(
                source_ref="person_1",
                target_ref="place_1",
                property_code="P98",
                property_label="was born",
            ),
        ],
    )
    return resolve_extraction(lite_result)


@pytest.mark.unit
class TestMapToCrmEntities:
    def test_returns_crm_entities(self, sample_extraction_result) -> None:
        entities, relations = map_to_crm_entities(sample_extraction_result)
        assert len(entities) == 2
        assert all(isinstance(e, CRMEntity) for e in entities)

    def test_returns_crm_relations(self, sample_extraction_result) -> None:
        entities, relations = map_to_crm_entities(sample_extraction_result)
        assert len(relations) == 1
        assert all(isinstance(r, CRMRelation) for r in relations)

    def test_entity_class_codes(self, sample_extraction_result) -> None:
        entities, _ = map_to_crm_entities(sample_extraction_result)
        codes = {e.class_code for e in entities}
        assert "E21" in codes
        assert "E53" in codes

    def test_relation_property_code(self, sample_extraction_result) -> None:
        _, relations = map_to_crm_entities(sample_extraction_result)
        assert relations[0].type == "P98"

    def test_entity_labels_preserved(self, sample_extraction_result) -> None:
        entities, _ = map_to_crm_entities(sample_extraction_result)
        labels = {e.label for e in entities}
        assert "Einstein" in labels
        assert "Ulm" in labels

    def test_empty_result(self) -> None:
        from infoextract_cidoc.extraction.models import ExtractionResult
        empty = ExtractionResult(entities=[], relationships=[])
        entities, relations = map_to_crm_entities(empty)
        assert entities == []
        assert relations == []
