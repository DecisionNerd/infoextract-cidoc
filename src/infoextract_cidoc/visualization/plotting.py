"""
Network plotting functions for CIDOC CRM graphs.

This module provides various plotting functions for visualizing
NetworkX graphs containing CRM entities and relationships.
"""

from typing import Any, Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


def plot_network_graph(
    graph: nx.Graph,
    *,
    title: str = "CRM Network",
    figsize: Tuple[int, int] = (12, 8),
    layout: str = "spring",
    node_size: int = 300,
    node_color: str = "class_code",
    edge_width: float = 1.0,
    edge_color: str = "gray",
    show_labels: bool = True,
    label_font_size: int = 8,
    save_path: Optional[str] = None,
    show_plot: bool = True,
) -> plt.Figure:
    """
    Create a static network plot using matplotlib.
    
    Args:
        graph: NetworkX graph to plot
        title: Plot title
        figsize: Figure size (width, height)
        layout: Layout algorithm ("spring", "circular", "hierarchical", "random")
        node_size: Base node size
        node_color: Node coloring scheme ("class_code", "degree", "centrality")
        edge_width: Edge width
        edge_color: Edge color
        show_labels: Whether to show node labels
        label_font_size: Font size for labels
        save_path: Path to save the plot
        show_plot: Whether to display the plot
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Get layout positions
    pos = _get_layout_positions(graph, layout)
    
    # Get node colors and sizes
    node_colors = _get_node_colors(graph, node_color)
    node_sizes = _get_node_sizes(graph, node_size)
    
    # Draw the graph
    nx.draw(
        graph,
        pos=pos,
        ax=ax,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color=edge_color,
        width=edge_width,
        with_labels=show_labels,
        font_size=label_font_size,
        font_weight="bold",
        alpha=0.8,
    )
    
    # Add title
    ax.set_title(title, fontsize=16, fontweight="bold", pad=20)
    
    # Create legend
    _create_legend(ax, graph, node_color)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    
    # Show if requested
    if show_plot:
        plt.show()
    
    return fig


def plot_temporal_network(
    graph: nx.Graph,
    *,
    title: str = "Temporal CRM Network",
    time_attribute: str = "temporal_info",
    figsize: Tuple[int, int] = (14, 10),
    show_timeline: bool = True,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Create a temporal network plot showing time-based relationships.
    
    Args:
        graph: NetworkX graph with temporal attributes
        title: Plot title
        time_attribute: Name of temporal attribute
        figsize: Figure size
        show_timeline: Whether to show timeline axis
        save_path: Path to save the plot
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Separate nodes by temporal information
    temporal_nodes = []
    non_temporal_nodes = []
    
    for node_id in graph.nodes():
        node_data = graph.nodes[node_id]
        if node_data.get("has_temporal_info", False):
            temporal_nodes.append(node_id)
        else:
            non_temporal_nodes.append(node_id)
    
    # Create subgraph for temporal nodes
    if temporal_nodes:
        temporal_subgraph = graph.subgraph(temporal_nodes)
        
        # Use time-based layout
        pos = _get_temporal_layout(temporal_subgraph, time_attribute)
        
        # Draw temporal nodes
        nx.draw_networkx_nodes(
            temporal_subgraph,
            pos=pos,
            ax=ax,
            node_color="red",
            node_size=400,
            alpha=0.8,
            label="Temporal Entities"
        )
        
        # Draw temporal edges
        nx.draw_networkx_edges(
            temporal_subgraph,
            pos=pos,
            ax=ax,
            edge_color="red",
            width=1.5,
            alpha=0.6
        )
    
    # Draw non-temporal nodes
    if non_temporal_nodes:
        non_temporal_subgraph = graph.subgraph(non_temporal_nodes)
        pos_non_temporal = nx.spring_layout(non_temporal_subgraph)
        
        nx.draw_networkx_nodes(
            non_temporal_subgraph,
            pos=pos_non_temporal,
            ax=ax,
            node_color="lightblue",
            node_size=300,
            alpha=0.6,
            label="Non-Temporal Entities"
        )
    
    # Add labels
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8)
    
    ax.set_title(title, fontsize=16, fontweight="bold")
    ax.legend()
    
    if show_timeline:
        _add_timeline_axis(ax, graph, time_attribute)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    
    return fig


def plot_community_network(
    graph: nx.Graph,
    communities: List[List[str]],
    *,
    title: str = "Community Structure",
    figsize: Tuple[int, int] = (12, 8),
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plot network with community structure highlighted.
    
    Args:
        graph: NetworkX graph
        communities: List of communities (lists of node IDs)
        title: Plot title
        figsize: Figure size
        save_path: Path to save the plot
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Get layout
    pos = nx.spring_layout(graph)
    
    # Color nodes by community
    colors = plt.cm.Set3(np.linspace(0, 1, len(communities)))
    
    for i, community in enumerate(communities):
        community_subgraph = graph.subgraph(community)
        
        nx.draw_networkx_nodes(
            community_subgraph,
            pos=pos,
            ax=ax,
            node_color=[colors[i]],
            node_size=400,
            alpha=0.8,
            label=f"Community {i+1}"
        )
    
    # Draw edges
    nx.draw_networkx_edges(
        graph,
        pos=pos,
        ax=ax,
        edge_color="gray",
        width=0.5,
        alpha=0.5
    )
    
    # Draw labels
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8)
    
    ax.set_title(title, fontsize=16, fontweight="bold")
    ax.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    
    return fig


def plot_centrality_network(
    graph: nx.Graph,
    centrality_scores: Dict[str, float],
    *,
    title: str = "Centrality Analysis",
    centrality_type: str = "degree",
    figsize: Tuple[int, int] = (12, 8),
    save_path: Optional[str] = None,
) -> plt.Figure:
    """
    Plot network with node sizes based on centrality scores.
    
    Args:
        graph: NetworkX graph
        centrality_scores: Dictionary of node centrality scores
        title: Plot title
        centrality_type: Type of centrality being visualized
        figsize: Figure size
        save_path: Path to save the plot
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Get layout
    pos = nx.spring_layout(graph)
    
    # Scale node sizes based on centrality
    max_centrality = max(centrality_scores.values()) if centrality_scores else 1
    node_sizes = [centrality_scores.get(node, 0) / max_centrality * 1000 + 100 
                  for node in graph.nodes()]
    
    # Draw nodes
    nx.draw_networkx_nodes(
        graph,
        pos=pos,
        ax=ax,
        node_size=node_sizes,
        node_color="lightcoral",
        alpha=0.8
    )
    
    # Draw edges
    nx.draw_networkx_edges(
        graph,
        pos=pos,
        ax=ax,
        edge_color="gray",
        width=0.5,
        alpha=0.5
    )
    
    # Draw labels
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8)
    
    ax.set_title(f"{title} - {centrality_type.title()} Centrality", 
                 fontsize=16, fontweight="bold")
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    
    return fig


def create_interactive_plot(
    graph: nx.Graph,
    *,
    title: str = "Interactive CRM Network",
    layout: str = "spring",
    show_labels: bool = True,
    node_size_multiplier: float = 20,
    edge_width_multiplier: float = 2,
) -> go.Figure:
    """
    Create an interactive network plot using Plotly for notebook display.
    
    Note: This function is designed for use in Jupyter notebooks only.
    It creates interactive visualizations that work well in notebook environments.
    
    Args:
        graph: NetworkX graph to plot
        title: Plot title
        layout: Layout algorithm
        show_labels: Whether to show node labels
        node_size_multiplier: Multiplier for node sizes
        edge_width_multiplier: Multiplier for edge widths
        
    Returns:
        Plotly figure object for notebook display
    """
    # Get layout positions
    pos = _get_layout_positions(graph, layout)
    
    # Prepare edge traces
    edge_x = []
    edge_y = []
    
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=edge_width_multiplier, color="#888"),
        hoverinfo="none",
        mode="lines"
    )
    
    # Prepare node traces
    node_x = []
    node_y = []
    node_text = []
    node_hovertext = []
    node_colors = []
    node_sizes = []
    
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_data = graph.nodes[node]
        label = node_data.get("label", node)
        class_code = node_data.get("class_code", "Unknown")
        
        node_text.append(label if show_labels else "")
        node_hovertext.append(f"ID: {node}<br>Label: {label}<br>Class: {class_code}")
        
        # Color by class code
        color_map = {
            "E21": "red",      # Person
            "E5": "blue",      # Event
            "E53": "green",    # Place
            "E22": "orange",   # Object
            "E52": "purple",   # Time
        }
        node_colors.append(color_map.get(class_code, "gray"))
        
        # Size by degree
        degree = graph.degree(node)
        node_sizes.append(max(10, degree * node_size_multiplier))
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        hoverinfo="text",
        hovertext=node_hovertext,
        text=node_text,
        textposition="middle center",
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color="white")
        )
    )
    
    # Create figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(text=title, font=dict(size=16)),
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text="Interactive CRM Network Visualization",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    xanchor="left", yanchor="bottom",
                    font=dict(color="#888", size=12)
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    
    return fig


# Helper functions

def _get_layout_positions(graph: nx.Graph, layout: str) -> Dict[str, Tuple[float, float]]:
    """Get node positions using specified layout algorithm."""
    if layout == "spring":
        return nx.spring_layout(graph)
    elif layout == "circular":
        return nx.circular_layout(graph)
    elif layout == "hierarchical":
        return nx.nx_agraph.graphviz_layout(graph, prog="dot")
    elif layout == "random":
        return nx.random_layout(graph)
    else:
        return nx.spring_layout(graph)


def _get_node_colors(graph: nx.Graph, color_scheme: str) -> List[str]:
    """Get node colors based on specified scheme."""
    colors = []
    color_map = {
        "E21": "red",      # Person
        "E5": "blue",      # Event
        "E53": "green",    # Place
        "E22": "orange",   # Object
        "E52": "purple",   # Time
    }
    
    for node in graph.nodes():
        node_data = graph.nodes[node]
        class_code = node_data.get("class_code", "Unknown")
        colors.append(color_map.get(class_code, "gray"))
    
    return colors


def _get_node_sizes(graph: nx.Graph, base_size: int) -> List[int]:
    """Get node sizes based on degree."""
    sizes = []
    degrees = dict(graph.degree())
    max_degree = max(degrees.values()) if degrees else 1
    
    # Handle case where all nodes have degree 0
    if max_degree == 0:
        return [base_size] * graph.number_of_nodes()
    
    for node in graph.nodes():
        degree = degrees.get(node, 0)
        size = base_size + (degree / max_degree) * base_size
        sizes.append(int(size))
    
    return sizes


def _create_legend(ax: plt.Axes, graph: nx.Graph, color_scheme: str) -> None:
    """Create legend for the plot."""
    if color_scheme == "class_code":
        legend_elements = []
        color_map = {
            "E21": ("Person", "red"),
            "E5": ("Event", "blue"),
            "E53": ("Place", "green"),
            "E22": ("Object", "orange"),
            "E52": ("Time", "purple"),
        }
        
        for class_code, (label, color) in color_map.items():
            if any(graph.nodes[node].get("class_code") == class_code for node in graph.nodes()):
                legend_elements.append(mpatches.Patch(color=color, label=label))
        
        if legend_elements:
            ax.legend(handles=legend_elements, loc="upper right")


def _get_temporal_layout(graph: nx.Graph, time_attribute: str) -> Dict[str, Tuple[float, float]]:
    """Get layout positions based on temporal information."""
    # This is a simplified implementation
    # In practice, you would parse temporal data and position nodes accordingly
    return nx.spring_layout(graph)


def _add_timeline_axis(ax: plt.Axes, graph: nx.Graph, time_attribute: str) -> None:
    """Add timeline axis to the plot."""
    # This would be implemented based on actual temporal data
    pass
