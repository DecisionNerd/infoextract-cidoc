"""
Unit tests for Markdown renderers.
"""

from uuid import uuid4

from ...io.to_markdown import MarkdownStyle, render_table, to_markdown
from ...models.generated.e_classes import (
    E12_Production,
    E22_HumanMadeObject,
)


class TestMarkdownRendering:
    """Test Markdown rendering functionality."""

    def test_card_rendering(self):
        """Test card-style rendering."""
        entity = E22_HumanMadeObject(
            id=uuid4(),
            class_code="E22",
            label="Ancient Vase",
            type=["E55:Vessel"],
            current_location=uuid4(),
            produced_by=uuid4(),
        )

        markdown = to_markdown(entity, MarkdownStyle.CARD)

        # Check that key elements are present
        assert "### E22 · Human-Made Object · Ancient Vase" in markdown
        assert "(" in markdown and ")" in markdown  # Should have UUID in parentheses
        assert "**Location** (`current_location`):" in markdown
        assert "**Produced By** (`produced_by`):" in markdown

    def test_detailed_rendering(self):
        """Test detailed-style rendering."""
        entity = E22_HumanMadeObject(
            id=uuid4(),
            class_code="E22",
            label="Ancient Vase",
            type=["E55:Vessel"],
            notes="A beautiful amphora",
        )

        markdown = to_markdown(entity, MarkdownStyle.DETAILED)

        # Check that key elements are present
        assert "## E22 · Human-Made Object — Ancient Vase" in markdown
        assert "(" in markdown and ")" in markdown  # Should have UUID in parentheses
        assert "**Label** (`label`): Ancient Vase" in markdown
        assert "**Notes** (`notes`): A beautiful amphora" in markdown

    def test_table_rendering(self):
        """Test table-style rendering."""
        entities = [
            E22_HumanMadeObject(id=uuid4(), class_code="E22", label="Vase 1"),
            E22_HumanMadeObject(id=uuid4(), class_code="E22", label="Vase 2"),
        ]

        markdown = render_table(entities)

        # Check that table structure is present
        assert "| id | class_code | label | type |" in markdown
        assert "| --- | --- | --- | --- |" in markdown
        assert "| E22 | Vase 1 |" in markdown
        assert "| E22 | Vase 2 |" in markdown

    def test_narrative_rendering(self):
        """Test narrative-style rendering."""
        entity = E12_Production(
            id=uuid4(),
            class_code="E12",
            label="Vase Production",
            timespan=uuid4(),
            took_place_at=uuid4(),
        )

        markdown = to_markdown(entity, MarkdownStyle.NARRATIVE)

        # Check that narrative elements are present
        assert "**Vase Production**" in markdown
        assert "is a production" in markdown
        assert "that occurred during" in markdown
        assert "at" in markdown

    def test_aliases_usage(self):
        """Test that aliases are used when provided."""
        entity = E22_HumanMadeObject(
            id=uuid4(), class_code="E22", label="Ancient Vase"
        )

        aliases = {"E22": "Artifact", "current_location": "Location"}

        markdown = to_markdown(entity, MarkdownStyle.CARD, aliases=aliases)

        # Check that aliases are used
        assert "### E22 · Artifact · Ancient Vase" in markdown
        assert "(" in markdown and ")" in markdown  # Should have UUID in parentheses

    def test_show_codes_option(self):
        """Test show_codes option."""
        entity = E22_HumanMadeObject(
            id=uuid4(), class_code="E22", label="Ancient Vase"
        )

        # With codes
        markdown_with_codes = to_markdown(entity, MarkdownStyle.CARD, show_codes=True)
        assert "**Label** (`label`): Ancient Vase" in markdown_with_codes

        # Without codes
        markdown_without_codes = to_markdown(
            entity, MarkdownStyle.CARD, show_codes=False
        )
        assert "**Label**: Ancient Vase" in markdown_without_codes
        assert "(`label`)" not in markdown_without_codes

    def test_empty_entity(self):
        """Test rendering of entity with minimal data."""
        entity = E22_HumanMadeObject(id=uuid4(), class_code="E22")

        markdown = to_markdown(entity, MarkdownStyle.CARD)

        # Should still render basic structure
        assert "### E22 · Human-Made Object" in markdown
        assert "(" in markdown and ")" in markdown  # Should have UUID in parentheses

    def test_custom_columns(self):
        """Test table rendering with custom columns."""
        entities = [
            E22_HumanMadeObject(id=uuid4(), class_code="E22", label="Vase 1"),
            E22_HumanMadeObject(id=uuid4(), class_code="E22", label="Vase 2"),
        ]

        custom_columns = ["id", "label"]
        markdown = render_table(entities, columns=custom_columns)

        # Check that only custom columns are present
        assert "| id | label |" in markdown
        assert "class_code" not in markdown
        assert "type" not in markdown

    def test_empty_entities_list(self):
        """Test table rendering with empty entities list."""
        markdown = render_table([])
        assert "No entities to display." in markdown
