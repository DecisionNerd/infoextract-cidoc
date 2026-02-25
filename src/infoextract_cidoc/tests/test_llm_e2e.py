"""End-to-end LLM tests: raw text -> LangStructExtractor -> full pipeline outputs.

Requires a live Gemini API key. Run with:
    pytest -m llm
    GEMINI_API_KEY=<key> pytest -m llm -v

Skipped automatically when GEMINI_API_KEY / GOOGLE_API_KEY is absent.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from infoextract_cidoc.extraction import (
    LangStructExtractor,
    map_to_crm_entities,
    resolve_extraction,
)
from infoextract_cidoc.io.to_cypher import generate_cypher_script
from infoextract_cidoc.io.to_markdown import MarkdownStyle, to_markdown
from infoextract_cidoc.io.to_networkx import to_networkx_graph

_EINSTEIN_TEXT = (Path(__file__).parent.parent / "examples" / "einstein.md").read_text()


@pytest.fixture(scope="module", autouse=True)
def _require_api_key() -> None:
    """Skip this entire module if no Gemini API key is configured."""
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        pytest.skip("No Gemini API key available; set GEMINI_API_KEY or GOOGLE_API_KEY")


@pytest.fixture(scope="module")
def einstein_result():
    """Run the full pipeline on the Einstein biography (single LLM call per session)."""
    extractor = LangStructExtractor()
    lite = extractor.extract(_EINSTEIN_TEXT)
    resolved = resolve_extraction(lite)
    entities, relations = map_to_crm_entities(resolved)
    return lite, entities, relations


@pytest.mark.llm
class TestEinsteinEndToEnd:
    """Full pipeline tests driven by a live LLM on the Einstein biography."""

    def test_extraction_returns_entities(self, einstein_result) -> None:
        lite, _, _ = einstein_result
        assert len(lite.entities) >= 3, (
            f"Expected at least 3 lite entities, got {len(lite.entities)}"
        )

    def test_extraction_finds_einstein_person(self, einstein_result) -> None:
        lite, _, _ = einstein_result
        labels = [e.label for e in lite.entities]
        assert any("Einstein" in label for label in labels), (
            f"No entity with 'Einstein' in label; got: {labels}"
        )

    def test_extraction_has_person_entity_type(self, einstein_result) -> None:
        lite, _, _ = einstein_result
        types = [e.entity_type for e in lite.entities]
        assert "Person" in types, f"No Person entity type found; got: {types}"

    def test_extraction_has_relationships(self, einstein_result) -> None:
        lite, _, _ = einstein_result
        assert len(lite.relationships) >= 1, (
            f"Expected at least 1 relationship, got {len(lite.relationships)}"
        )

    def test_pipeline_entity_count(self, einstein_result) -> None:
        _, entities, _ = einstein_result
        assert len(entities) >= 3, (
            f"Expected at least 3 CRM entities, got {len(entities)}"
        )

    def test_pipeline_produces_e21_person(self, einstein_result) -> None:
        _, entities, _ = einstein_result
        class_codes = {e.class_code for e in entities}
        assert "E21" in class_codes, (
            f"Expected E21 (Person) in CRM output; got class codes: {class_codes}"
        )

    def test_pipeline_to_markdown(self, einstein_result) -> None:
        _, entities, _ = einstein_result
        for entity in entities:
            card = to_markdown(entity, MarkdownStyle.CARD)
            assert entity.label in card

    def test_pipeline_to_cypher(self, einstein_result) -> None:
        _, entities, _ = einstein_result
        cypher = generate_cypher_script(entities)
        assert "MERGE" in cypher or "CREATE" in cypher

    def test_pipeline_to_networkx(self, einstein_result) -> None:
        _, entities, _ = einstein_result
        graph = to_networkx_graph(entities)
        assert graph.number_of_nodes() >= 3
