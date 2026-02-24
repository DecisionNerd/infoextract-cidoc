"""
Styling utilities for network visualizations.

This module provides functions for customizing the appearance
of network plots and creating consistent styling.
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def get_node_colors(
    graph: nx.Graph,
    color_scheme: str = "class_code",
    *,
    custom_colors: dict[str, str] | None = None,
) -> list[str]:
    """
    Get node colors based on specified color scheme.

    Args:
        graph: NetworkX graph
        color_scheme: Color scheme to use ("class_code", "degree", "centrality", "custom")
        custom_colors: Custom color mapping for "custom" scheme

    Returns:
        List of colors for each node
    """
    colors = []

    if color_scheme == "class_code":
        color_map = {
            "E21": "#FF6B6B",  # Person - Red
            "E5": "#4ECDC4",  # Event - Teal
            "E53": "#45B7D1",  # Place - Blue
            "E22": "#96CEB4",  # Object - Green
            "E52": "#FFEAA7",  # Time - Yellow
            "E74": "#DDA0DD",  # Group - Plum
            "E42": "#98D8C8",  # Identifier - Mint
            "E35": "#F7DC6F",  # Title - Gold
        }

        for node in graph.nodes():
            node_data = graph.nodes[node]
            class_code = node_data.get("class_code", "Unknown")
            colors.append(color_map.get(class_code, "#CCCCCC"))

    elif color_scheme == "degree":
        degrees = dict(graph.degree())
        max_degree = max(degrees.values()) if degrees else 1

        for node in graph.nodes():
            degree = degrees.get(node, 0)
            # Use a colormap to map degree to color
            normalized_degree = degree / max_degree
            color = plt.cm.viridis(normalized_degree)
            colors.append(color)

    elif color_scheme == "centrality":
        # This would require centrality scores to be passed
        # For now, use a default color
        colors = ["#FF6B6B"] * len(graph.nodes())

    elif color_scheme == "custom" and custom_colors:
        for node in graph.nodes():
            node_data = graph.nodes[node]
            class_code = node_data.get("class_code", "Unknown")
            colors.append(custom_colors.get(class_code, "#CCCCCC"))

    else:
        # Default color
        colors = ["#FF6B6B"] * len(graph.nodes())

    return colors


def get_edge_colors(
    graph: nx.Graph,
    color_scheme: str = "property_code",
    *,
    custom_colors: dict[str, str] | None = None,
) -> list[str]:
    """
    Get edge colors based on specified color scheme.

    Args:
        graph: NetworkX graph
        color_scheme: Color scheme to use ("property_code", "uniform", "custom")
        custom_colors: Custom color mapping for "custom" scheme

    Returns:
        List of colors for each edge
    """
    colors = []

    if color_scheme == "property_code":
        color_map = {
            "P11": "#FF6B6B",  # had participant - Red
            "P7": "#4ECDC4",  # took place at - Teal
            "P53": "#45B7D1",  # has current location - Blue
            "P108": "#96CEB4",  # was produced by - Green
            "P4": "#FFEAA7",  # has time-span - Yellow
            "P69": "#DDA0DD",  # has association with - Plum
        }

        for edge in graph.edges(data=True):
            edge_data = edge[2]
            property_code = edge_data.get("property_code", "Unknown")
            colors.append(color_map.get(property_code, "#CCCCCC"))

    elif color_scheme == "uniform":
        colors = ["#888888"] * graph.number_of_edges()

    elif color_scheme == "custom" and custom_colors:
        for edge in graph.edges(data=True):
            edge_data = edge[2]
            property_code = edge_data.get("property_code", "Unknown")
            colors.append(custom_colors.get(property_code, "#CCCCCC"))

    else:
        colors = ["#888888"] * graph.number_of_edges()

    return colors


def get_node_sizes(
    graph: nx.Graph,
    size_scheme: str = "degree",
    *,
    base_size: int = 300,
    min_size: int = 50,
    max_size: int = 1000,
    size_multiplier: float = 1.0,
) -> list[int]:
    """
    Get node sizes based on specified size scheme.

    Args:
        graph: NetworkX graph
        size_scheme: Size scheme to use ("degree", "uniform", "centrality")
        base_size: Base size for nodes
        min_size: Minimum node size
        max_size: Maximum node size
        size_multiplier: Multiplier for size calculation

    Returns:
        List of sizes for each node
    """
    sizes = []

    if size_scheme == "degree":
        degrees = dict(graph.degree())
        max_degree = max(degrees.values()) if degrees else 1

        for node in graph.nodes():
            degree = degrees.get(node, 0)
            normalized_degree = degree / max_degree
            size = base_size + (normalized_degree * base_size * size_multiplier)
            size = max(min_size, min(max_size, int(size)))
            sizes.append(size)

    elif size_scheme == "uniform":
        sizes = [base_size] * len(graph.nodes())

    elif size_scheme == "centrality":
        # This would require centrality scores to be passed
        # For now, use base size
        sizes = [base_size] * len(graph.nodes())

    else:
        sizes = [base_size] * len(graph.nodes())

    return sizes


def get_layout_positions(
    graph: nx.Graph,
    layout: str = "spring",
    *,
    seed: int | None = None,
    iterations: int = 50,
) -> dict[str, tuple[float, float]]:
    """
    Get node positions using specified layout algorithm.

    Args:
        graph: NetworkX graph
        layout: Layout algorithm ("spring", "circular", "hierarchical", "random", "kamada_kawai")
        seed: Random seed for reproducible layouts
        iterations: Number of iterations for spring layout

    Returns:
        Dictionary mapping node IDs to (x, y) positions
    """
    if seed is not None:
        np.random.seed(seed)

    if layout == "spring":
        return nx.spring_layout(graph, iterations=iterations, seed=seed)
    if layout == "circular":
        return nx.circular_layout(graph)
    if layout == "hierarchical":
        try:
            return nx.nx_agraph.graphviz_layout(graph, prog="dot")
        except ImportError:
            # Fallback to spring layout if graphviz is not available
            return nx.spring_layout(graph, iterations=iterations, seed=seed)
    elif layout == "random":
        return nx.random_layout(graph, seed=seed)
    elif layout == "kamada_kawai":
        return nx.kamada_kawai_layout(graph)
    elif layout == "spectral":
        return nx.spectral_layout(graph)
    else:
        return nx.spring_layout(graph, iterations=iterations, seed=seed)


def create_legend(
    ax: plt.Axes,
    graph: nx.Graph,
    legend_type: str = "nodes",
    *,
    title: str | None = None,
    loc: str = "upper right",
    fontsize: int = 10,
) -> None:
    """
    Create legend for network plot.

    Args:
        ax: Matplotlib axes object
        graph: NetworkX graph
        legend_type: Type of legend ("nodes", "edges", "both")
        title: Legend title
        loc: Legend location
        fontsize: Font size for legend

    Returns:
        None
    """
    legend_elements = []

    if legend_type in ["nodes", "both"]:
        # Create node legend
        node_color_map = {
            "E21": ("Person", "#FF6B6B"),
            "E5": ("Event", "#4ECDC4"),
            "E53": ("Place", "#45B7D1"),
            "E22": ("Object", "#96CEB4"),
            "E52": ("Time", "#FFEAA7"),
            "E74": ("Group", "#DDA0DD"),
            "E42": ("Identifier", "#98D8C8"),
            "E35": ("Title", "#F7DC6F"),
        }

        # Only include classes that exist in the graph
        existing_classes = set()
        for node in graph.nodes():
            node_data = graph.nodes[node]
            class_code = node_data.get("class_code", "Unknown")
            existing_classes.add(class_code)

        for class_code, (label, color) in node_color_map.items():
            if class_code in existing_classes:
                legend_elements.append(mpatches.Patch(color=color, label=label))

    if legend_type in ["edges", "both"]:
        # Create edge legend
        edge_color_map = {
            "P11": ("had participant", "#FF6B6B"),
            "P7": ("took place at", "#4ECDC4"),
            "P53": ("has current location", "#45B7D1"),
            "P108": ("was produced by", "#96CEB4"),
            "P4": ("has time-span", "#FFEAA7"),
            "P69": ("has association with", "#DDA0DD"),
        }

        # Only include properties that exist in the graph
        existing_properties = set()
        for edge in graph.edges(data=True):
            edge_data = edge[2]
            property_code = edge_data.get("property_code", "Unknown")
            existing_properties.add(property_code)

        for prop_code, (label, color) in edge_color_map.items():
            if prop_code in existing_properties:
                legend_elements.append(mpatches.Patch(color=color, label=label))

    if legend_elements:
        legend = ax.legend(
            handles=legend_elements,
            loc=loc,
            fontsize=fontsize,
            title=title,
            title_fontsize=fontsize + 2,
        )
        legend.get_frame().set_facecolor("white")
        legend.get_frame().set_alpha(0.8)


def get_color_palette(
    palette_name: str = "default",
    *,
    n_colors: int = 8,
) -> list[str]:
    """
    Get a color palette for network visualization.

    Args:
        palette_name: Name of the color palette
        n_colors: Number of colors to return

    Returns:
        List of hex color codes
    """
    palettes = {
        "default": [
            "#FF6B6B",
            "#4ECDC4",
            "#45B7D1",
            "#96CEB4",
            "#FFEAA7",
            "#DDA0DD",
            "#98D8C8",
            "#F7DC6F",
        ],
        "pastel": [
            "#FFB3BA",
            "#FFDFBA",
            "#FFFFBA",
            "#BAFFC9",
            "#BAE1FF",
            "#E6BAFF",
            "#FFBAE6",
            "#FFE6BA",
        ],
        "vibrant": [
            "#FF0000",
            "#00FF00",
            "#0000FF",
            "#FFFF00",
            "#FF00FF",
            "#00FFFF",
            "#FFA500",
            "#800080",
        ],
        "muted": [
            "#8B4513",
            "#2F4F4F",
            "#483D8B",
            "#556B2F",
            "#8B008B",
            "#B22222",
            "#228B22",
            "#4682B4",
        ],
        "grayscale": [
            "#000000",
            "#333333",
            "#666666",
            "#999999",
            "#CCCCCC",
            "#FFFFFF",
            "#808080",
            "#404040",
        ],
    }

    palette = palettes.get(palette_name, palettes["default"])

    # Repeat or truncate palette to get desired number of colors
    if len(palette) >= n_colors:
        return palette[:n_colors]
    return [palette[i % len(palette)] for i in range(n_colors)]


def apply_style(
    ax: plt.Axes,
    *,
    background_color: str = "white",
    grid: bool = False,
    grid_color: str = "lightgray",
    grid_alpha: float = 0.3,
    border_color: str = "black",
    border_width: float = 1.0,
) -> None:
    """
    Apply styling to matplotlib axes.

    Args:
        ax: Matplotlib axes object
        background_color: Background color
        grid: Whether to show grid
        grid_color: Grid color
        grid_alpha: Grid transparency
        border_color: Border color
        border_width: Border width

    Returns:
        None
    """
    ax.set_facecolor(background_color)

    if grid:
        ax.grid(True, color=grid_color, alpha=grid_alpha, linestyle="-", linewidth=0.5)

    # Set border
    for spine in ax.spines.values():
        spine.set_color(border_color)
        spine.set_linewidth(border_width)

    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
