"""
Markdown renderers for CIDOC CRM entities.
Provides card, detailed, table, and narrative rendering styles.
"""

from enum import Enum
from typing import Any
from uuid import UUID

from infoextract_cidoc.models.base import CRMEntity


class MarkdownStyle(str, Enum):
    """Available Markdown rendering styles."""

    CARD = "card"
    DETAILED = "detailed"
    TABLE = "table"
    NARRATIVE = "narrative"


def to_markdown(
    entity: CRMEntity,
    style: MarkdownStyle = MarkdownStyle.CARD,
    *,
    aliases: dict[str, str] | None = None,
    show_codes: bool = True,
) -> str:
    """
    Render a CRM entity to Markdown.

    Args:
        entity: The CRM entity to render
        style: Rendering style (card, detailed, table, narrative)
        aliases: Optional alias mapping for friendly names
        show_codes: Whether to show E/P codes in output

    Returns:
        Markdown string representation
    """
    if style == MarkdownStyle.CARD:
        return _render_card(entity, aliases, show_codes)
    if style == MarkdownStyle.DETAILED:
        return _render_detailed(entity, aliases, show_codes)
    if style == MarkdownStyle.TABLE:
        return _render_table([entity], aliases, show_codes)
    if style == MarkdownStyle.NARRATIVE:
        return _render_narrative(entity, aliases, show_codes)
    msg = f"Unknown style: {style}"
    raise ValueError(msg)


def render_table(
    entities: list[CRMEntity],
    columns: list[str] | None = None,
    *,
    aliases: dict[str, str] | None = None,
    show_codes: bool = True,
) -> str:
    """
    Render multiple entities as a Markdown table.

    Args:
        entities: List of CRM entities to render
        columns: Optional list of columns to include
        aliases: Optional alias mapping for friendly names
        show_codes: Whether to show E/P codes in output

    Returns:
        Markdown table string
    """
    return _render_table(entities, aliases, show_codes, columns)


def _render_card(
    entity: CRMEntity, aliases: dict[str, str] | None, show_codes: bool
) -> str:
    """Render entity as a card-style Markdown."""
    # Get friendly class name
    class_name = _get_friendly_class_name(entity.class_code, aliases)

    # Build header
    header_parts = [entity.class_code, class_name]
    if entity.label:
        header_parts.append(entity.label)
    header_parts.append(f"({_format_uuid_for_display(entity.id)})")

    header = "### " + " · ".join(header_parts)

    # Build body with canonical fields
    body_lines = []
    canonical_fields = _get_canonical_fields(entity)

    for field in canonical_fields:
        value = _get_field_value(entity, field)
        if value:
            friendly_name = _get_friendly_property_name(field, aliases)
            formatted_value = _format_uuid_for_display(value)
            if show_codes:
                body_lines.append(
                    f"- **{friendly_name}** (`{field}`): {formatted_value}"
                )
            else:
                body_lines.append(f"- **{friendly_name}**: {formatted_value}")

    # Add notes if present
    if entity.notes:
        body_lines.append(f"- **Notes**: {entity.notes}")

    return header + "\n\n" + "\n".join(body_lines)


def _render_detailed(
    entity: CRMEntity, aliases: dict[str, str] | None, show_codes: bool
) -> str:
    """Render entity in detailed format with all non-empty fields."""
    # Get friendly class name
    class_name = _get_friendly_class_name(entity.class_code, aliases)

    # Build header
    header = f"## {entity.class_code} · {class_name}"
    if entity.label:
        header += f" — {entity.label}"
    header += f" ({_format_uuid_for_display(entity.id)})"

    # Build detailed body
    body_lines = []

    # Add all non-empty fields
    for field_name, field_value in entity.dict().items():
        if field_value and field_name not in ["id", "class_code"]:
            friendly_name = _get_friendly_property_name(field_name, aliases)
            formatted_value = _format_uuid_for_display(field_value)
            if show_codes:
                body_lines.append(
                    f"- **{friendly_name}** (`{field_name}`): {formatted_value}"
                )
            else:
                body_lines.append(f"- **{friendly_name}**: {formatted_value}")

    return header + "\n\n" + "\n".join(body_lines)


def _render_table(
    entities: list[CRMEntity],
    _aliases: dict[str, str] | None,
    _show_codes: bool,
    columns: list[str] | None = None,
) -> str:
    """Render entities as a Markdown table."""
    if not entities:
        return "No entities to display."

    # Determine columns
    if columns is None:
        columns = ["id", "class_code", "label", "type"]

    # Build header
    header_row = "| " + " | ".join(columns) + " |"
    separator_row = "| " + " | ".join(["---"] * len(columns)) + " |"

    # Build data rows
    data_rows = []
    for entity in entities:
        row_values = []
        for col in columns:
            value = _get_field_value(entity, col)
            if value is None:
                value = ""
            elif isinstance(value, list):
                value = ", ".join(_format_uuid_for_display(v) for v in value)
            else:
                value = _format_uuid_for_display(value)
            row_values.append(value)
        data_rows.append("| " + " | ".join(row_values) + " |")

    return "\n".join([header_row, separator_row, *data_rows])


def _render_narrative(
    entity: CRMEntity, aliases: dict[str, str] | None, _show_codes: bool
) -> str:
    """Render entity as a narrative (especially useful for events)."""
    # Get friendly class name
    class_name = _get_friendly_class_name(entity.class_code, aliases)

    # Build narrative
    narrative_parts = []

    if entity.label:
        narrative_parts.append(f"**{entity.label}**")

    narrative_parts.append(f"is a {class_name.lower()}")

    if entity.class_code in ["E5", "E7", "E8", "E12"]:
        # Event-specific narrative
        if hasattr(entity, "timespan") and entity.timespan:
            narrative_parts.append(
                f"that occurred during {_format_uuid_for_display(entity.timespan)}"
            )

        if hasattr(entity, "took_place_at") and entity.took_place_at:
            narrative_parts.append(
                f"at {_format_uuid_for_display(entity.took_place_at)}"
            )

    elif entity.class_code == "E22":
        # Human-made object narrative
        if hasattr(entity, "produced_by") and entity.produced_by:
            narrative_parts.append(
                f"that was produced by {_format_uuid_for_display(entity.produced_by)}"
            )

        if hasattr(entity, "current_location") and entity.current_location:
            narrative_parts.append(
                f"currently located at {_format_uuid_for_display(entity.current_location)}"
            )

    narrative = " ".join(narrative_parts) + "."

    # Add additional details
    if entity.notes:
        narrative += f"\n\n{entity.notes}"

    return narrative


def _get_friendly_class_name(class_code: str, aliases: dict[str, str] | None) -> str:
    """Get friendly class name from aliases or use default."""
    if aliases and class_code in aliases:
        return aliases[class_code]

    # Default mapping for common classes
    default_aliases = {
        "E1": "CRM Entity",
        "E5": "Event",
        "E7": "Activity",
        "E8": "Acquisition",
        "E12": "Production",
        "E21": "Person",
        "E22": "Human-Made Object",
        "E53": "Place",
        "E52": "Time-Span",
        "E42": "Identifier",
        "E35": "Title",
    }

    return default_aliases.get(class_code, f"E{class_code}")


def _get_friendly_property_name(
    property_name: str, aliases: dict[str, str] | None
) -> str:
    """Get friendly property name from aliases or use default."""
    if aliases and property_name in aliases:
        return aliases[property_name]

    # Default mapping for common properties
    default_aliases = {
        "label": "Label",
        "type": "Type",
        "notes": "Notes",
        "timespan": "Time-Span",
        "took_place_at": "Location",
        "current_location": "Location",
        "produced_by": "Produced By",
        "begin_of_the_begin": "Start",
        "end_of_the_end": "End",
    }

    return default_aliases.get(property_name, property_name.replace("_", " ").title())


def _get_canonical_fields(entity: CRMEntity) -> list[str]:
    """Get canonical fields for an entity based on its class."""
    # This would ideally come from the class metadata
    # For now, use a simple mapping
    canonical_mapping = {
        "E5": ["label", "type", "timespan", "took_place_at"],
        "E7": ["label", "type", "timespan", "took_place_at"],
        "E8": ["label", "type", "timespan", "took_place_at"],
        "E12": ["label", "type", "timespan", "took_place_at"],
        "E21": ["label", "type", "current_location"],
        "E22": ["label", "type", "current_location", "produced_by"],
        "E53": ["label", "type"],
        "E52": ["label", "type", "begin_of_the_begin", "end_of_the_end"],
        "E42": ["label", "type"],
        "E35": ["label", "type"],
    }

    return canonical_mapping.get(entity.class_code, ["label", "type"])


def _get_field_value(entity: CRMEntity, field_name: str) -> Any:
    """Get field value from entity, handling both direct attributes and shortcut fields."""
    if hasattr(entity, field_name):
        return getattr(entity, field_name)
    return None


def _format_uuid_for_display(uuid_value: Any) -> str:
    """Format UUID for display in Markdown."""
    if isinstance(uuid_value, UUID):
        # Show first 8 characters for readability
        return str(uuid_value)[:8] + "..."
    if isinstance(uuid_value, str):
        try:
            # Try to parse as UUID
            uuid_obj = UUID(uuid_value)
            return str(uuid_obj)[:8] + "..."
        except ValueError:
            # Not a UUID, return as-is
            return uuid_value
    return str(uuid_value)
