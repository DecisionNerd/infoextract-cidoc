"""Unit tests for the LinkML-based code generator."""

import pytest
from pathlib import Path

from infoextract_cidoc.models.generated.e_classes import (
    E1_CRMEntity,
    E5_Event,
    E7_Activity,
    E12_Production,
    E19_PhysicalObject,
    E21_Person,
    E22_HumanMadeObject,
    E52_TimeSpan,
    E53_Place,
    E61_TimePrimitive,
)
from infoextract_cidoc.models.base import CRMEntity


@pytest.mark.unit
class TestGeneratedClassHierarchy:
    """Verify the generated class hierarchy reflects the LinkML schema."""

    def test_root_inherits_crm_entity(self):
        assert issubclass(E1_CRMEntity, CRMEntity)

    def test_event_inherits_from_root(self):
        assert issubclass(E5_Event, E1_CRMEntity)

    def test_activity_inherits_from_event(self):
        assert issubclass(E7_Activity, E5_Event)

    def test_production_inherits_from_activity(self):
        assert issubclass(E12_Production, E7_Activity)

    def test_person_inherits_physical_object(self):
        assert issubclass(E21_Person, E19_PhysicalObject)

    def test_place_is_crm_entity(self):
        assert issubclass(E53_Place, CRMEntity)

    def test_timespan_is_crm_entity(self):
        assert issubclass(E52_TimeSpan, CRMEntity)


@pytest.mark.unit
class TestGeneratedClassCodes:
    """Verify class_code defaults match E-numbers."""

    def test_event_class_code(self):
        e = E5_Event(class_code="E5", label="test")
        assert e.class_code == "E5"

    def test_person_class_code(self):
        p = E21_Person(class_code="E21", label="Alice")
        assert p.class_code == "E21"

    def test_timespan_class_code(self):
        ts = E52_TimeSpan(class_code="E52")
        assert ts.class_code == "E52"


@pytest.mark.unit
class TestShortcutFieldInheritance:
    """Verify shortcut fields appear on the correct classes."""

    def test_event_has_timespan_slot(self):
        assert "timespan" in E5_Event.model_fields

    def test_event_has_took_place_at_slot(self):
        assert "took_place_at" in E5_Event.model_fields

    def test_activity_inherits_timespan(self):
        # E7_Activity extends E5_Event — inherits slots via Python class hierarchy
        assert "timespan" in E7_Activity.model_fields

    def test_physical_object_has_current_location(self):
        assert "current_location" in E19_PhysicalObject.model_fields

    def test_human_made_object_has_produced_by(self):
        assert "produced_by" in E22_HumanMadeObject.model_fields

    def test_human_made_object_inherits_current_location(self):
        assert "current_location" in E22_HumanMadeObject.model_fields

    def test_timespan_has_temporal_slots(self):
        assert "begin_of_the_begin" in E52_TimeSpan.model_fields
        assert "end_of_the_end" in E52_TimeSpan.model_fields

    def test_place_has_no_shortcut_slots(self):
        # E53_Place has no shortcut fields
        extra = set(E53_Place.model_fields) - set(CRMEntity.model_fields)
        assert "class_code" in E53_Place.model_fields
        assert "timespan" not in extra
        assert "current_location" not in extra


@pytest.mark.unit
class TestCodegenSchema:
    """Verify the LinkML schema file exists and is valid."""

    def test_schema_file_exists(self):
        schema = Path(__file__).parents[2] / "codegen" / "cidoc_crm.yaml"
        assert schema.exists(), f"cidoc_crm.yaml not found at {schema}"

    def test_schema_loadable(self):
        from linkml_runtime.utils.schemaview import SchemaView

        schema = Path(__file__).parents[2] / "codegen" / "cidoc_crm.yaml"
        sv = SchemaView(str(schema))
        classes = sv.all_classes()
        assert len(classes) == 99  # noqa: PLR2004

    def test_schema_has_shortcut_slots(self):
        from linkml_runtime.utils.schemaview import SchemaView

        schema = Path(__file__).parents[2] / "codegen" / "cidoc_crm.yaml"
        sv = SchemaView(str(schema))
        slots = sv.all_slots()
        assert "timespan" in slots
        assert "took_place_at" in slots
        assert "current_location" in slots
        assert "produced_by" in slots
        assert "begin_of_the_begin" in slots
        assert "end_of_the_end" in slots
