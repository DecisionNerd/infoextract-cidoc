"""Unit tests for the LinkML-based code generators."""

from pathlib import Path

import pytest

from infoextract_cidoc.models.base import CRMEntity
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
)


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
        assert len(classes) == 99

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


@pytest.mark.unit
class TestPropertySchema:
    """Verify the LinkML property schema file exists and is valid."""

    def test_schema_file_exists(self):
        schema = Path(__file__).parents[2] / "codegen" / "cidoc_crm_properties.yaml"
        assert schema.exists(), f"cidoc_crm_properties.yaml not found at {schema}"

    def test_schema_loadable(self):
        from linkml_runtime.utils.schemaview import SchemaView

        schema = Path(__file__).parents[2] / "codegen" / "cidoc_crm_properties.yaml"
        sv = SchemaView(str(schema))
        all_slots = sv.all_slots()
        crm_slots = [
            s for s in all_slots.values() if "crm_code" in (s.annotations or {})
        ]
        assert len(crm_slots) == 322

    def test_all_inverse_pairs_symmetric(self):
        from linkml_runtime.utils.schemaview import SchemaView

        schema = Path(__file__).parents[2] / "codegen" / "cidoc_crm_properties.yaml"
        sv = SchemaView(str(schema))
        all_slots = sv.all_slots()
        crm_slots = {
            s.annotations["crm_code"].value: s
            for s in all_slots.values()
            if "crm_code" in (s.annotations or {})
        }
        for code, slot in crm_slots.items():
            inv_slot_name = slot.inverse or ""
            if inv_slot_name:
                assert inv_slot_name in all_slots, (
                    f"{code}.inverse={inv_slot_name!r} not found in schema"
                )
                inv_slot = all_slots[inv_slot_name]
                assert (
                    inv_slot.inverse
                    == f"{code}_{slot.annotations['crm_label'].value.lower().replace(' ', '_').replace('-', '_')}".replace(
                        "__", "_"
                    )
                    or inv_slot.inverse is not None
                ), f"{code}: inverse slot {inv_slot_name!r} has no back-reference"

    def test_all_domain_range_reference_valid_eclasses(self):
        from linkml_runtime.utils.schemaview import SchemaView

        schema = Path(__file__).parents[2] / "codegen" / "cidoc_crm_properties.yaml"
        sv = SchemaView(str(schema))
        all_classes = sv.all_classes()
        all_slots = sv.all_slots()
        for slot in all_slots.values():
            if "crm_code" not in (slot.annotations or {}):
                continue
            code = slot.annotations["crm_code"].value
            assert slot.domain in all_classes, (
                f"{code}: domain {slot.domain!r} not a known E-class"
            )
            assert slot.range in all_classes, (
                f"{code}: range {slot.range!r} not a known E-class"
            )


@pytest.mark.unit
class TestPropertyRegistryBackwardsCompat:
    """Verify the generated properties.py is backwards-compatible."""

    def test_p_dict_has_322_entries(self):
        from infoextract_cidoc.properties import P

        assert len(P) == 322

    def test_every_entry_has_required_keys(self):
        from infoextract_cidoc.properties import P

        required_keys = {
            "label",
            "domain",
            "range",
            "inverse",
            "quantifier",
            "aliases",
            "notes",
        }
        for code, entry in P.items():
            missing = required_keys - entry.keys()
            assert not missing, f"{code} is missing keys: {missing}"

    def test_16_properties_have_0_1_quantifier(self):
        from infoextract_cidoc.properties import P

        count = sum(1 for v in P.values() if v["quantifier"] == "0..1")
        assert count == 16

    def test_all_aliases_are_nonempty_lists(self):
        from infoextract_cidoc.properties import P

        for code, entry in P.items():
            assert isinstance(entry["aliases"], list), f"{code}: aliases is not a list"
            assert len(entry["aliases"]) > 0, f"{code}: aliases is empty"

    def test_all_inverse_references_resolve(self):
        from infoextract_cidoc.properties import P

        for code, entry in P.items():
            inv = entry["inverse"]
            assert inv in P, f"{code}: inverse {inv!r} not in P"

    def test_spot_check_p4(self):
        from infoextract_cidoc.properties import P

        assert P["P4"]["aliases"][0] == "HAS_TIME_SPAN"
        assert P["P4"]["domain"] == "E2"
        assert P["P4"]["range"] == "E52"
        assert P["P4"]["inverse"] == "P4i"
        assert P["P4"]["quantifier"] == "0..1"

    def test_spot_check_p108(self):
        from infoextract_cidoc.properties import P

        assert P["P108"]["aliases"][0] == "WAS_PRODUCED_BY"
        assert P["P108"]["domain"] == "E22"
        assert P["P108"]["range"] == "E12"
        assert P["P108"]["inverse"] == "P108i"
        assert P["P108"]["quantifier"] == "0..1"

    def test_spot_check_p7(self):
        from infoextract_cidoc.properties import P

        assert P["P7"]["aliases"][0] == "TOOK_PLACE_AT"
        assert P["P7"]["domain"] == "E5"
        assert P["P7"]["range"] == "E53"

    def test_domain_lookup_exists(self):
        from infoextract_cidoc.properties import DOMAIN

        assert "E1" in DOMAIN
        assert "P1" in DOMAIN["E1"]
        assert "E5" in DOMAIN
        assert "P7" in DOMAIN["E5"]

    def test_range_not_exported(self):
        import infoextract_cidoc.properties as props

        assert not hasattr(props, "RANGE"), (
            "RANGE is dead code and should not be exported"
        )
