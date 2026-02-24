"""
Export utilities for network visualizations.

This module provides functions for exporting plots and creating
network summaries in various formats.
"""

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def export_plot(
    fig: plt.Figure,
    filepath: str,
    *,
    format: str = "png",
    dpi: int = 300,
    bbox_inches: str = "tight",
    transparent: bool = False,
) -> None:
    """
    Export matplotlib figure to file.

    Args:
        fig: Matplotlib figure object
        filepath: Output file path
        format: File format ("png", "pdf", "svg", "jpg")
        dpi: Resolution for raster formats
        bbox_inches: Bounding box for tight layout
        transparent: Whether to use transparent background

    Returns:
        None
    """
    # Ensure directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    # Save figure
    fig.savefig(
        filepath,
        format=format,
        dpi=dpi,
        bbox_inches=bbox_inches,
        transparent=transparent,
        facecolor="white" if not transparent else "none",
    )


def create_network_summary(
    graph: nx.Graph,
    *,
    include_statistics: bool = True,
    include_centrality: bool = True,
    include_communities: bool = True,
) -> dict[str, Any]:
    """
    Create a comprehensive summary of the network.

    Args:
        graph: NetworkX graph
        include_statistics: Whether to include basic statistics
        include_centrality: Whether to include centrality measures
        include_communities: Whether to include community detection

    Returns:
        Dictionary containing network summary
    """
    summary = {
        "network_info": {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "density": nx.density(graph),
            "is_connected": nx.is_connected(graph) if not graph.is_directed() else None,
        }
    }

    if include_statistics:
        summary["statistics"] = _get_network_statistics(graph)

    if include_centrality:
        summary["centrality"] = _get_centrality_summary(graph)

    if include_communities:
        summary["communities"] = _get_community_summary(graph)

    return summary


def export_network_data(
    graph: nx.Graph,
    filepath: str,
    *,
    format: str = "json",
    include_attributes: bool = True,
) -> None:
    """
    Export network data to file.

    Args:
        graph: NetworkX graph
        filepath: Output file path
        format: Export format ("json", "gexf", "graphml", "csv")
        include_attributes: Whether to include node/edge attributes

    Returns:
        None
    """
    # Ensure directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    if format == "json":
        # Export as JSON
        data = nx.node_link_data(graph)
        with Path(filepath).open("w") as f:
            json.dump(data, f, indent=2)

    elif format == "gexf":
        # Export as GEXF
        nx.write_gexf(graph, filepath)

    elif format == "graphml":
        # Export as GraphML
        nx.write_graphml(graph, filepath)

    elif format == "csv":
        # Export as CSV files
        _export_to_csv(graph, filepath, include_attributes)

    else:
        msg = f"Unsupported format: {format}"
        raise ValueError(msg)


def create_network_report(
    graph: nx.Graph,
    output_dir: str,
    *,
    include_plots: bool = True,
    include_data: bool = True,
    include_summary: bool = True,
) -> str:
    """
    Create a comprehensive network report with plots, data, and summary.

    Args:
        graph: NetworkX graph
        output_dir: Output directory for the report
        include_plots: Whether to include visualization plots
        include_data: Whether to include data exports
        include_summary: Whether to include summary statistics

    Returns:
        Path to the created report directory
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Create plots
    if include_plots:
        plots_dir = output_path / "plots"
        plots_dir.mkdir(exist_ok=True)

        # Basic network plot
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph)
        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=500,
            font_size=8,
            font_weight="bold",
        )
        plt.title("Network Overview")
        plt.tight_layout()
        plt.savefig(plots_dir / "network_overview.png", dpi=300, bbox_inches="tight")
        plt.close()

        # Degree distribution
        degrees = dict(graph.degree())
        degree_values = list(degrees.values())
        plt.figure(figsize=(10, 6))
        plt.hist(degree_values, bins=20, alpha=0.7, color="skyblue", edgecolor="black")
        plt.xlabel("Degree")
        plt.ylabel("Frequency")
        plt.title("Degree Distribution")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(plots_dir / "degree_distribution.png", dpi=300, bbox_inches="tight")
        plt.close()

    # Export data
    if include_data:
        data_dir = output_path / "data"
        data_dir.mkdir(exist_ok=True)

        export_network_data(graph, str(data_dir / "network.json"), format="json")
        export_network_data(graph, str(data_dir / "network.gexf"), format="gexf")

    # Create summary
    if include_summary:
        summary = create_network_summary(graph)
        summary_file = output_path / "summary.json"
        with summary_file.open("w") as f:
            json.dump(summary, f, indent=2)

    return str(output_path)


def _get_network_statistics(graph: nx.Graph) -> dict[str, Any]:
    """Get basic network statistics."""
    stats = {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": nx.density(graph),
        "average_clustering": nx.average_clustering(graph),
        "transitivity": nx.transitivity(graph),
    }

    # Degree statistics
    degrees = dict(graph.degree())
    if degrees:
        degree_values = list(degrees.values())
        stats["degree_stats"] = {
            "min": min(degree_values),
            "max": max(degree_values),
            "mean": sum(degree_values) / len(degree_values),
            "median": sorted(degree_values)[len(degree_values) // 2],
        }

    return stats


def _get_centrality_summary(graph: nx.Graph) -> dict[str, Any]:
    """Get centrality measures summary."""
    centrality_summary = {}

    try:
        centrality_summary["degree"] = nx.degree_centrality(graph)
    except nx.NetworkXError:
        centrality_summary["degree"] = {}

    try:
        centrality_summary["betweenness"] = nx.betweenness_centrality(graph)
    except nx.NetworkXError:
        centrality_summary["betweenness"] = {}

    try:
        centrality_summary["closeness"] = nx.closeness_centrality(graph)
    except nx.NetworkXError:
        centrality_summary["closeness"] = {}

    return centrality_summary


def _get_community_summary(graph: nx.Graph) -> dict[str, Any]:
    """Get community detection summary."""
    try:
        communities = list(nx.community.greedy_modularity_communities(graph))
        return {
            "number_of_communities": len(communities),
            "communities": [list(community) for community in communities],
            "modularity": nx.community.modularity(graph, communities),
        }
    except nx.NetworkXError:
        return {"error": "Community detection failed"}


def _export_to_csv(graph: nx.Graph, filepath: str, include_attributes: bool) -> None:
    """Export graph to CSV files."""
    base_path = Path(filepath).with_suffix("")

    # Export nodes
    nodes_data = []
    for node in graph.nodes():
        node_data = {"node_id": node}
        if include_attributes:
            node_data.update(graph.nodes[node])
        nodes_data.append(node_data)

    nodes_df = pd.DataFrame(nodes_data)
    nodes_df.to_csv(f"{base_path}_nodes.csv", index=False)

    # Export edges
    edges_data = []
    for edge in graph.edges(data=True):
        edge_data = {"source": edge[0], "target": edge[1]}
        if include_attributes:
            edge_data.update(edge[2])
        edges_data.append(edge_data)

    edges_df = pd.DataFrame(edges_data)
    edges_df.to_csv(f"{base_path}_edges.csv", index=False)
