"""Unit tests for to_networkx/graph_builder.py."""

from uuid import uuid4

import pytest

from infoextract_cidoc.io.to_networkx.graph_builder import (
    build_graph_from_entities,
    create_temporal_graph,
    to_networkx_graph,
)
from infoextract_cidoc.models.base import CRMEntity, CRMRelation
from infoextract_cidoc.models.generated.e_classes import (
    E5_Event,
    E22_HumanMadeObject,
    E52_TimeSpan,
    E53_Place,
)


@pytest.mark.unit
class TestToNetworkxGraph:
    def test_creates_nodes_for_entities(self) -> None:
        entities = [
            CRMEntity(id=uuid4(), class_code="E21", label="Einstein"),
            CRMEntity(id=uuid4(), class_code="E53", label="Princeton"),
        ]
        graph = to_networkx_graph(entities)
        assert graph.number_of_nodes() == 2

    def test_creates_edges_for_relationships(self) -> None:
        e1 = CRMEntity(id=uuid4(), class_code="E21", label="Einstein")
        e2 = CRMEntity(id=uuid4(), class_code="E53", label="Princeton")
        rel = CRMRelation(src=e1.id, type="P74", tgt=e2.id)
        graph = to_networkx_graph([e1, e2], [rel])
        assert graph.number_of_edges() == 1

    def test_node_attributes_stored(self) -> None:
        entity = CRMEntity(id=uuid4(), class_code="E21", label="Einstein")
        graph = to_networkx_graph([entity])
        node_data = graph.nodes[str(entity.id)]
        assert node_data["class_code"] == "E21"
        assert node_data["label"] == "Einstein"

    def test_empty_entities(self) -> None:
        graph = to_networkx_graph([])
        assert graph.number_of_nodes() == 0


@pytest.mark.unit
class TestBuildGraphFromEntities:
    def test_expands_shortcut_fields(self) -> None:
        place = E53_Place(id=uuid4(), class_code="E53", label="Athens")
        timespan = E52_TimeSpan(id=uuid4(), class_code="E52", label="450 BCE")
        event = E5_Event(
            id=uuid4(),
            class_code="E5",
            label="Vase Creation",
            timespan=timespan.id,
            took_place_at=place.id,
        )
        graph = build_graph_from_entities([event, place, timespan])
        # Should have 2 edges from P4 and P7 shortcut expansion
        assert graph.number_of_edges() == 2

    def test_no_shortcuts_when_disabled(self) -> None:
        place = E53_Place(id=uuid4(), class_code="E53", label="Athens")
        event = E5_Event(
            id=uuid4(), class_code="E5", label="Event", took_place_at=place.id
        )
        graph = build_graph_from_entities([event, place], expand_shortcuts=False)
        assert graph.number_of_edges() == 0

    def test_no_self_loops_by_default(self) -> None:
        import networkx as nx

        # Create entity where current_location points to its own ID
        own_id = uuid4()
        entity = E22_HumanMadeObject(
            id=own_id, class_code="E22", label="Vase", current_location=own_id
        )
        graph = build_graph_from_entities([entity], include_self_loops=False)
        assert nx.number_of_selfloops(graph) == 0


@pytest.mark.unit
class TestCreateTemporalGraph:
    def test_marks_temporal_nodes(self) -> None:
        timespan = E52_TimeSpan(id=uuid4(), class_code="E52", label="1879")
        event = E5_Event(
            id=uuid4(),
            class_code="E5",
            label="Birth",
            timespan=timespan.id,
        )
        temporal_graph = create_temporal_graph([event, timespan], [])
        # Check that nodes have has_temporal_info attribute set
        node_data = dict(temporal_graph.nodes(data=True))
        # Event has a timespan shortcut field — so its node_data will have "timespan" key
        event_node = node_data.get(str(event.id), {})
        assert "has_temporal_info" in event_node

    def test_empty_graph(self) -> None:
        temporal_graph = create_temporal_graph([], [])
        assert temporal_graph.number_of_nodes() == 0
