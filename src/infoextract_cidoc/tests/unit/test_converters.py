"""Unit tests for to_networkx/converters.py."""

from uuid import uuid4

import networkx as nx
import pytest

from infoextract_cidoc.extraction.models import ExtractedEntity, ExtractedRelationship
from infoextract_cidoc.io.to_networkx.converters import (
    convert_extracted_to_networkx,
    entities_to_networkx,
    export_graph_to_dataframe,
    extract_edge_attributes,
    extract_node_attributes,
    filter_graph_by_attribute,
    get_subgraph_by_entity_type,
    merge_graphs,
    relationships_to_edges,
)
from infoextract_cidoc.models.base import CRMEntity, CRMRelation


@pytest.mark.unit
class TestEntitiesToNetworkx:
    def test_basic_conversion(self) -> None:
        entities = [
            CRMEntity(id=uuid4(), class_code="E21", label="Einstein"),
            CRMEntity(id=uuid4(), class_code="E53", label="Princeton"),
        ]
        node_ids, node_data_list = entities_to_networkx(entities)
        assert len(node_ids) == 2
        assert len(node_data_list) == 2
        assert node_data_list[0]["class_code"] == "E21"
        assert node_data_list[0]["label"] == "Einstein"

    def test_excludes_id_from_node_data(self) -> None:
        entities = [CRMEntity(id=uuid4(), class_code="E21", label="Test")]
        _node_ids, node_data_list = entities_to_networkx(entities)
        # id is the node key, not in data dict
        assert "id" not in node_data_list[0]

    def test_exclude_all_attributes(self) -> None:
        entities = [CRMEntity(id=uuid4(), class_code="E21", label="Test")]
        _node_ids, node_data_list = entities_to_networkx(
            entities, include_all_attributes=False
        )
        assert node_data_list[0] == {"class_code": "E21", "label": "Test"}


@pytest.mark.unit
class TestRelationshipsToEdges:
    def test_basic_conversion(self) -> None:
        src_id = uuid4()
        tgt_id = uuid4()
        rels = [CRMRelation(src=src_id, type="P74", tgt=tgt_id)]
        edges = relationships_to_edges(rels)
        assert len(edges) == 1
        assert edges[0][0] == str(src_id)
        assert edges[0][1] == str(tgt_id)
        assert edges[0][2]["property_code"] == "P74"

    def test_empty_list(self) -> None:
        assert relationships_to_edges([]) == []


@pytest.mark.unit
class TestExtractNodeAttributes:
    def test_extracts_attribute(self) -> None:
        graph = nx.Graph()
        graph.add_node("A", class_code="E21")
        graph.add_node("B", class_code="E53")
        result = extract_node_attributes(graph, "class_code")
        assert result == {"A": "E21", "B": "E53"}

    def test_default_value(self) -> None:
        graph = nx.Graph()
        graph.add_node("A")
        result = extract_node_attributes(graph, "class_code", default_value="unknown")
        assert result["A"] == "unknown"


@pytest.mark.unit
class TestExtractEdgeAttributes:
    def test_extracts_attribute(self) -> None:
        graph = nx.Graph()
        graph.add_edge("A", "B", property_code="P74")
        result = extract_edge_attributes(graph, "property_code")
        assert result[("A", "B")] == "P74"


@pytest.mark.unit
class TestFilterGraphByAttribute:
    def test_filter_nodes(self) -> None:
        graph = nx.Graph()
        graph.add_node("A", class_code="E21")
        graph.add_node("B", class_code="E53")
        filtered = filter_graph_by_attribute(graph, "class_code", "E21")
        assert "A" in filtered.nodes
        assert "B" not in filtered.nodes

    def test_filter_edges(self) -> None:
        graph = nx.Graph()
        graph.add_edge("A", "B", property_code="P74")
        graph.add_edge("B", "C", property_code="P7")
        filtered = filter_graph_by_attribute(
            graph, "property_code", "P74", filter_nodes=False, filter_edges=True
        )
        assert graph.has_edge("A", "B")
        assert not filtered.has_edge("B", "C")


@pytest.mark.unit
class TestGetSubgraphByEntityType:
    def test_filters_by_type(self) -> None:
        graph = nx.Graph()
        graph.add_node("A", class_code="E21")
        graph.add_node("B", class_code="E53")
        graph.add_node("C", class_code="E21")
        subgraph = get_subgraph_by_entity_type(graph, "E21")
        assert "A" in subgraph.nodes
        assert "C" in subgraph.nodes
        assert "B" not in subgraph.nodes


@pytest.mark.unit
class TestConvertExtractedToNetworkx:
    def test_confidence_filtering(self) -> None:
        high_conf = ExtractedEntity(
            class_code="E21", label="Einstein", confidence=0.9
        )
        low_conf = ExtractedEntity(class_code="E53", label="Place", confidence=0.2)
        graph = convert_extracted_to_networkx(
            [high_conf, low_conf], [], min_confidence=0.5
        )
        assert graph.number_of_nodes() == 1
        node_data = next(iter(graph.nodes(data=True)))[1]
        assert node_data["label"] == "Einstein"

    def test_edge_creation(self) -> None:
        entity1 = ExtractedEntity(class_code="E21", label="Einstein", confidence=1.0)
        entity2 = ExtractedEntity(class_code="E53", label="Princeton", confidence=1.0)
        rel = ExtractedRelationship(
            source_id=entity1.id,
            target_id=entity2.id,
            property_code="P74",
            property_label="has residence",
            confidence=1.0,
        )
        graph = convert_extracted_to_networkx([entity1, entity2], [rel])
        assert graph.number_of_edges() == 1


@pytest.mark.unit
class TestMergeGraphs:
    def test_union_merge(self) -> None:
        g1 = nx.Graph()
        g1.add_node("A")
        g2 = nx.Graph()
        g2.add_node("B")
        merged = merge_graphs([g1, g2])
        assert "A" in merged.nodes
        assert "B" in merged.nodes

    def test_empty_list(self) -> None:
        result = merge_graphs([])
        assert result.number_of_nodes() == 0

    def test_single_graph(self) -> None:
        g = nx.Graph()
        g.add_node("A")
        result = merge_graphs([g])
        assert result is g


@pytest.mark.unit
class TestExportGraphToDataframe:
    def test_basic_export(self) -> None:
        graph = nx.Graph()
        graph.add_node("A", class_code="E21", label="Einstein")
        graph.add_edge("A", "B", property_code="P74")
        nodes_df, edges_df = export_graph_to_dataframe(graph)
        assert len(nodes_df) >= 1
        assert len(edges_df) == 1
