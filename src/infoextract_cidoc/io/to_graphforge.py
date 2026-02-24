"""GraphForge output module for infoextract-cidoc.

GraphForge is an optional dependency. Install with:
    pip install infoextract-cidoc[graphforge]
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from infoextract_cidoc.models.base import CRMEntity, CRMRelation


def _require_graphforge() -> Any:
    """Import graphforge or raise a helpful error."""
    try:
        import graphforge  # type: ignore[import]  # noqa: PLC0415
    except ImportError as e:
        msg = (
            "graphforge is required for GraphForge output. "
            "Install it with: pip install infoextract-cidoc[graphforge]"
        )
        raise ImportError(msg) from e
    else:
        return graphforge


def to_graphforge_graph(
    entities: list[CRMEntity],
    relations: list[CRMRelation],
) -> Any:
    """Build an in-process GraphForge graph from CRM entities and relations.

    Args:
        entities: List of CRMEntity instances.
        relations: List of CRMRelation instances.

    Returns:
        A GraphForge graph object.

    Raises:
        ImportError: If graphforge is not installed.
    """
    gf = _require_graphforge()

    graph = gf.Graph()

    for entity in entities:
        graph.add_node(
            str(entity.id),
            label=entity.label or "",
            class_code=entity.class_code,
            notes=entity.notes or "",
        )

    for relation in relations:
        graph.add_edge(
            str(relation.src),
            str(relation.tgt),
            type=relation.type,
        )

    return graph


def to_graphforge_cypher(
    entities: list[CRMEntity],
    relations: list[CRMRelation],
) -> str:
    """Generate Cypher via GraphForge's planner.

    Args:
        entities: List of CRMEntity instances.
        relations: List of CRMRelation instances.

    Returns:
        Cypher string for graph database import.

    Raises:
        ImportError: If graphforge is not installed.
    """
    graph = to_graphforge_graph(entities, relations)
    return graph.to_cypher()
