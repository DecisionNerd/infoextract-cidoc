"""
NetworkX integration utilities for CIDOC CRM entities.

This module provides conversion from CRM entities to NetworkX graphs
and social network analysis capabilities.
"""

from .analysis import (
    analyze_temporal_patterns,
    calculate_centrality_measures,
    find_communities,
    get_network_statistics,
)
from .converters import (
    entities_to_networkx,
    extract_edge_attributes,
    extract_node_attributes,
    relationships_to_edges,
)
from .graph_builder import (
    add_relationships_to_graph,
    build_graph_from_entities,
    create_temporal_graph,
    to_networkx_graph,
)

__all__ = [
    "add_relationships_to_graph",
    "analyze_temporal_patterns",
    "build_graph_from_entities",
    "calculate_centrality_measures",
    "create_temporal_graph",
    "entities_to_networkx",
    "extract_edge_attributes",
    "extract_node_attributes",
    "find_communities",
    "get_network_statistics",
    "relationships_to_edges",
    "to_networkx_graph",
]
