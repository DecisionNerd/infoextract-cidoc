"""End-to-end pipeline integration tests: LiteExtractionResult -> outputs."""

import pytest

from infoextract_cidoc.extraction import (
    map_to_crm_entities,
    resolve_extraction,
)
from infoextract_cidoc.extraction.lite_schema import (
    LiteEntity,
    LiteExtractionResult,
    LiteRelationship,
)
from infoextract_cidoc.io.to_cypher import generate_cypher_script
from infoextract_cidoc.io.to_markdown import MarkdownStyle, render_table, to_markdown
from infoextract_cidoc.io.to_networkx import to_networkx_graph


@pytest.fixture
def einstein_lite_result() -> LiteExtractionResult:
    """Fixture simulating what LangStruct would extract from Einstein text."""
    return LiteExtractionResult(
        entities=[
            LiteEntity(
                ref_id="person_1",
                entity_type="Person",
                label="Albert Einstein",
                description="German-born theoretical physicist",
                confidence=0.99,
                source_snippet="Albert Einstein was born on March 14, 1879",
            ),
            LiteEntity(
                ref_id="place_1",
                entity_type="Place",
                label="Ulm",
                description="City in the Kingdom of Württemberg, Germany",
                confidence=0.98,
                source_snippet="born ... in Ulm",
            ),
            LiteEntity(
                ref_id="event_1",
                entity_type="Event",
                label="Birth of Albert Einstein",
                description="Birth event of Einstein",
                confidence=0.99,
                attributes={"event_type": "Birth"},
            ),
            LiteEntity(
                ref_id="timespan_1",
                entity_type="TimeSpan",
                label="March 14, 1879",
                confidence=0.99,
                attributes={"time_type": "Date"},
            ),
        ],
        relationships=[
            LiteRelationship(
                source_ref="person_1",
                target_ref="place_1",
                property_code="P98",
                property_label="was born",
                confidence=0.95,
            ),
            LiteRelationship(
                source_ref="event_1",
                target_ref="place_1",
                property_code="P7",
                property_label="took place at",
                confidence=0.92,
            ),
            LiteRelationship(
                source_ref="event_1",
                target_ref="timespan_1",
                property_code="P4",
                property_label="has time-span",
                confidence=0.99,
            ),
        ],
        overall_confidence=0.97,
    )


@pytest.mark.integration
class TestPipelineIntegration:
    def test_full_pipeline_entity_count(
        self, einstein_lite_result: LiteExtractionResult
    ) -> None:
        extraction_result = resolve_extraction(einstein_lite_result)
        entities, relations = map_to_crm_entities(extraction_result)
        assert len(entities) == 4
        assert len(relations) == 3

    def test_full_pipeline_entity_types(
        self, einstein_lite_result: LiteExtractionResult
    ) -> None:
        extraction_result = resolve_extraction(einstein_lite_result)
        entities, _ = map_to_crm_entities(extraction_result)
        codes = {e.class_code for e in entities}
        assert "E21" in codes  # Person
        assert "E53" in codes  # Place
        assert "E5" in codes  # Event
        assert "E52" in codes  # TimeSpan

    def test_full_pipeline_stable_ids(
        self, einstein_lite_result: LiteExtractionResult
    ) -> None:
        """Running the pipeline twice should produce the same UUIDs."""
        r1 = resolve_extraction(einstein_lite_result)
        r2 = resolve_extraction(einstein_lite_result)
        ids1 = {e.id for e in r1.entities}
        ids2 = {e.id for e in r2.entities}
        assert ids1 == ids2

    def test_pipeline_to_markdown(
        self, einstein_lite_result: LiteExtractionResult
    ) -> None:
        extraction_result = resolve_extraction(einstein_lite_result)
        entities, _ = map_to_crm_entities(extraction_result)
        for entity in entities:
            card = to_markdown(entity, MarkdownStyle.CARD)
            assert entity.label in card
        table = render_table(entities)
        assert "Albert Einstein" in table

    def test_pipeline_to_cypher(
        self, einstein_lite_result: LiteExtractionResult
    ) -> None:
        extraction_result = resolve_extraction(einstein_lite_result)
        entities, _ = map_to_crm_entities(extraction_result)
        cypher = generate_cypher_script(entities)
        assert "MERGE" in cypher or "CREATE" in cypher
        # The Cypher emitter uses parameterized queries; check for CRM structure
        assert "CRM" in cypher or "class_code" in cypher

    def test_pipeline_to_networkx(
        self, einstein_lite_result: LiteExtractionResult
    ) -> None:
        extraction_result = resolve_extraction(einstein_lite_result)
        entities, _ = map_to_crm_entities(extraction_result)
        graph = to_networkx_graph(entities)
        assert graph.number_of_nodes() == 4

    def test_pipeline_broken_links_excluded(self) -> None:
        """Broken relationship refs should be silently excluded."""
        lite_result = LiteExtractionResult(
            entities=[
                LiteEntity(ref_id="person_1", entity_type="Person", label="Einstein"),
            ],
            relationships=[
                LiteRelationship(
                    source_ref="person_1",
                    target_ref="nonexistent_ref",  # broken
                    property_code="P98",
                    property_label="was born",
                ),
            ],
        )
        extraction_result = resolve_extraction(lite_result)
        entities, relations = map_to_crm_entities(extraction_result)
        assert len(entities) == 1
        assert len(relations) == 0

    def test_extractor_exports(self) -> None:
        """Verify all expected symbols are exported from the extraction module."""
        from infoextract_cidoc import extraction

        assert hasattr(extraction, "LangStructExtractor")
        assert hasattr(extraction, "resolve_extraction")
        assert hasattr(extraction, "map_to_crm_entities")
        assert hasattr(extraction, "LiteExtractionResult")
        assert hasattr(extraction, "ExtractionResult")

    def test_source_text_propagates_to_crm(
        self, einstein_lite_result: LiteExtractionResult
    ) -> None:
        """source_snippet on LiteEntity/LiteRelationship must survive to CRM layer."""
        extraction_result = resolve_extraction(einstein_lite_result)

        # Verify source_text on ExtractedEntity
        person = next(e for e in extraction_result.entities if e.class_code == "E21")
        assert person.source_text == "Albert Einstein was born on March 14, 1879"

        place = next(e for e in extraction_result.entities if e.class_code == "E53")
        assert place.source_text == "born ... in Ulm"

        # Verify source_text on CRMEntity
        entities, _relations = map_to_crm_entities(extraction_result)
        crm_person = next(e for e in entities if e.class_code == "E21")
        assert crm_person.source_text == "Albert Einstein was born on March 14, 1879"

        crm_place = next(e for e in entities if e.class_code == "E53")
        assert crm_place.source_text == "born ... in Ulm"

        # Entities without source_snippet should have None
        crm_event = next(e for e in entities if e.class_code == "E5")
        assert crm_event.source_text is None

    def test_source_text_in_markdown_card(
        self, einstein_lite_result: LiteExtractionResult
    ) -> None:
        """source_text should appear as a blockquote in card-style Markdown."""
        extraction_result = resolve_extraction(einstein_lite_result)
        entities, _ = map_to_crm_entities(extraction_result)
        crm_person = next(e for e in entities if e.class_code == "E21")
        card = to_markdown(crm_person, MarkdownStyle.CARD)
        assert "Albert Einstein was born on March 14, 1879" in card
        assert card.count(">") >= 1  # blockquote present

    def test_source_text_in_cypher_script(
        self, einstein_lite_result: LiteExtractionResult
    ) -> None:
        """source_text should be emitted as a node property in Cypher output."""
        extraction_result = resolve_extraction(einstein_lite_result)
        entities, _ = map_to_crm_entities(extraction_result)
        cypher = generate_cypher_script(entities)
        assert "source_text" in cypher

    def test_relationship_source_text_propagates(self) -> None:
        """source_snippet on LiteRelationship must survive to CRMRelation."""
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
                    source_snippet="Einstein was born in Ulm",
                ),
            ],
        )
        extraction_result = resolve_extraction(lite_result)
        assert extraction_result.relationships[0].source_text == "Einstein was born in Ulm"

        _, crm_relations = map_to_crm_entities(extraction_result)
        assert crm_relations[0].source_text == "Einstein was born in Ulm"
