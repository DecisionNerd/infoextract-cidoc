"""
NetworkX graph construction from CIDOC CRM entities.

This module provides utilities to convert CRM entities and relationships
into NetworkX graphs for social network analysis.
"""

from typing import Any

import networkx as nx

from infoextract_cidoc.extraction.models import ExtractionResult
from infoextract_cidoc.models.base import CRMEntity, CRMRelation


def to_networkx_graph(
    entities: list[CRMEntity],
    relationships: list[CRMRelation] | None = None,
    *,
    directed: bool = True,
    multigraph: bool = False,
    include_attributes: bool = True,
) -> nx.Graph:
    """
    Convert CRM entities and relationships to a NetworkX graph.

    Args:
        entities: List of CRM entities to include as nodes
        relationships: Optional list of relationships to include as edges
        directed: Whether to create a directed graph
        multigraph: Whether to allow multiple edges between same nodes
        include_attributes: Whether to include entity attributes as node data

    Returns:
        NetworkX graph with entities as nodes and relationships as edges
    """
    # Create appropriate graph type
    if directed:
        graph = nx.MultiDiGraph() if multigraph else nx.DiGraph()
    elif multigraph:
        graph = nx.MultiGraph()
    else:
        graph = nx.Graph()

    # Add nodes (entities)
    for entity in entities:
        node_data = {}
        if include_attributes:
            node_data.update(
                {
                    "class_code": entity.class_code,
                    "label": entity.label,
                    "notes": entity.notes,
                    "type": entity.type,
                }
            )
            # Add any additional attributes
            node_data.update(
                {
                    k: v
                    for k, v in entity.dict().items()
                    if k not in ["id", "class_code", "label", "notes", "type"]
                }
            )

        graph.add_node(str(entity.id), **node_data)

    # Add edges (relationships)
    if relationships:
        for rel in relationships:
            edge_data = {
                "property_code": rel.type,
                "properties": rel.props or {},
            }

            graph.add_edge(str(rel.src), str(rel.tgt), **edge_data)

    return graph


def build_graph_from_entities(
    entities: list[CRMEntity],
    *,
    expand_shortcuts: bool = True,
    include_self_loops: bool = False,
) -> nx.Graph:
    """
    Build a NetworkX graph from CRM entities, automatically expanding shortcut relationships.

    Args:
        entities: List of CRM entities
        expand_shortcuts: Whether to expand shortcut fields into relationships
        include_self_loops: Whether to include self-loops in the graph

    Returns:
        NetworkX graph with expanded relationships
    """
    graph = nx.DiGraph()

    # Add all entities as nodes
    for entity in entities:
        graph.add_node(
            str(entity.id),
            class_code=entity.class_code,
            label=entity.label,
            notes=entity.notes,
            type=entity.type,
        )

    # Expand shortcut relationships if requested
    if expand_shortcuts:
        relationships = []
        for entity in entities:
            shortcut_rels = _expand_entity_shortcuts(entity)
            relationships.extend(shortcut_rels)

        # Add relationships as edges
        for rel in relationships:
            if not include_self_loops and rel["src"] == rel["tgt"]:
                continue

            graph.add_edge(
                rel["src"],
                rel["tgt"],
                property_code=rel["type"],
                properties=rel.get("props", {}),
            )

    return graph


def add_relationships_to_graph(
    graph: nx.Graph,
    relationships: list[CRMRelation],
    *,
    update_existing: bool = True,
) -> nx.Graph:
    """
    Add relationships to an existing NetworkX graph.

    Args:
        graph: Existing NetworkX graph
        relationships: List of relationships to add
        update_existing: Whether to update existing edges

    Returns:
        Updated NetworkX graph
    """
    for rel in relationships:
        edge_data = {
            "property_code": rel.type,
            "properties": rel.props or {},
        }

        if update_existing or not graph.has_edge(str(rel.src), str(rel.tgt)):
            graph.add_edge(str(rel.src), str(rel.tgt), **edge_data)

    return graph


def create_temporal_graph(
    entities: list[CRMEntity],
    relationships: list[CRMRelation] | None = None,
    *,
    time_attribute: str = "timespan",
) -> nx.Graph:
    """
    Create a temporal NetworkX graph with time-based attributes.

    Args:
        entities: List of CRM entities
        relationships: Optional list of relationships
        time_attribute: Attribute name for temporal information

    Returns:
        NetworkX graph with temporal attributes
    """
    graph = to_networkx_graph(entities, relationships)

    # Add temporal attributes to nodes
    for node_id in graph.nodes():
        node_data = graph.nodes[node_id]

        # Extract temporal information if available
        if hasattr(node_data, time_attribute):
            temporal_info = getattr(node_data, time_attribute)
            if temporal_info:
                node_data["temporal_info"] = temporal_info
                node_data["has_temporal_info"] = True
        else:
            node_data["has_temporal_info"] = False

    return graph


def _expand_entity_shortcuts(entity: CRMEntity) -> list[dict[str, Any]]:
    """Expand shortcut fields in an entity to full relationships."""
    relationships = []

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
                relationships.append(
                    {
                        "src": str(entity.id),
                        "type": p_code,
                        "tgt": str(target_id),
                        "props": {"shortcut_field": shortcut_field},
                    }
                )

    return relationships


# Utility functions for working with extracted entities


def extraction_result_to_networkx(
    extraction_result: ExtractionResult,
    *,
    min_confidence: float = 0.5,
    include_relationships: bool = True,
) -> nx.Graph:
    """
    Convert an extraction result to a NetworkX graph.

    Args:
        extraction_result: Result from AI extraction
        min_confidence: Minimum confidence threshold for including entities
        include_relationships: Whether to include relationships as edges

    Returns:
        NetworkX graph from extraction result
    """
    graph = nx.DiGraph()

    # Add high-confidence entities as nodes
    for entity in extraction_result.entities:
        if entity.confidence >= min_confidence:
            graph.add_node(
                str(entity.id),
                class_code=entity.class_code,
                label=entity.label,
                description=entity.description,
                confidence=entity.confidence,
                source_text=entity.source_text,
                **entity.properties,
            )

    # Add relationships as edges
    if include_relationships:
        for rel in extraction_result.relationships:
            if (
                rel.confidence >= min_confidence
                and graph.has_node(str(rel.source_id))
                and graph.has_node(str(rel.target_id))
            ):
                graph.add_edge(
                    str(rel.source_id),
                    str(rel.target_id),
                    property_code=rel.property_code,
                    property_label=rel.property_label,
                    confidence=rel.confidence,
                    source_text=rel.source_text,
                    **rel.properties,
                )

    return graph
