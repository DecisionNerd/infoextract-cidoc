"""Unit tests for LiteExtractionResult schema."""

import pytest

from infoextract_cidoc.extraction.lite_schema import (
    LiteEntity,
    LiteExtractionResult,
    LiteRelationship,
)


@pytest.mark.unit
class TestLiteEntity:
    def test_valid_entity(self) -> None:
        entity = LiteEntity(
            ref_id="person_1",
            entity_type="Person",
            label="Albert Einstein",
            confidence=0.95,
        )
        assert entity.ref_id == "person_1"
        assert entity.label == "Albert Einstein"
        assert entity.confidence == 0.95

    def test_confidence_bounds(self) -> None:
        with pytest.raises(Exception):
            LiteEntity(
                ref_id="person_1",
                entity_type="Person",
                label="Test",
                confidence=1.5,  # out of range
            )

    def test_defaults(self) -> None:
        entity = LiteEntity(
            ref_id="place_1",
            entity_type="Place",
            label="Warsaw",
        )
        assert entity.confidence == 1.0
        assert entity.description is None
        assert entity.attributes == {}


@pytest.mark.unit
class TestLiteRelationship:
    def test_valid_relationship(self) -> None:
        rel = LiteRelationship(
            source_ref="person_1",
            target_ref="place_1",
            property_code="P98",
            property_label="was born",
            confidence=0.9,
        )
        assert rel.source_ref == "person_1"
        assert rel.property_code == "P98"


@pytest.mark.unit
class TestLiteExtractionResult:
    def test_empty_result(self) -> None:
        result = LiteExtractionResult()
        assert result.entities == []
        assert result.relationships == []
        assert result.overall_confidence == 1.0

    def test_with_entities_and_relationships(self) -> None:
        result = LiteExtractionResult(
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
        assert len(result.entities) == 2
        assert len(result.relationships) == 1
