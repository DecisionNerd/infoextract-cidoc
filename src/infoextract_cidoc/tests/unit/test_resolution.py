"""Unit tests for entity and relationship resolution pipeline."""

import pytest

from infoextract_cidoc.extraction.lite_schema import (
    LiteEntity,
    LiteExtractionResult,
    LiteRelationship,
)
from infoextract_cidoc.extraction.resolution import EntityRegistry, resolve_extraction


@pytest.mark.unit
class TestEntityRegistry:
    def test_register_entity(self) -> None:
        registry = EntityRegistry()
        lite = LiteEntity(ref_id="person_1", entity_type="Person", label="Einstein")
        entity = registry.register(lite)
        assert entity.label == "Einstein"
        assert entity.class_code == "E21"

    def test_stable_uuid(self) -> None:
        registry1 = EntityRegistry()
        registry2 = EntityRegistry()
        lite = LiteEntity(ref_id="person_1", entity_type="Person", label="Einstein")
        e1 = registry1.register(lite)
        e2 = registry2.register(lite)
        assert e1.id == e2.id  # deterministic UUID5

    def test_deduplication_by_label(self) -> None:
        registry = EntityRegistry()
        lite1 = LiteEntity(ref_id="person_1", entity_type="Person", label="Einstein")
        lite2 = LiteEntity(ref_id="person_2", entity_type="Person", label="Einstein")
        e1 = registry.register(lite1)
        e2 = registry.register(lite2)
        assert e1.id == e2.id  # same entity
        assert len(registry.entities) == 1

    def test_resolve_by_ref_id(self) -> None:
        registry = EntityRegistry()
        lite = LiteEntity(ref_id="place_1", entity_type="Place", label="Ulm")
        registry.register(lite)
        resolved = registry.resolve("place_1")
        assert resolved is not None
        assert resolved.label == "Ulm"

    def test_resolve_missing_returns_none(self) -> None:
        registry = EntityRegistry()
        assert registry.resolve("nonexistent") is None


@pytest.mark.unit
class TestResolveExtraction:
    def test_basic_resolution(self) -> None:
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
        result = resolve_extraction(lite_result)
        assert len(result.entities) == 2
        assert len(result.relationships) == 1

    def test_broken_source_ref_excluded(self) -> None:
        lite_result = LiteExtractionResult(
            entities=[
                LiteEntity(ref_id="place_1", entity_type="Place", label="Ulm"),
            ],
            relationships=[
                LiteRelationship(
                    source_ref="nonexistent",
                    target_ref="place_1",
                    property_code="P98",
                    property_label="was born",
                ),
            ],
        )
        result = resolve_extraction(lite_result)
        assert len(result.entities) == 1
        assert len(result.relationships) == 0  # broken link excluded

    def test_broken_target_ref_excluded(self) -> None:
        lite_result = LiteExtractionResult(
            entities=[
                LiteEntity(ref_id="person_1", entity_type="Person", label="Einstein"),
            ],
            relationships=[
                LiteRelationship(
                    source_ref="person_1",
                    target_ref="nonexistent",
                    property_code="P98",
                    property_label="was born",
                ),
            ],
        )
        result = resolve_extraction(lite_result)
        assert len(result.relationships) == 0

    def test_entity_type_mapping(self) -> None:
        lite_result = LiteExtractionResult(
            entities=[
                LiteEntity(ref_id="person_1", entity_type="Person", label="P"),
                LiteEntity(ref_id="event_1", entity_type="Event", label="E"),
                LiteEntity(ref_id="place_1", entity_type="Place", label="Pl"),
                LiteEntity(ref_id="object_1", entity_type="Object", label="O"),
                LiteEntity(ref_id="time_1", entity_type="TimeSpan", label="T"),
            ],
        )
        result = resolve_extraction(lite_result)
        codes = {e.class_code for e in result.entities}
        assert codes == {"E21", "E5", "E53", "E22", "E52"}
