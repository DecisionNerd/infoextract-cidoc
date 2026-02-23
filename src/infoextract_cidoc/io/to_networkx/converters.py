"""
Utility functions for converting between CRM entities and NetworkX formats.

This module provides helper functions for data conversion and attribute extraction.
"""

from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

import networkx as nx

from infoextract_cidoc.models.base import CRMEntity, CRMRelation
from infoextract_cidoc.extraction.models import ExtractedEntity, ExtractedRelationship


def entities_to_networkx(
    entities: List[CRMEntity],
    *,
    node_id_field: str = "id",
    label_field: str = "label",
    include_all_attributes: bool = True,
) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Convert CRM entities to NetworkX node format.
    
    Args:
        entities: List of CRM entities
        node_id_field: Field to use as node ID
        label_field: Field to use as node label
        include_all_attributes: Whether to include all entity attributes
        
    Returns:
        Tuple of (node_ids, node_data_list)
    """
    node_ids = []
    node_data_list = []
    
    for entity in entities:
        # Get node ID
        node_id = str(getattr(entity, node_id_field))
        node_ids.append(node_id)
        
        # Get node data
        node_data = {
            "class_code": entity.class_code,
            "label": getattr(entity, label_field, None),
        }
        
        if include_all_attributes:
            entity_dict = entity.dict()
            for key, value in entity_dict.items():
                if key not in [node_id_field, "class_code"]:
                    node_data[key] = value
        
        node_data_list.append(node_data)
    
    return node_ids, node_data_list


def relationships_to_edges(
    relationships: List[CRMRelation],
    *,
    include_properties: bool = True,
) -> List[Tuple[str, str, Dict[str, Any]]]:
    """
    Convert CRM relationships to NetworkX edge format.
    
    Args:
        relationships: List of CRM relationships
        include_properties: Whether to include relationship properties
        
    Returns:
        List of (source_id, target_id, edge_data) tuples
    """
    edges = []
    
    for rel in relationships:
        edge_data = {
            "property_code": rel.type,
        }
        
        if include_properties and rel.props:
            edge_data.update(rel.props)
        
        edges.append((
            str(rel.src),
            str(rel.tgt),
            edge_data
        ))
    
    return edges


def extract_node_attributes(
    graph: nx.Graph,
    attribute_name: str,
    *,
    default_value: Any = None,
) -> Dict[str, Any]:
    """
    Extract a specific attribute from all nodes in the graph.
    
    Args:
        graph: NetworkX graph
        attribute_name: Name of the attribute to extract
        default_value: Default value for nodes without the attribute
        
    Returns:
        Dictionary mapping node_id to attribute value
    """
    attributes = {}
    
    for node_id in graph.nodes():
        node_data = graph.nodes[node_id]
        attributes[node_id] = node_data.get(attribute_name, default_value)
    
    return attributes


def extract_edge_attributes(
    graph: nx.Graph,
    attribute_name: str,
    *,
    default_value: Any = None,
) -> Dict[Tuple[str, str], Any]:
    """
    Extract a specific attribute from all edges in the graph.
    
    Args:
        graph: NetworkX graph
        attribute_name: Name of the attribute to extract
        default_value: Default value for edges without the attribute
        
    Returns:
        Dictionary mapping (source_id, target_id) to attribute value
    """
    attributes = {}
    
    for edge in graph.edges(data=True):
        source, target, edge_data = edge
        attributes[(source, target)] = edge_data.get(attribute_name, default_value)
    
    return attributes


def filter_graph_by_attribute(
    graph: nx.Graph,
    attribute_name: str,
    attribute_value: Any,
    *,
    filter_nodes: bool = True,
    filter_edges: bool = False,
) -> nx.Graph:
    """
    Filter graph to include only nodes/edges with specific attribute values.
    
    Args:
        graph: Original NetworkX graph
        attribute_name: Name of the attribute to filter on
        attribute_value: Value to filter for
        filter_nodes: Whether to filter nodes
        filter_edges: Whether to filter edges
        
    Returns:
        Filtered NetworkX graph
    """
    filtered_graph = graph.copy()
    
    # Filter nodes
    if filter_nodes:
        nodes_to_remove = []
        for node_id in filtered_graph.nodes():
            node_data = filtered_graph.nodes[node_id]
            if node_data.get(attribute_name) != attribute_value:
                nodes_to_remove.append(node_id)
        
        filtered_graph.remove_nodes_from(nodes_to_remove)
    
    # Filter edges
    if filter_edges:
        edges_to_remove = []
        for edge in filtered_graph.edges(data=True):
            source, target, edge_data = edge
            if edge_data.get(attribute_name) != attribute_value:
                edges_to_remove.append((source, target))
        
        filtered_graph.remove_edges_from(edges_to_remove)
    
    return filtered_graph


def get_subgraph_by_entity_type(
    graph: nx.Graph,
    entity_type: str,
    *,
    include_relationships: bool = True,
) -> nx.Graph:
    """
    Get a subgraph containing only nodes of a specific entity type.
    
    Args:
        graph: Original NetworkX graph
        entity_type: CRM class code to filter for
        include_relationships: Whether to include relationships between filtered nodes
        
    Returns:
        Subgraph containing only the specified entity type
    """
    # Find nodes of the specified type
    nodes_of_type = []
    for node_id in graph.nodes():
        node_data = graph.nodes[node_id]
        if node_data.get("class_code") == entity_type:
            nodes_of_type.append(node_id)
    
    # Create subgraph
    if include_relationships:
        subgraph = graph.subgraph(nodes_of_type)
    else:
        subgraph = nx.Graph()
        subgraph.add_nodes_from([(node_id, graph.nodes[node_id]) for node_id in nodes_of_type])
    
    return subgraph


def convert_extracted_to_networkx(
    extracted_entities: List[ExtractedEntity],
    extracted_relationships: List[ExtractedRelationship],
    *,
    min_confidence: float = 0.5,
) -> nx.Graph:
    """
    Convert extracted entities and relationships to a NetworkX graph.
    
    Args:
        extracted_entities: List of extracted entities
        extracted_relationships: List of extracted relationships
        min_confidence: Minimum confidence threshold
        
    Returns:
        NetworkX graph from extracted data
    """
    graph = nx.DiGraph()
    
    # Add entities as nodes
    for entity in extracted_entities:
        if entity.confidence >= min_confidence:
            graph.add_node(
                str(entity.id),
                class_code=entity.class_code,
                label=entity.label,
                description=entity.description,
                confidence=entity.confidence,
                source_text=entity.source_text,
                **entity.properties
            )
    
    # Add relationships as edges
    for rel in extracted_relationships:
        if (rel.confidence >= min_confidence and 
            graph.has_node(str(rel.source_id)) and 
            graph.has_node(str(rel.target_id))):
            
            graph.add_edge(
                str(rel.source_id),
                str(rel.target_id),
                property_code=rel.property_code,
                property_label=rel.property_label,
                confidence=rel.confidence,
                source_text=rel.source_text,
                **rel.properties
            )
    
    return graph


def merge_graphs(
    graphs: List[nx.Graph],
    *,
    merge_strategy: str = "union",
) -> nx.Graph:
    """
    Merge multiple NetworkX graphs.
    
    Args:
        graphs: List of NetworkX graphs to merge
        merge_strategy: Strategy for merging ("union", "intersection")
        
    Returns:
        Merged NetworkX graph
    """
    if not graphs:
        return nx.Graph()
    
    if len(graphs) == 1:
        return graphs[0]
    
    merged_graph = graphs[0].copy()
    
    for graph in graphs[1:]:
        if merge_strategy == "union":
            merged_graph = nx.compose(merged_graph, graph)
        elif merge_strategy == "intersection":
            merged_graph = nx.intersection(merged_graph, graph)
        else:
            raise ValueError(f"Unknown merge strategy: {merge_strategy}")
    
    return merged_graph


def export_graph_to_dataframe(
    graph: nx.Graph,
    *,
    include_node_attributes: bool = True,
    include_edge_attributes: bool = True,
) -> Tuple[Any, Any]:
    """
    Export NetworkX graph to pandas DataFrames.
    
    Args:
        graph: NetworkX graph
        include_node_attributes: Whether to include node attributes
        include_edge_attributes: Whether to include edge attributes
        
    Returns:
        Tuple of (nodes_df, edges_df) DataFrames
    """
    import pandas as pd
    
    # Export nodes
    nodes_data = []
    for node_id in graph.nodes():
        node_data = {"node_id": node_id}
        if include_node_attributes:
            node_data.update(graph.nodes[node_id])
        nodes_data.append(node_data)
    
    nodes_df = pd.DataFrame(nodes_data)
    
    # Export edges
    edges_data = []
    for edge in graph.edges(data=True):
        source, target, edge_data = edge
        edge_row = {"source": source, "target": target}
        if include_edge_attributes:
            edge_row.update(edge_data)
        edges_data.append(edge_row)
    
    edges_df = pd.DataFrame(edges_data)
    
    return nodes_df, edges_df
