"""Unit tests for GraphForge output module."""

from unittest.mock import MagicMock, patch
import uuid

import pytest

from infoextract_cidoc.models.base import CRMEntity, CRMRelation


@pytest.fixture()
def sample_entities() -> list:
    return [
        CRMEntity(
            id=str(uuid.uuid4()),
            class_code="E21",
            label="Einstein",
            notes=None,
            type=["E21"],
        ),
        CRMEntity(
            id=str(uuid.uuid4()),
            class_code="E53",
            label="Ulm",
            notes=None,
            type=["E53"],
        ),
    ]


@pytest.fixture()
def sample_relations(sample_entities) -> list:
    return [
        CRMRelation(
            src=sample_entities[0].id,
            type="P98",
            tgt=sample_entities[1].id,
        )
    ]


@pytest.mark.unit
class TestGraphForgeOutput:
    def test_import_guard_raises_without_graphforge(
        self, sample_entities, sample_relations
    ) -> None:
        with patch.dict("sys.modules", {"graphforge": None}):
            from importlib import reload
            import infoextract_cidoc.io.to_graphforge as module
            # Force re-evaluation of import
            with pytest.raises(ImportError, match="graphforge is required"):
                module._require_graphforge()

    def test_to_graphforge_graph_with_mock(
        self, sample_entities, sample_relations
    ) -> None:
        mock_graph = MagicMock()
        mock_gf = MagicMock()
        mock_gf.Graph.return_value = mock_graph

        with patch.dict("sys.modules", {"graphforge": mock_gf}):
            from importlib import reload
            import infoextract_cidoc.io.to_graphforge as gf_module
            # Patch _require_graphforge to return our mock
            with patch.object(gf_module, "_require_graphforge", return_value=mock_gf):
                result = gf_module.to_graphforge_graph(sample_entities, sample_relations)

        assert result is mock_graph
        assert mock_graph.add_node.call_count == 2
        assert mock_graph.add_edge.call_count == 1
