"""
Social network analysis utilities for CIDOC CRM graphs.

This module provides analysis functions for NetworkX graphs containing
CRM entities and relationships.
"""

from collections import defaultdict
from typing import Any

import networkx as nx


def calculate_centrality_measures(
    graph: nx.Graph,
    *,
    include_betweenness: bool = True,
    include_closeness: bool = True,
    include_eigenvector: bool = True,
    include_pagerank: bool = True,
) -> dict[str, dict[str, float]]:
    """
    Calculate various centrality measures for nodes in the graph.

    Args:
        graph: NetworkX graph
        include_betweenness: Whether to calculate betweenness centrality
        include_closeness: Whether to calculate closeness centrality
        include_eigenvector: Whether to calculate eigenvector centrality
        include_pagerank: Whether to calculate PageRank centrality

    Returns:
        Dictionary mapping centrality type to node centrality scores
    """
    centrality_measures = {}

    # Degree centrality
    centrality_measures["degree"] = nx.degree_centrality(graph)

    # Betweenness centrality
    if include_betweenness:
        try:
            centrality_measures["betweenness"] = nx.betweenness_centrality(graph)
        except nx.NetworkXError:
            centrality_measures["betweenness"] = {}

    # Closeness centrality
    if include_closeness:
        try:
            centrality_measures["closeness"] = nx.closeness_centrality(graph)
        except nx.NetworkXError:
            centrality_measures["closeness"] = {}

    # Eigenvector centrality
    if include_eigenvector:
        try:
            centrality_measures["eigenvector"] = nx.eigenvector_centrality(graph)
        except nx.NetworkXError:
            centrality_measures["eigenvector"] = {}

    # PageRank
    if include_pagerank:
        try:
            centrality_measures["pagerank"] = nx.pagerank(graph)
        except nx.NetworkXError:
            centrality_measures["pagerank"] = {}

    return centrality_measures


def find_communities(
    graph: nx.Graph,
    *,
    algorithm: str = "greedy_modularity",
    min_community_size: int = 2,
) -> list[list[str]]:
    """
    Find communities in the graph using various algorithms.

    Args:
        graph: NetworkX graph
        algorithm: Community detection algorithm to use
        min_community_size: Minimum size for communities to include

    Returns:
        List of communities, where each community is a list of node IDs
    """
    communities = []

    if algorithm == "greedy_modularity":
        try:
            communities = list(nx.community.greedy_modularity_communities(graph))
        except nx.NetworkXError:
            communities = []
    elif algorithm == "label_propagation":
        try:
            communities = list(nx.community.label_propagation_communities(graph))
        except nx.NetworkXError:
            communities = []
    elif algorithm == "asyn_lpa":
        try:
            communities = list(nx.community.asyn_lpa_communities(graph))
        except nx.NetworkXError:
            communities = []
    else:
        msg = f"Unknown community detection algorithm: {algorithm}"
        raise ValueError(msg)

    # Filter communities by minimum size
    return [
        list(community)
        for community in communities
        if len(community) >= min_community_size
    ]



def analyze_temporal_patterns(
    graph: nx.Graph,
    *,
    time_attribute: str = "temporal_info",
) -> dict[str, Any]:
    """
    Analyze temporal patterns in the graph.

    Args:
        graph: NetworkX graph with temporal attributes
        time_attribute: Name of the temporal attribute

    Returns:
        Dictionary containing temporal analysis results
    """
    temporal_analysis = {
        "nodes_with_temporal_info": 0,
        "temporal_coverage": 0.0,
        "time_span": None,
        "temporal_clusters": [],
    }

    nodes_with_time = 0
    time_values = []

    for node_id in graph.nodes():
        node_data = graph.nodes[node_id]
        if node_data.get("has_temporal_info", False):
            nodes_with_time += 1
            temporal_info = node_data.get(time_attribute)
            if temporal_info:
                time_values.append(temporal_info)

    temporal_analysis["nodes_with_temporal_info"] = nodes_with_time
    temporal_analysis["temporal_coverage"] = (
        nodes_with_time / len(graph.nodes()) if graph.nodes() else 0
    )

    # Analyze time span if we have temporal data
    if time_values:
        # This would need more sophisticated temporal parsing in practice
        temporal_analysis["time_span"] = {
            "earliest": min(time_values),
            "latest": max(time_values),
            "count": len(time_values),
        }

    return temporal_analysis


def get_network_statistics(graph: nx.Graph) -> dict[str, Any]:
    """
    Get comprehensive network statistics for the graph.

    Args:
        graph: NetworkX graph

    Returns:
        Dictionary containing network statistics
    """
    stats = {
        "basic_metrics": {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "density": nx.density(graph),
            "is_connected": nx.is_connected(graph) if not graph.is_directed() else None,
            "is_strongly_connected": nx.is_strongly_connected(graph)
            if graph.is_directed()
            else None,
            "is_weakly_connected": nx.is_weakly_connected(graph)
            if graph.is_directed()
            else None,
        }
    }

    # Node degree statistics
    degrees = dict(graph.degree())
    if degrees:
        degree_values = list(degrees.values())
        stats["degree_stats"] = {
            "min_degree": min(degree_values),
            "max_degree": max(degree_values),
            "avg_degree": sum(degree_values) / len(degree_values),
            "degree_distribution": list(nx.degree_histogram(graph)),
        }

    # Entity type distribution
    entity_types = defaultdict(int)
    for node_id in graph.nodes():
        node_data = graph.nodes[node_id]
        class_code = node_data.get("class_code", "Unknown")
        entity_types[class_code] += 1

    stats["entity_type_distribution"] = dict(entity_types)

    # Relationship type distribution
    relationship_types = defaultdict(int)
    for edge in graph.edges(data=True):
        edge_data = edge[2]
        property_code = edge_data.get("property_code", "Unknown")
        relationship_types[property_code] += 1

    stats["relationship_type_distribution"] = dict(relationship_types)

    # Connectivity metrics
    if graph.number_of_nodes() > 0:
        try:
            stats["connectivity"] = {
                "average_clustering": nx.average_clustering(graph),
                "transitivity": nx.transitivity(graph),
            }
        except nx.NetworkXError:
            stats["connectivity"] = {}

    return stats


def get_most_central_nodes(
    graph: nx.Graph,
    centrality_measures: dict[str, dict[str, float]],
    *,
    top_k: int = 10,
) -> dict[str, list[tuple[str, float]]]:
    """
    Get the most central nodes for each centrality measure.

    Args:
        graph: NetworkX graph
        centrality_measures: Dictionary of centrality measures
        top_k: Number of top nodes to return for each measure

    Returns:
        Dictionary mapping centrality type to list of (node_id, score) tuples
    """
    top_nodes = {}

    for measure_name, scores in centrality_measures.items():
        if scores:
            # Sort by score (descending) and take top k
            sorted_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top_nodes[measure_name] = sorted_nodes[:top_k]
        else:
            top_nodes[measure_name] = []

    return top_nodes


def analyze_node_importance(
    graph: nx.Graph,
    node_id: str,
    *,
    include_neighbors: bool = True,
    include_paths: bool = True,
) -> dict[str, Any]:
    """
    Analyze the importance and role of a specific node in the network.

    Args:
        graph: NetworkX graph
        node_id: ID of the node to analyze
        include_neighbors: Whether to include neighbor analysis
        include_paths: Whether to include path analysis

    Returns:
        Dictionary containing node importance analysis
    """
    if not graph.has_node(node_id):
        return {"error": "Node not found in graph"}

    analysis = {
        "node_id": node_id,
        "node_data": dict(graph.nodes[node_id]),
        "degree": graph.degree(node_id),
    }

    # Neighbor analysis
    if include_neighbors:
        neighbors = list(graph.neighbors(node_id))
        analysis["neighbors"] = {
            "count": len(neighbors),
            "neighbor_ids": neighbors,
            "neighbor_types": [
                graph.nodes[n].get("class_code", "Unknown") for n in neighbors
            ],
        }

    # Path analysis
    if include_paths and graph.number_of_nodes() > 1:
        try:
            # Calculate shortest paths to all other nodes
            paths = nx.single_source_shortest_path_length(graph, node_id)
            analysis["paths"] = {
                "reachable_nodes": len(paths) - 1,  # Exclude self
                "average_path_length": sum(paths.values()) / len(paths) if paths else 0,
                "max_path_length": max(paths.values()) if paths else 0,
            }
        except nx.NetworkXError:
            analysis["paths"] = {"error": "Path analysis failed"}

    return analysis
