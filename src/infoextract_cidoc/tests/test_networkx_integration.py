"""
Tests for NetworkX integration and visualization features.

This module tests the new NetworkX integration, visualization,
and complete workflow functionality.
"""

import pytest
import networkx as nx
from pathlib import Path

from infoextract_cidoc.models.base import CRMEntity
from infoextract_cidoc.io.to_networkx import (
    to_networkx_graph,
    calculate_centrality_measures,
    find_communities,
    get_network_statistics,
)
from infoextract_cidoc.visualization import (
    plot_network_graph,
    create_interactive_plot,
    get_node_colors,
    get_edge_colors,
    get_node_sizes,
)
from infoextract_cidoc.extraction.models import ExtractedEntity, ExtractedRelationship, ExtractionResult


class TestNetworkXIntegration:
    """Test NetworkX integration functionality."""
    
    def test_to_networkx_graph_basic(self):
        """Test basic NetworkX graph creation."""
        # Create test entities
        entities = [
            CRMEntity(id="person1", class_code="E21", label="Albert Einstein"),
            CRMEntity(id="place1", class_code="E53", label="Princeton"),
            CRMEntity(id="event1", class_code="E5", label="Nobel Prize"),
        ]
        
        # Create graph
        graph = to_networkx_graph(entities)
        
        # Verify graph properties
        assert graph.number_of_nodes() == 3
        assert graph.number_of_edges() == 0  # No relationships provided
        
        # Verify node data - entities get UUIDs, so we check by class_code
        node_data = dict(graph.nodes(data=True))
        node_labels = {data["label"]: node_id for node_id, data in node_data.items()}
        
        assert "Albert Einstein" in node_labels
        assert "Princeton" in node_labels
        assert "Nobel Prize" in node_labels
        
        # Verify specific node data
        einstein_node = node_labels["Albert Einstein"]
        assert node_data[einstein_node]["class_code"] == "E21"
        assert node_data[einstein_node]["label"] == "Albert Einstein"
    
    def test_to_networkx_graph_with_relationships(self):
        """Test NetworkX graph creation with relationships."""
        # Create test entities
        entities = [
            CRMEntity(id="person1", class_code="E21", label="Albert Einstein"),
            CRMEntity(id="place1", class_code="E53", label="Princeton"),
        ]
        
        # Create test relationships using the actual UUIDs
        from infoextract_cidoc.models.base import CRMRelation
        person_id = str(entities[0].id)
        place_id = str(entities[1].id)
        
        relationships = [
            CRMRelation(src=person_id, type="P74", tgt=place_id),  # has residence
        ]
        
        # Create graph
        graph = to_networkx_graph(entities, relationships)
        
        # Verify graph properties
        assert graph.number_of_nodes() == 2
        assert graph.number_of_edges() == 1
        
        # Verify edge data
        edges = list(graph.edges(data=True))
        assert len(edges) == 1
        edge = edges[0]
        assert edge[0] == person_id
        assert edge[1] == place_id
        assert edge[2]["property_code"] == "P74"
    
    def test_calculate_centrality_measures(self):
        """Test centrality measure calculation."""
        # Create a simple connected graph
        graph = nx.DiGraph()
        graph.add_edges_from([
            ("A", "B"), ("B", "C"), ("C", "A"),
            ("A", "D"), ("B", "D")
        ])
        
        # Calculate centrality measures
        centrality_measures = calculate_centrality_measures(graph)
        
        # Verify measures are calculated
        assert "degree" in centrality_measures
        assert "betweenness" in centrality_measures
        assert "closeness" in centrality_measures
        
        # Verify degree centrality
        degree_centrality = centrality_measures["degree"]
        assert "A" in degree_centrality
        assert "B" in degree_centrality
        assert degree_centrality["A"] > degree_centrality["D"]  # A has higher degree
        
        # Skip PageRank test if scipy is not available
        if "pagerank" in centrality_measures:
            pagerank = centrality_measures["pagerank"]
            assert "A" in pagerank
            assert "B" in pagerank
    
    def test_find_communities(self):
        """Test community detection."""
        # Create a graph with clear communities
        graph = nx.Graph()
        # Community 1: A-B-C
        graph.add_edges_from([("A", "B"), ("B", "C"), ("A", "C")])
        # Community 2: D-E-F
        graph.add_edges_from([("D", "E"), ("E", "F"), ("D", "F")])
        # Bridge: C-D
        graph.add_edge("C", "D")
        
        # Find communities
        communities = find_communities(graph)
        
        # Verify communities are found
        assert len(communities) >= 1
        assert len(communities[0]) >= 3  # At least one community should have 3+ nodes
    
    def test_get_network_statistics(self):
        """Test network statistics calculation."""
        # Create test graph
        graph = nx.Graph()
        graph.add_edges_from([
            ("A", "B"), ("B", "C"), ("C", "A"),
            ("A", "D")
        ])
        
        # Add node attributes
        graph.nodes["A"]["class_code"] = "E21"
        graph.nodes["B"]["class_code"] = "E21"
        graph.nodes["C"]["class_code"] = "E53"
        graph.nodes["D"]["class_code"] = "E53"
        
        # Get statistics
        stats = get_network_statistics(graph)
        
        # Verify basic metrics
        assert stats["basic_metrics"]["nodes"] == 4
        assert stats["basic_metrics"]["edges"] == 4
        assert stats["basic_metrics"]["density"] > 0
        
        # Verify entity type distribution
        assert "entity_type_distribution" in stats
        assert stats["entity_type_distribution"]["E21"] == 2
        assert stats["entity_type_distribution"]["E53"] == 2


class TestVisualization:
    """Test visualization functionality."""
    
    def test_get_node_colors(self):
        """Test node color assignment."""
        graph = nx.Graph()
        graph.add_nodes_from(["A", "B", "C"])
        graph.nodes["A"]["class_code"] = "E21"
        graph.nodes["B"]["class_code"] = "E53"
        graph.nodes["C"]["class_code"] = "E5"
        
        colors = get_node_colors(graph, "class_code")
        
        assert len(colors) == 3
        assert all(isinstance(color, str) for color in colors)
        assert all(color.startswith("#") for color in colors)
    
    def test_get_edge_colors(self):
        """Test edge color assignment."""
        graph = nx.Graph()
        graph.add_edges_from([("A", "B"), ("B", "C")])
        graph.edges[("A", "B")]["property_code"] = "P11"
        graph.edges[("B", "C")]["property_code"] = "P7"
        
        colors = get_edge_colors(graph, "property_code")
        
        assert len(colors) == 2
        assert all(isinstance(color, str) for color in colors)
        assert all(color.startswith("#") for color in colors)
    
    def test_get_node_sizes(self):
        """Test node size calculation."""
        graph = nx.Graph()
        graph.add_edges_from([
            ("A", "B"), ("B", "C"), ("C", "A"),
            ("A", "D")
        ])
        
        sizes = get_node_sizes(graph, "degree")
        
        assert len(sizes) == 4
        assert all(isinstance(size, int) for size in sizes)
        assert all(size > 0 for size in sizes)
        
        # A should have the largest size (highest degree)
        node_sizes = dict(zip(graph.nodes(), sizes))
        assert node_sizes["A"] >= node_sizes["D"]
    
    def test_plot_network_graph_creation(self):
        """Test static network plot creation."""
        graph = nx.Graph()
        graph.add_edges_from([("A", "B"), ("B", "C"), ("C", "A")])
        graph.nodes["A"]["class_code"] = "E21"
        graph.nodes["B"]["class_code"] = "E53"
        graph.nodes["C"]["class_code"] = "E5"
        
        # Test plot creation (without showing)
        fig = plot_network_graph(
            graph,
            title="Test Network",
            show_plot=False,
            save_path=None
        )
        
        assert fig is not None
        assert hasattr(fig, "axes")
    
    def test_create_interactive_plot(self):
        """Test interactive plot creation."""
        graph = nx.Graph()
        graph.add_edges_from([("A", "B"), ("B", "C")])
        graph.nodes["A"]["class_code"] = "E21"
        graph.nodes["B"]["class_code"] = "E53"
        graph.nodes["C"]["class_code"] = "E5"
        
        # Test interactive plot creation
        fig = create_interactive_plot(graph, title="Test Interactive Network")
        
        assert fig is not None
        assert hasattr(fig, "data")
        assert hasattr(fig, "layout")


class TestExtractionModels:
    """Test extraction model functionality."""
    
    def test_extracted_entity_creation(self):
        """Test ExtractedEntity model creation."""
        entity = ExtractedEntity(
            class_code="E21",
            label="Albert Einstein",
            description="Theoretical physicist",
            confidence=0.9
        )
        
        assert entity.class_code == "E21"
        assert entity.label == "Albert Einstein"
        assert entity.confidence == 0.9
        assert entity.id is not None
    
    def test_extracted_relationship_creation(self):
        """Test ExtractedRelationship model creation."""
        from uuid import uuid4
        
        source_id = uuid4()
        target_id = uuid4()
        
        relationship = ExtractedRelationship(
            source_id=source_id,
            target_id=target_id,
            property_code="P74",
            property_label="has residence",
            confidence=0.8
        )
        
        assert relationship.source_id == source_id
        assert relationship.target_id == target_id
        assert relationship.property_code == "P74"
        assert relationship.confidence == 0.8
    
    def test_extraction_result_operations(self):
        """Test ExtractionResult operations."""
        entities = [
            ExtractedEntity(class_code="E21", label="Person 1"),
            ExtractedEntity(class_code="E53", label="Place 1"),
            ExtractedEntity(class_code="E21", label="Person 2"),
        ]
        
        relationships = [
            ExtractedRelationship(
                source_id=entities[0].id,
                target_id=entities[1].id,
                property_code="P74",
                property_label="has residence"
            )
        ]
        
        result = ExtractionResult(entities=entities, relationships=relationships)
        
        # Test entity filtering
        person_entities = result.get_entities_by_class("E21")
        assert len(person_entities) == 2
        
        place_entities = result.get_entities_by_class("E53")
        assert len(place_entities) == 1
        
        # Test relationship filtering
        residence_rels = result.get_relationships_by_property("P74")
        assert len(residence_rels) == 1


class TestCompleteWorkflow:
    """Test complete workflow integration."""
    
    def test_workflow_integration(self):
        """Test integration of all workflow components."""
        # Create test entities
        entities = [
            CRMEntity(id="person1", class_code="E21", label="Albert Einstein"),
            CRMEntity(id="place1", class_code="E53", label="Princeton"),
            CRMEntity(id="event1", class_code="E5", label="Nobel Prize"),
        ]
        
        # Test NetworkX conversion
        graph = to_networkx_graph(entities)
        assert graph.number_of_nodes() == 3
        
        # Test centrality calculation
        centrality_measures = calculate_centrality_measures(graph)
        assert "degree" in centrality_measures
        
        # Test community detection
        communities = find_communities(graph)
        assert isinstance(communities, list)
        
        # Test visualization
        fig = plot_network_graph(graph, show_plot=False, save_path=None)
        assert fig is not None
        
        # Test interactive plot
        interactive_fig = create_interactive_plot(graph)
        assert interactive_fig is not None
    
    def test_markdown_integration(self):
        """Test Markdown rendering integration."""
        from infoextract_cidoc.io.to_markdown import to_markdown, MarkdownStyle, render_table
        
        entities = [
            CRMEntity(id="person1", class_code="E21", label="Albert Einstein"),
            CRMEntity(id="place1", class_code="E53", label="Princeton"),
        ]
        
        # Test individual entity rendering
        markdown_card = to_markdown(entities[0], MarkdownStyle.CARD)
        assert "Albert Einstein" in markdown_card
        assert "E21" in markdown_card
        
        # Test table rendering
        table_markdown = render_table(entities)
        assert "Albert Einstein" in table_markdown
        assert "Princeton" in table_markdown


if __name__ == "__main__":
    pytest.main([__file__])
