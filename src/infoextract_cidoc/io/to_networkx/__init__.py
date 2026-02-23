"""
NetworkX integration utilities for CIDOC CRM entities.

This module provides conversion from CRM entities to NetworkX graphs
and social network analysis capabilities.
"""

from .graph_builder import (
    to_networkx_graph,
    build_graph_from_entities,
    add_relationships_to_graph,
    create_temporal_graph,
)
from .analysis import (
    calculate_centrality_measures,
    find_communities,
    analyze_temporal_patterns,
    get_network_statistics,
)
from .converters import (
    entities_to_networkx,
    relationships_to_edges,
    extract_node_attributes,
    extract_edge_attributes,
)

__all__ = [
    "to_networkx_graph",
    "build_graph_from_entities", 
    "add_relationships_to_graph",
    "create_temporal_graph",
    "calculate_centrality_measures",
    "find_communities",
    "analyze_temporal_patterns",
    "get_network_statistics",
    "entities_to_networkx",
    "relationships_to_edges",
    "extract_node_attributes",
    "extract_edge_attributes",
]
