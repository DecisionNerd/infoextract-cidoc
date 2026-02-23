"""
Cypher emitters for CIDOC CRM entities.
Generates idempotent MERGE/UNWIND scripts for Neo4j and Memgraph.
"""

from collections.abc import Iterable
from typing import Any

from infoextract_cidoc.models.base import CRMEntity
from infoextract_cidoc.properties import P


def emit_nodes(entities: Iterable[CRMEntity]) -> dict[str, list[dict[str, Any]]]:
    """
    Emit node data for Cypher script generation.

    Args:
        entities: Iterable of CRM entities

    Returns:
        Dictionary with 'nodes' key containing node data
    """
    nodes = []
    for entity in entities:
        node_data = {
            "id": str(entity.id),  # Convert UUID to string for Cypher
            "class_code": entity.class_code,
            "label": entity.label,
            "notes": entity.notes,
            "type": entity.type,
        }
        # Remove None values
        node_data = {k: v for k, v in node_data.items() if v is not None}
        nodes.append(node_data)

    return {"nodes": nodes}


def emit_relationships(
    entities: Iterable[CRMEntity],
) -> dict[str, list[dict[str, Any]]]:
    """
    Emit relationship data for Cypher script generation.

    Args:
        entities: Iterable of CRM entities

    Returns:
        Dictionary with 'rels' key containing relationship data
    """
    rels = []
    for entity in entities:
        # Expand shortcut fields to relationships
        shortcut_rels = expand_shortcuts(entity)
        rels.extend(shortcut_rels)

        # Handle class-specific relationship collections
        if hasattr(entity, "participants"):
            for participant in entity.participants:
                rels.append(
                    {
                        "src": str(entity.id),  # Convert UUID to string
                        "type": "P11_HAD_PARTICIPANT",
                        "tgt": str(participant),  # Convert UUID to string
                    }
                )

    return {"rels": rels}


def expand_shortcuts(entity: CRMEntity) -> list[dict[str, Any]]:
    """
    Expand shortcut fields to full CRM relationships.

    Args:
        entity: CRM entity with potential shortcut fields

    Returns:
        List of relationship dictionaries
    """
    rels = []

    # Map shortcut fields to P-properties
    shortcut_mapping = {
        "timespan": "P4",
        "took_place_at": "P7",
        "current_location": "P53",
        "produced_by": "P108",
        "begin_of_the_begin": "P79",
        "end_of_the_end": "P80",
    }

    for shortcut_field, p_code in shortcut_mapping.items():
        if hasattr(entity, shortcut_field):
            target_id = getattr(entity, shortcut_field)
            if target_id:
                rels.append(
                    {
                        "src": str(entity.id),  # Convert UUID to string
                        "type": f"{p_code}_{P[p_code]['aliases'][0]}",
                        "tgt": str(target_id),  # Convert UUID to string
                    }
                )

    return rels


def generate_cypher_script(
    entities: Iterable[CRMEntity],
    *,
    include_constraints: bool = True,
    batch_size: int = 1000,
) -> str:
    """
    Generate a complete Cypher script for entities.

    Args:
        entities: Iterable of CRM entities
        include_constraints: Whether to include constraint creation
        batch_size: Batch size for UNWIND operations

    Returns:
        Complete Cypher script as string
    """
    # Get node and relationship data
    node_data = emit_nodes(entities)
    rel_data = emit_relationships(entities)

    script_parts = []

    # Add constraints if requested
    if include_constraints:
        script_parts.append(_generate_constraints())

    # Add node creation
    if node_data["nodes"]:
        script_parts.append(_generate_node_script(node_data["nodes"], batch_size))

    # Add relationship creation
    if rel_data["rels"]:
        script_parts.append(_generate_relationship_script(rel_data["rels"], batch_size))

    return "\n\n".join(script_parts)


def _generate_constraints() -> str:
    """Generate constraint creation statements."""
    return """-- Create constraints
CREATE CONSTRAINT crm_id IF NOT EXISTS FOR (n:CRM) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT crm_class_code IF NOT EXISTS FOR (n:CRM) REQUIRE n.class_code IS NOT NULL;"""


def _generate_node_script(nodes: list[dict[str, Any]], batch_size: int) -> str:
    """Generate node creation script."""
    if not nodes:
        return ""

    script_parts = ["-- Create nodes"]

    # Process nodes in batches
    for i in range(0, len(nodes), batch_size):
        nodes[i : i + batch_size]
        script_parts.append(f"UNWIND $nodes_{i // batch_size} AS n")
        script_parts.append("MERGE (x:CRM {id: n.id})")
        script_parts.append("SET x.label = coalesce(n.label, x.label)")
        script_parts.append("SET x.class_code = n.class_code")
        script_parts.append("SET x.notes = coalesce(n.notes, x.notes)")
        script_parts.append("SET x.type = coalesce(n.type, x.type);")
        script_parts.append("")

    return "\n".join(script_parts)


def _generate_relationship_script(rels: list[dict[str, Any]], batch_size: int) -> str:
    """Generate relationship creation script."""
    if not rels:
        return ""

    # Group relationships by type
    rels_by_type = {}
    for rel in rels:
        rel_type = rel["type"]
        if rel_type not in rels_by_type:
            rels_by_type[rel_type] = []
        rels_by_type[rel_type].append(rel)

    script_parts = ["-- Create relationships"]

    for rel_type, type_rels in rels_by_type.items():
        # Process relationships in batches
        for i in range(0, len(type_rels), batch_size):
            type_rels[i : i + batch_size]
            script_parts.append(f"UNWIND $rels_{rel_type}_{i // batch_size} AS r")
            script_parts.append("MATCH (s:CRM {id: r.src})")
            script_parts.append("MATCH (t:CRM {id: r.tgt})")
            script_parts.append(f"MERGE (s)-[:`{rel_type}`]->(t);")
            script_parts.append("")

    return "\n".join(script_parts)


def generate_cypher_parameters(
    entities: Iterable[CRMEntity], *, batch_size: int = 1000
) -> dict[str, Any]:
    """
    Generate Cypher parameters for the script.

    Args:
        entities: Iterable of CRM entities
        batch_size: Batch size for parameter grouping

    Returns:
        Dictionary of parameters for Cypher execution
    """
    node_data = emit_nodes(entities)
    rel_data = emit_relationships(entities)

    params = {}

    # Add node parameters
    if node_data["nodes"]:
        for i in range(0, len(node_data["nodes"]), batch_size):
            batch = node_data["nodes"][i : i + batch_size]
            params[f"nodes_{i // batch_size}"] = batch

    # Add relationship parameters
    if rel_data["rels"]:
        rels_by_type = {}
        for rel in rel_data["rels"]:
            rel_type = rel["type"]
            if rel_type not in rels_by_type:
                rels_by_type[rel_type] = []
            rels_by_type[rel_type].append(rel)

        for rel_type, type_rels in rels_by_type.items():
            for i in range(0, len(type_rels), batch_size):
                batch = type_rels[i : i + batch_size]
                params[f"rels_{rel_type}_{i // batch_size}"] = batch

    return params


def validate_cypher_script(script: str) -> list[str]:
    """
    Validate a Cypher script for common issues.

    Args:
        script: Cypher script to validate

    Returns:
        List of validation warnings/errors
    """
    issues = []

    # Check for basic syntax issues
    if not script.strip():
        issues.append("Empty script")

    # Check for proper MERGE usage
    if "CREATE" in script and "MERGE" not in script:
        issues.append(
            "Consider using MERGE instead of CREATE for idempotent operations"
        )

    # Check for proper parameter usage
    if "UNWIND" in script and not any("$" in line for line in script.split("\n")):
        issues.append("UNWIND statements should use parameters")

    return issues


def format_cypher_script(script: str) -> str:
    """
    Format a Cypher script for better readability.

    Args:
        script: Raw Cypher script

    Returns:
        Formatted Cypher script
    """
    lines = script.split("\n")
    formatted_lines = []
    indent_level = 0

    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append("")
            continue

        # Decrease indent for closing statements
        if line.startswith(("END", "}")):
            indent_level = max(0, indent_level - 1)

        # Add indentation
        formatted_line = "  " * indent_level + line
        formatted_lines.append(formatted_line)

        # Increase indent for opening statements
        if line.endswith((":", "{")):
            indent_level += 1

    return "\n".join(formatted_lines)
