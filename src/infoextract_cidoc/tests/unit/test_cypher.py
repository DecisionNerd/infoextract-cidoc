"""
Unit tests for Cypher emitters.
"""

from uuid import uuid4

from ...io.to_cypher import (
    emit_nodes,
    emit_relationships,
    expand_shortcuts,
    generate_cypher_parameters,
    generate_cypher_script,
    validate_cypher_script,
)
from ...models.generated.e_classes import (
    EE22_HumanMadeObject,
    EE53_Place,
)


class TestCypherEmission:
    """Test Cypher emission functionality."""

    def test_emit_nodes(self):
        """Test node emission."""
        entities = [
            EE22_HumanMadeObject(
                id=uuid4(), class_code="E22", label="Ancient Vase", type=["E55:Vessel"]
            ),
            EE53_Place(id=uuid4(), class_code="E53", label="Athens, Greece"),
        ]

        result = emit_nodes(entities)

        assert "nodes" in result
        assert len(result["nodes"]) == 2

        # Check first node
        node1 = result["nodes"][0]
        assert isinstance(node1["id"], str)  # Should be UUID converted to string
        assert node1["class_code"] == "E22"
        assert node1["label"] == "Ancient Vase"
        assert node1["type"] == ["E55:Vessel"]

        # Check second node
        node2 = result["nodes"][1]
        assert isinstance(node2["id"], str)  # Should be UUID converted to string
        assert node2["class_code"] == "E53"
        assert node2["label"] == "Athens, Greece"

    def test_emit_relationships(self):
        """Test relationship emission."""
        entities = [
            EE22_HumanMadeObject(
                id=uuid4(),
                class_code="E22",
                current_location=uuid4(),
                produced_by=uuid4(),
            )
        ]

        result = emit_relationships(entities)

        assert "rels" in result
        assert len(result["rels"]) == 2

        # Check relationships
        rel_types = [rel["type"] for rel in result["rels"]]
        assert "P53_HAS_CURRENT_LOCATION" in rel_types
        assert "P108_WAS_PRODUCED_BY" in rel_types

        # Check relationship structure
        for rel in result["rels"]:
            assert "src" in rel
            assert "type" in rel
            assert "tgt" in rel
            assert isinstance(rel["src"], str)  # Should be UUID converted to string

    def test_expand_shortcuts(self):
        """Test shortcut expansion."""
        entity = EE22_HumanMadeObject(
            id=uuid4(), class_code="E22", current_location=uuid4(), produced_by=uuid4()
        )

        relationships = expand_shortcuts(entity)

        assert len(relationships) == 2

        # Check specific relationships
        rel_dict = {rel["type"]: rel for rel in relationships}

        assert "P53_HAS_CURRENT_LOCATION" in rel_dict
        assert isinstance(
            rel_dict["P53_HAS_CURRENT_LOCATION"]["tgt"], str
        )  # Should be UUID converted to string

        assert "P108_WAS_PRODUCED_BY" in rel_dict
        assert isinstance(
            rel_dict["P108_WAS_PRODUCED_BY"]["tgt"], str
        )  # Should be UUID converted to string

    def test_generate_cypher_script(self):
        """Test Cypher script generation."""
        entities = [
            EE22_HumanMadeObject(id=uuid4(), class_code="E22", label="Ancient Vase"),
            EE53_Place(id=uuid4(), class_code="E53", label="Athens, Greece"),
        ]

        script = generate_cypher_script(entities)

        # Check that script contains expected elements
        assert "-- Create constraints" in script
        assert "CREATE CONSTRAINT crm_id" in script
        assert "-- Create nodes" in script
        assert "UNWIND $nodes_0 AS n" in script
        assert "MERGE (x:CRM {id: n.id})" in script
        assert "SET x.class_code = n.class_code" in script

    def test_generate_cypher_parameters(self):
        """Test Cypher parameter generation."""
        entities = [
            EE22_HumanMadeObject(id="obj_001", class_code="E22", label="Ancient Vase")
        ]

        params = generate_cypher_parameters(entities)

        # Check that parameters are generated
        assert "nodes_0" in params
        assert len(params["nodes_0"]) == 1

        # Check node data
        node = params["nodes_0"][0]
        # The ID will be converted to a deterministic UUID from "obj_001"
        assert node["class_code"] == "E22"
        assert node["label"] == "Ancient Vase"

    def test_cypher_script_with_relationships(self):
        """Test Cypher script generation with relationships."""
        # Use proper UUIDs for the test
        vase_id = "550e8400-e29b-41d4-a716-446655440000"
        place_id = "550e8400-e29b-41d4-a716-446655440001"

        entities = [
            EE22_HumanMadeObject(
                id=vase_id, class_code="E22", current_location=place_id
            ),
            EE53_Place(id=place_id, class_code="E53", label="Athens, Greece"),
        ]

        script = generate_cypher_script(entities)

        # Check that relationship creation is included
        assert "-- Create relationships" in script
        assert "UNWIND $rels_P53_HAS_CURRENT_LOCATION_0 AS r" in script
        assert "MATCH (s:CRM {id: r.src})" in script
        assert "MATCH (t:CRM {id: r.tgt})" in script
        assert "MERGE (s)-[:`P53_HAS_CURRENT_LOCATION`]->(t);" in script

    def test_cypher_parameters_with_relationships(self):
        """Test Cypher parameter generation with relationships."""
        # Use proper UUIDs for the test
        vase_id = "550e8400-e29b-41d4-a716-446655440000"
        place_id = "550e8400-e29b-41d4-a716-446655440001"

        entities = [
            EE22_HumanMadeObject(
                id=vase_id, class_code="E22", current_location=place_id
            ),
            EE53_Place(id=place_id, class_code="E53", label="Athens, Greece"),
        ]

        params = generate_cypher_parameters(entities)

        # Check that relationship parameters are generated
        assert "rels_P53_HAS_CURRENT_LOCATION_0" in params
        assert len(params["rels_P53_HAS_CURRENT_LOCATION_0"]) == 1

        # Check relationship data
        rel = params["rels_P53_HAS_CURRENT_LOCATION_0"][0]
        assert rel["src"] == vase_id
        assert rel["type"] == "P53_HAS_CURRENT_LOCATION"
        assert rel["tgt"] == place_id

    def test_validate_cypher_script(self):
        """Test Cypher script validation."""
        # Valid script
        valid_script = """
        UNWIND $nodes AS n
        MERGE (x:CRM {id: n.id})
        SET x.class_code = n.class_code;
        """

        issues = validate_cypher_script(valid_script)
        assert len(issues) == 0

        # Script with potential issues
        problematic_script = """
        CREATE (x:CRM {id: 'test'})
        """

        issues = validate_cypher_script(problematic_script)
        assert len(issues) > 0
        assert any("MERGE" in issue for issue in issues)

    def test_empty_entities(self):
        """Test handling of empty entities list."""
        script = generate_cypher_script([])
        params = generate_cypher_parameters([])

        # Should still generate constraints
        assert "CREATE CONSTRAINT" in script
        assert len(params) == 0

    def test_batch_size_handling(self):
        """Test custom batch size handling."""
        entities = [
            EE22_HumanMadeObject(id=f"obj_{i:03d}", class_code="E22") for i in range(5)
        ]

        # Test with small batch size
        script = generate_cypher_script(entities, batch_size=2)
        params = generate_cypher_parameters(entities, batch_size=2)

        # Should create multiple batches
        assert "UNWIND $nodes_0 AS n" in script
        assert "UNWIND $nodes_1 AS n" in script
        assert "UNWIND $nodes_2 AS n" in script

        assert "nodes_0" in params
        assert "nodes_1" in params
        assert "nodes_2" in params
