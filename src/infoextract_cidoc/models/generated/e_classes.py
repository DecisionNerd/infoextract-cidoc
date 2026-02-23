"""
Auto-generated CIDOC CRM E-class models.
Generated from YAML specifications in codegen/specs/
"""

from uuid import UUID

from infoextract_cidoc.models.base import CRMEntity


class EE1_CRMEntity(CRMEntity):
    """CIDOC CRM E1: CRM Entity (Abstract)"""

    class_code: str = "E1"

    class Config:
        json_schema_extra = {
            "description": "CRM Entity",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE2_TemporalEntity(EE1_CRMEntity):
    """CIDOC CRM E2: Temporal Entity (Abstract)"""

    class_code: str = "E2"

    class Config:
        json_schema_extra = {
            "description": "Temporal Entity",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE3_ConditionState(EE2_TemporalEntity):
    """CIDOC CRM E3: Condition State"""

    class_code: str = "E3"

    class Config:
        json_schema_extra = {
            "description": "Condition State",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE4_Period(EE2_TemporalEntity):
    """CIDOC CRM E4: Period"""

    class_code: str = "E4"

    class Config:
        json_schema_extra = {
            "description": "Period",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE5_Event(EE2_TemporalEntity):
    """CIDOC CRM E5: Event"""

    class_code: str = "E5"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Event",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE6_Destruction(EE5_Event):
    """CIDOC CRM E6: Destruction"""

    class_code: str = "E6"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Destruction",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE7_Activity(EE5_Event):
    """CIDOC CRM E7: Activity"""

    class_code: str = "E7"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Activity",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE8_Acquisition(EE7_Activity):
    """CIDOC CRM E8: Acquisition"""

    class_code: str = "E8"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Acquisition",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE9_Move(EE7_Activity):
    """CIDOC CRM E9: Move"""

    class_code: str = "E9"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Move",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE10_TransferofCustody(EE7_Activity):
    """CIDOC CRM E10: Transfer of Custody"""

    class_code: str = "E10"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Transfer of Custody",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE11_Modification(EE7_Activity):
    """CIDOC CRM E11: Modification"""

    class_code: str = "E11"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Modification",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE12_Production(EE7_Activity):
    """CIDOC CRM E12: Production"""

    class_code: str = "E12"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Production",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE13_AttributeAssignment(EE7_Activity):
    """CIDOC CRM E13: Attribute Assignment"""

    class_code: str = "E13"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Attribute Assignment",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE14_ConditionAssessment(EE13_AttributeAssignment):
    """CIDOC CRM E14: Condition Assessment"""

    class_code: str = "E14"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Condition Assessment",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE15_IdentifierAssignment(EE13_AttributeAssignment):
    """CIDOC CRM E15: Identifier Assignment"""

    class_code: str = "E15"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Identifier Assignment",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE16_Measurement(EE13_AttributeAssignment):
    """CIDOC CRM E16: Measurement"""

    class_code: str = "E16"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Measurement",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE17_TypeAssignment(EE13_AttributeAssignment):
    """CIDOC CRM E17: Type Assignment"""

    class_code: str = "E17"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Type Assignment",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE18_PhysicalThing(EE1_CRMEntity):
    """CIDOC CRM E18: Physical Thing (Abstract)"""

    class_code: str = "E18"

    class Config:
        json_schema_extra = {
            "description": "Physical Thing",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE19_PhysicalObject(EE18_PhysicalThing):
    """CIDOC CRM E19: Physical Object"""

    class_code: str = "E19"

    current_location: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Physical Object",
            "canonical_fields": ["label", "type", "notes", "current_location"],
        }


class EE20_BiologicalObject(EE19_PhysicalObject):
    """CIDOC CRM E20: Biological Object"""

    class_code: str = "E20"

    current_location: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Biological Object",
            "canonical_fields": ["label", "type", "notes", "current_location"],
        }


class EE21_Person(EE20_BiologicalObject):
    """CIDOC CRM E21: Person"""

    class_code: str = "E21"

    current_location: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Person",
            "canonical_fields": ["label", "type", "notes", "current_location"],
        }


class EE22_HumanMadeObject(EE19_PhysicalObject):
    """CIDOC CRM E22: Human-Made Object"""

    class_code: str = "E22"

    current_location: UUID | None = None
    produced_by: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Human-Made Object",
            "canonical_fields": [
                "label",
                "type",
                "notes",
                "current_location",
                "produced_by",
            ],
        }


class EE23_ConceptualObject(EE1_CRMEntity):
    """CIDOC CRM E23: Conceptual Object (Abstract)"""

    class_code: str = "E23"

    class Config:
        json_schema_extra = {
            "description": "Conceptual Object",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE24_PhysicalManMadeThing(EE18_PhysicalThing):
    """CIDOC CRM E24: Physical Man-Made Thing"""

    class_code: str = "E24"

    current_location: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Physical Man-Made Thing",
            "canonical_fields": ["label", "type", "notes", "current_location"],
        }


class EE25_ManMadeFeature(EE24_PhysicalManMadeThing):
    """CIDOC CRM E25: Man-Made Feature"""

    class_code: str = "E25"

    current_location: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Man-Made Feature",
            "canonical_fields": ["label", "type", "notes", "current_location"],
        }


class EE26_PhysicalFeature(EE18_PhysicalThing):
    """CIDOC CRM E26: Physical Feature"""

    class_code: str = "E26"

    current_location: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Physical Feature",
            "canonical_fields": ["label", "type", "notes", "current_location"],
        }


class EE27_Site(EE26_PhysicalFeature):
    """CIDOC CRM E27: Site"""

    class_code: str = "E27"

    current_location: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Site",
            "canonical_fields": ["label", "type", "notes", "current_location"],
        }


class EE28_ConceptualObject(EE23_ConceptualObject):
    """CIDOC CRM E28: Conceptual Object"""

    class_code: str = "E28"

    class Config:
        json_schema_extra = {
            "description": "Conceptual Object",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE29_DesignorProcedure(EE28_ConceptualObject):
    """CIDOC CRM E29: Design or Procedure"""

    class_code: str = "E29"

    class Config:
        json_schema_extra = {
            "description": "Design or Procedure",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE30_Right(EE28_ConceptualObject):
    """CIDOC CRM E30: Right"""

    class_code: str = "E30"

    class Config:
        json_schema_extra = {
            "description": "Right",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE31_Document(EE28_ConceptualObject):
    """CIDOC CRM E31: Document"""

    class_code: str = "E31"

    class Config:
        json_schema_extra = {
            "description": "Document",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE32_AuthorityDocument(EE31_Document):
    """CIDOC CRM E32: Authority Document"""

    class_code: str = "E32"

    class Config:
        json_schema_extra = {
            "description": "Authority Document",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE33_LinguisticObject(EE28_ConceptualObject):
    """CIDOC CRM E33: Linguistic Object"""

    class_code: str = "E33"

    class Config:
        json_schema_extra = {
            "description": "Linguistic Object",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE34_Inscription(EE33_LinguisticObject):
    """CIDOC CRM E34: Inscription"""

    class_code: str = "E34"

    class Config:
        json_schema_extra = {
            "description": "Inscription",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE35_Title(EE33_LinguisticObject):
    """CIDOC CRM E35: Title"""

    class_code: str = "E35"

    class Config:
        json_schema_extra = {
            "description": "Title",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE36_VisualItem(EE28_ConceptualObject):
    """CIDOC CRM E36: Visual Item"""

    class_code: str = "E36"

    class Config:
        json_schema_extra = {
            "description": "Visual Item",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE37_Mark(EE36_VisualItem):
    """CIDOC CRM E37: Mark"""

    class_code: str = "E37"

    class Config:
        json_schema_extra = {
            "description": "Mark",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE38_Image(EE36_VisualItem):
    """CIDOC CRM E38: Image"""

    class_code: str = "E38"

    class Config:
        json_schema_extra = {
            "description": "Image",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE39_Actor(EE1_CRMEntity):
    """CIDOC CRM E39: Actor (Abstract)"""

    class_code: str = "E39"

    class Config:
        json_schema_extra = {
            "description": "Actor",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE40_LegalBody(EE39_Actor):
    """CIDOC CRM E40: Legal Body"""

    class_code: str = "E40"

    class Config:
        json_schema_extra = {
            "description": "Legal Body",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE41_Appellation(EE28_ConceptualObject):
    """CIDOC CRM E41: Appellation"""

    class_code: str = "E41"

    class Config:
        json_schema_extra = {
            "description": "Appellation",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE42_Identifier(EE28_ConceptualObject):
    """CIDOC CRM E42: Identifier"""

    class_code: str = "E42"

    class Config:
        json_schema_extra = {
            "description": "Identifier",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE43_Place(EE1_CRMEntity):
    """CIDOC CRM E43: Place (Abstract)"""

    class_code: str = "E43"

    class Config:
        json_schema_extra = {
            "description": "Place",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE44_PlaceAppellation(EE41_Appellation):
    """CIDOC CRM E44: Place Appellation"""

    class_code: str = "E44"

    class Config:
        json_schema_extra = {
            "description": "Place Appellation",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE45_Address(EE44_PlaceAppellation):
    """CIDOC CRM E45: Address"""

    class_code: str = "E45"

    class Config:
        json_schema_extra = {
            "description": "Address",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE46_Section(EE43_Place):
    """CIDOC CRM E46: Section"""

    class_code: str = "E46"

    class Config:
        json_schema_extra = {
            "description": "Section",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE47_SpatialCoordinates(EE28_ConceptualObject):
    """CIDOC CRM E47: Spatial Coordinates"""

    class_code: str = "E47"

    class Config:
        json_schema_extra = {
            "description": "Spatial Coordinates",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE48_PlaceName(EE44_PlaceAppellation):
    """CIDOC CRM E48: Place Name"""

    class_code: str = "E48"

    class Config:
        json_schema_extra = {
            "description": "Place Name",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE49_TimeAppellation(EE41_Appellation):
    """CIDOC CRM E49: Time Appellation"""

    class_code: str = "E49"

    class Config:
        json_schema_extra = {
            "description": "Time Appellation",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE50_Date(EE49_TimeAppellation):
    """CIDOC CRM E50: Date"""

    class_code: str = "E50"

    class Config:
        json_schema_extra = {
            "description": "Date",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE51_ContactPoint(EE45_Address):
    """CIDOC CRM E51: Contact Point"""

    class_code: str = "E51"

    class Config:
        json_schema_extra = {
            "description": "Contact Point",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE52_TimeSpan(EE1_CRMEntity):
    """CIDOC CRM E52: Time-Span"""

    class_code: str = "E52"

    begin_of_the_begin: UUID | None = None
    end_of_the_end: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Time-Span",
            "canonical_fields": [
                "label",
                "type",
                "notes",
                "begin_of_the_begin",
                "end_of_the_end",
            ],
        }


class EE53_Place(EE43_Place):
    """CIDOC CRM E53: Place"""

    class_code: str = "E53"

    class Config:
        json_schema_extra = {
            "description": "Place",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE54_Dimension(EE28_ConceptualObject):
    """CIDOC CRM E54: Dimension"""

    class_code: str = "E54"

    class Config:
        json_schema_extra = {
            "description": "Dimension",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE55_Type(EE28_ConceptualObject):
    """CIDOC CRM E55: Type"""

    class_code: str = "E55"

    class Config:
        json_schema_extra = {
            "description": "Type",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE56_Language(EE55_Type):
    """CIDOC CRM E56: Language"""

    class_code: str = "E56"

    class Config:
        json_schema_extra = {
            "description": "Language",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE57_Material(EE55_Type):
    """CIDOC CRM E57: Material"""

    class_code: str = "E57"

    class Config:
        json_schema_extra = {
            "description": "Material",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE58_MeasurementUnit(EE55_Type):
    """CIDOC CRM E58: Measurement Unit"""

    class_code: str = "E58"

    class Config:
        json_schema_extra = {
            "description": "Measurement Unit",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE59_PrimitiveValue(EE1_CRMEntity):
    """CIDOC CRM E59: Primitive Value (Abstract)"""

    class_code: str = "E59"

    class Config:
        json_schema_extra = {
            "description": "Primitive Value",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE60_Number(EE59_PrimitiveValue):
    """CIDOC CRM E60: Number"""

    class_code: str = "E60"

    class Config:
        json_schema_extra = {
            "description": "Number",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE61_TimePrimitive(EE59_PrimitiveValue):
    """CIDOC CRM E61: Time Primitive"""

    class_code: str = "E61"

    class Config:
        json_schema_extra = {
            "description": "Time Primitive",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE62_String(EE59_PrimitiveValue):
    """CIDOC CRM E62: String"""

    class_code: str = "E62"

    class Config:
        json_schema_extra = {
            "description": "String",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE63_BeginningofExistence(EE5_Event):
    """CIDOC CRM E63: Beginning of Existence"""

    class_code: str = "E63"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Beginning of Existence",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE64_EndofExistence(EE5_Event):
    """CIDOC CRM E64: End of Existence"""

    class_code: str = "E64"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "End of Existence",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE65_Creation(EE63_BeginningofExistence):
    """CIDOC CRM E65: Creation"""

    class_code: str = "E65"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Creation",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE66_Formation(EE63_BeginningofExistence):
    """CIDOC CRM E66: Formation"""

    class_code: str = "E66"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Formation",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE67_Birth(EE66_Formation):
    """CIDOC CRM E67: Birth"""

    class_code: str = "E67"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Birth",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE68_Dissolution(EE64_EndofExistence):
    """CIDOC CRM E68: Dissolution"""

    class_code: str = "E68"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Dissolution",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE69_Death(EE64_EndofExistence):
    """CIDOC CRM E69: Death"""

    class_code: str = "E69"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Death",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE70_Thing(EE1_CRMEntity):
    """CIDOC CRM E70: Thing (Abstract)"""

    class_code: str = "E70"

    class Config:
        json_schema_extra = {
            "description": "Thing",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE71_HumanMadeThing(EE70_Thing):
    """CIDOC CRM E71: Human-Made Thing"""

    class_code: str = "E71"

    class Config:
        json_schema_extra = {
            "description": "Human-Made Thing",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE72_LegalObject(EE70_Thing):
    """CIDOC CRM E72: Legal Object"""

    class_code: str = "E72"

    class Config:
        json_schema_extra = {
            "description": "Legal Object",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE73_InformationObject(EE70_Thing):
    """CIDOC CRM E73: Information Object"""

    class_code: str = "E73"

    class Config:
        json_schema_extra = {
            "description": "Information Object",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE74_Group(EE39_Actor):
    """CIDOC CRM E74: Group"""

    class_code: str = "E74"

    class Config:
        json_schema_extra = {
            "description": "Group",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE75_ConceptualObjectAppellation(EE41_Appellation):
    """CIDOC CRM E75: Conceptual Object Appellation"""

    class_code: str = "E75"

    class Config:
        json_schema_extra = {
            "description": "Conceptual Object Appellation",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE76_ConceptualObjectIdentifier(EE42_Identifier):
    """CIDOC CRM E76: Conceptual Object Identifier"""

    class_code: str = "E76"

    class Config:
        json_schema_extra = {
            "description": "Conceptual Object Identifier",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE77_PersistentItem(EE1_CRMEntity):
    """CIDOC CRM E77: Persistent Item"""

    class_code: str = "E77"

    class Config:
        json_schema_extra = {
            "description": "Persistent Item",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE78_CuratedHolding(EE77_PersistentItem):
    """CIDOC CRM E78: Curated Holding"""

    class_code: str = "E78"

    class Config:
        json_schema_extra = {
            "description": "Curated Holding",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE79_PartAddition(EE11_Modification):
    """CIDOC CRM E79: Part Addition"""

    class_code: str = "E79"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Part Addition",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE80_PartRemoval(EE11_Modification):
    """CIDOC CRM E80: Part Removal"""

    class_code: str = "E80"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Part Removal",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE81_Transformation(EE11_Modification):
    """CIDOC CRM E81: Transformation"""

    class_code: str = "E81"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Transformation",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE82_ActorAppellation(EE75_ConceptualObjectAppellation):
    """CIDOC CRM E82: Actor Appellation"""

    class_code: str = "E82"

    class Config:
        json_schema_extra = {
            "description": "Actor Appellation",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE83_TypeCreation(EE65_Creation):
    """CIDOC CRM E83: Type Creation"""

    class_code: str = "E83"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Type Creation",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE84_InformationCarrier(EE73_InformationObject):
    """CIDOC CRM E84: Information Carrier"""

    class_code: str = "E84"

    class Config:
        json_schema_extra = {
            "description": "Information Carrier",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE85_Joining(EE7_Activity):
    """CIDOC CRM E85: Joining"""

    class_code: str = "E85"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Joining",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE86_Leaving(EE7_Activity):
    """CIDOC CRM E86: Leaving"""

    class_code: str = "E86"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Leaving",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE87_CurationActivity(EE7_Activity):
    """CIDOC CRM E87: Curation Activity"""

    class_code: str = "E87"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Curation Activity",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE88_PropositionalObject(EE28_ConceptualObject):
    """CIDOC CRM E88: Propositional Object"""

    class_code: str = "E88"

    class Config:
        json_schema_extra = {
            "description": "Propositional Object",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE89_PropositionalStatement(EE88_PropositionalObject):
    """CIDOC CRM E89: Propositional Statement"""

    class_code: str = "E89"

    class Config:
        json_schema_extra = {
            "description": "Propositional Statement",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE90_SymbolicObject(EE28_ConceptualObject):
    """CIDOC CRM E90: Symbolic Object"""

    class_code: str = "E90"

    class Config:
        json_schema_extra = {
            "description": "Symbolic Object",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE91_KnowledgeObject(EE90_SymbolicObject):
    """CIDOC CRM E91: Knowledge Object"""

    class_code: str = "E91"

    class Config:
        json_schema_extra = {
            "description": "Knowledge Object",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE92_SpacetimeVolume(EE1_CRMEntity):
    """CIDOC CRM E92: Spacetime Volume"""

    class_code: str = "E92"

    class Config:
        json_schema_extra = {
            "description": "Spacetime Volume",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE93_Presence(EE92_SpacetimeVolume):
    """CIDOC CRM E93: Presence"""

    class_code: str = "E93"

    class Config:
        json_schema_extra = {
            "description": "Presence",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE94_Space(EE92_SpacetimeVolume):
    """CIDOC CRM E94: Space"""

    class_code: str = "E94"

    class Config:
        json_schema_extra = {
            "description": "Space",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE95_SpacetimePrimitive(EE59_PrimitiveValue):
    """CIDOC CRM E95: Spacetime Primitive"""

    class_code: str = "E95"

    class Config:
        json_schema_extra = {
            "description": "Spacetime Primitive",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE96_Purchase(EE8_Acquisition):
    """CIDOC CRM E96: Purchase"""

    class_code: str = "E96"

    timespan: UUID | None = None
    took_place_at: UUID | None = None

    class Config:
        json_schema_extra = {
            "description": "Purchase",
            "canonical_fields": ["label", "type", "notes", "timespan", "took_place_at"],
        }


class EE97_MonetaryAmount(EE28_ConceptualObject):
    """CIDOC CRM E97: Monetary Amount"""

    class_code: str = "E97"

    class Config:
        json_schema_extra = {
            "description": "Monetary Amount",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE98_Currency(EE55_Type):
    """CIDOC CRM E98: Currency"""

    class_code: str = "E98"

    class Config:
        json_schema_extra = {
            "description": "Currency",
            "canonical_fields": ["label", "type", "notes"],
        }


class EE99_ProductType(EE55_Type):
    """CIDOC CRM E99: Product Type"""

    class_code: str = "E99"

    class Config:
        json_schema_extra = {
            "description": "Product Type",
            "canonical_fields": ["label", "type", "notes"],
        }
