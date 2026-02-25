"""
Auto-generated CIDOC CRM E-class models.
Source of truth: codegen/cidoc_crm.yaml (LinkML schema)

DO NOT EDIT — regenerate with: make codegen
"""

from __future__ import annotations

from uuid import UUID

from pydantic import Field

from infoextract_cidoc.models.base import CRMEntity


class E1_CRMEntity(CRMEntity):
    """E1: CRM Entity — the most abstract CRM class"""

    class_code: str = "E1"


class E18_PhysicalThing(E1_CRMEntity):
    """E18: Physical Thing — a material thing that occupies space"""

    class_code: str = "E18"


class E23_ConceptualObject(E1_CRMEntity):
    """E23: Conceptual Object (abstract) — immaterial, conceptual items"""

    class_code: str = "E23"


class E2_TemporalEntity(E1_CRMEntity):
    """E2: Temporal Entity — entities that persist through time"""

    class_code: str = "E2"


class E39_Actor(E1_CRMEntity):
    """E39: Actor — a person or group capable of intentional action"""

    class_code: str = "E39"


class E43_Place(E1_CRMEntity):
    """E43: Place (abstract) — a location in space"""

    class_code: str = "E43"


class E52_TimeSpan(E1_CRMEntity):
    """E52: Time-Span — a temporal extent defined by begin and end"""

    class_code: str = "E52"

    begin_of_the_begin: UUID | None = Field(
        None,
        description="P79: beginning is qualified by — shortcut to E61_TimePrimitive entity ID",
    )
    end_of_the_end: UUID | None = Field(
        None,
        description="P80: end is qualified by — shortcut to E61_TimePrimitive entity ID",
    )


class E59_PrimitiveValue(E1_CRMEntity):
    """E59: Primitive Value — a primitive data value"""

    class_code: str = "E59"


class E70_Thing(E1_CRMEntity):
    """E70: Thing — anything with identity"""

    class_code: str = "E70"


class E77_PersistentItem(E1_CRMEntity):
    """E77: Persistent Item — an item that persists through time"""

    class_code: str = "E77"


class E92_SpacetimeVolume(E1_CRMEntity):
    """E92: Spacetime Volume — a volume in spacetime"""

    class_code: str = "E92"


class E19_PhysicalObject(E18_PhysicalThing):
    """E19: Physical Object — a discrete physical object"""

    class_code: str = "E19"

    current_location: UUID | None = Field(
        None,
        description="P53: has current or former location — shortcut to E53_Place entity ID",
    )


class E24_PhysicalManMadeThing(E18_PhysicalThing):
    """E24: Physical Man-Made Thing — a physical man-made thing"""

    class_code: str = "E24"

    current_location: UUID | None = Field(
        None,
        description="P53: has current or former location — shortcut to E53_Place entity ID",
    )


class E26_PhysicalFeature(E18_PhysicalThing):
    """E26: Physical Feature — a physical feature of an object or location"""

    class_code: str = "E26"

    current_location: UUID | None = Field(
        None,
        description="P53: has current or former location — shortcut to E53_Place entity ID",
    )


class E28_ConceptualObject(E23_ConceptualObject):
    """E28: Conceptual Object — a non-material conceptual item"""

    class_code: str = "E28"


class E3_ConditionState(E2_TemporalEntity):
    """E3: Condition State — a physical condition of an object"""

    class_code: str = "E3"


class E4_Period(E2_TemporalEntity):
    """E4: Period — a named historical or cultural period"""

    class_code: str = "E4"


class E5_Event(E2_TemporalEntity):
    """E5: Event — something that happens and has spatiotemporal extent"""

    class_code: str = "E5"

    timespan: UUID | None = Field(
        None, description="P4: has time-span — shortcut to E52_TimeSpan entity ID"
    )
    took_place_at: UUID | None = Field(
        None, description="P7: took place at — shortcut to E53_Place entity ID"
    )


class E40_LegalBody(E39_Actor):
    """E40: Legal Body — a legal body such as a corporation or institution"""

    class_code: str = "E40"


class E74_Group(E39_Actor):
    """E74: Group — a group of people or organisations"""

    class_code: str = "E74"


class E46_Section(E43_Place):
    """E46: Section — a named section of a place"""

    class_code: str = "E46"


class E53_Place(E43_Place):
    """E53: Place — a location defined in space"""

    class_code: str = "E53"


class E60_Number(E59_PrimitiveValue):
    """E60: Number — a numeric value"""

    class_code: str = "E60"


class E61_TimePrimitive(E59_PrimitiveValue):
    """E61: Time Primitive — a primitive time value"""

    class_code: str = "E61"


class E62_String(E59_PrimitiveValue):
    """E62: String — a string value"""

    class_code: str = "E62"


class E95_SpacetimePrimitive(E59_PrimitiveValue):
    """E95: Spacetime Primitive — a primitive spacetime coordinate"""

    class_code: str = "E95"


class E71_HumanMadeThing(E70_Thing):
    """E71: Human-Made Thing — a human-made thing (abstract)"""

    class_code: str = "E71"


class E72_LegalObject(E70_Thing):
    """E72: Legal Object — something with legal significance"""

    class_code: str = "E72"


class E73_InformationObject(E70_Thing):
    """E73: Information Object — an information object"""

    class_code: str = "E73"


class E78_CuratedHolding(E77_PersistentItem):
    """E78: Curated Holding — a managed collection of objects"""

    class_code: str = "E78"


class E93_Presence(E92_SpacetimeVolume):
    """E93: Presence — the presence of an entity in a spacetime volume"""

    class_code: str = "E93"


class E94_Space(E92_SpacetimeVolume):
    """E94: Space — a geometric space"""

    class_code: str = "E94"


class E20_BiologicalObject(E19_PhysicalObject):
    """E20: Biological Object — a biological object"""

    class_code: str = "E20"


class E22_HumanMadeObject(E19_PhysicalObject):
    """E22: Human-Made Object — a physical object intentionally made by humans"""

    class_code: str = "E22"

    produced_by: UUID | None = Field(
        None, description="P108: was produced by — shortcut to E12_Production entity ID"
    )


class E25_ManMadeFeature(E24_PhysicalManMadeThing):
    """E25: Man-Made Feature — a man-made feature in the landscape"""

    class_code: str = "E25"


class E27_Site(E26_PhysicalFeature):
    """E27: Site — an area of land of cultural heritage significance"""

    class_code: str = "E27"


class E29_DesignOrProcedure(E28_ConceptualObject):
    """E29: Design or Procedure — a design or procedural prescription"""

    class_code: str = "E29"


class E30_Right(E28_ConceptualObject):
    """E30: Right — a legal right"""

    class_code: str = "E30"


class E31_Document(E28_ConceptualObject):
    """E31: Document — a document containing propositional content"""

    class_code: str = "E31"


class E33_LinguisticObject(E28_ConceptualObject):
    """E33: Linguistic Object — a linguistic expression"""

    class_code: str = "E33"


class E36_VisualItem(E28_ConceptualObject):
    """E36: Visual Item — a visual representation"""

    class_code: str = "E36"


class E41_Appellation(E28_ConceptualObject):
    """E41: Appellation — a name or identifier used to refer to an entity"""

    class_code: str = "E41"


class E42_Identifier(E28_ConceptualObject):
    """E42: Identifier — a unique identifier"""

    class_code: str = "E42"


class E47_SpatialCoordinates(E28_ConceptualObject):
    """E47: Spatial Coordinates — coordinates that define a location"""

    class_code: str = "E47"


class E54_Dimension(E28_ConceptualObject):
    """E54: Dimension — a measured dimension of a physical thing"""

    class_code: str = "E54"


class E55_Type(E28_ConceptualObject):
    """E55: Type — a type or category concept"""

    class_code: str = "E55"


class E88_PropositionalObject(E28_ConceptualObject):
    """E88: Propositional Object — a set of propositions"""

    class_code: str = "E88"


class E90_SymbolicObject(E28_ConceptualObject):
    """E90: Symbolic Object — a symbolic expression"""

    class_code: str = "E90"


class E97_MonetaryAmount(E28_ConceptualObject):
    """E97: Monetary Amount — a monetary value"""

    class_code: str = "E97"


class E63_BeginningOfExistence(E5_Event):
    """E63: Beginning of Existence — an event that brings an entity into existence"""

    class_code: str = "E63"


class E64_EndOfExistence(E5_Event):
    """E64: End of Existence — an event that terminates an entity's existence"""

    class_code: str = "E64"


class E6_Destruction(E5_Event):
    """E6: Destruction — an event that destroys a physical object"""

    class_code: str = "E6"


class E7_Activity(E5_Event):
    """E7: Activity — an intentional action by an actor"""

    class_code: str = "E7"


class E84_InformationCarrier(E73_InformationObject):
    """E84: Information Carrier — a physical carrier of information"""

    class_code: str = "E84"


class E21_Person(E20_BiologicalObject):
    """E21: Person — a human individual"""

    class_code: str = "E21"


class E32_AuthorityDocument(E31_Document):
    """E32: Authority Document — an authoritative reference document"""

    class_code: str = "E32"


class E34_Inscription(E33_LinguisticObject):
    """E34: Inscription — a textual inscription on a physical object"""

    class_code: str = "E34"


class E35_Title(E33_LinguisticObject):
    """E35: Title — a title or name of a work"""

    class_code: str = "E35"


class E37_Mark(E36_VisualItem):
    """E37: Mark — a mark or symbol"""

    class_code: str = "E37"


class E38_Image(E36_VisualItem):
    """E38: Image — a pictorial representation"""

    class_code: str = "E38"


class E44_PlaceAppellation(E41_Appellation):
    """E44: Place Appellation — a name used to refer to a place"""

    class_code: str = "E44"


class E49_TimeAppellation(E41_Appellation):
    """E49: Time Appellation — a name used to refer to a time"""

    class_code: str = "E49"


class E75_ConceptualObjectAppellation(E41_Appellation):
    """E75: Conceptual Object Appellation — a name for a conceptual object"""

    class_code: str = "E75"


class E76_ConceptualObjectIdentifier(E42_Identifier):
    """E76: Conceptual Object Identifier — an identifier for a conceptual object"""

    class_code: str = "E76"


class E56_Language(E55_Type):
    """E56: Language — a natural language"""

    class_code: str = "E56"


class E57_Material(E55_Type):
    """E57: Material — a physical material"""

    class_code: str = "E57"


class E58_MeasurementUnit(E55_Type):
    """E58: Measurement Unit — a unit of measurement"""

    class_code: str = "E58"


class E98_Currency(E55_Type):
    """E98: Currency — a monetary currency"""

    class_code: str = "E98"


class E99_ProductType(E55_Type):
    """E99: Product Type — a product type"""

    class_code: str = "E99"


class E89_PropositionalStatement(E88_PropositionalObject):
    """E89: Propositional Statement — a single propositional statement"""

    class_code: str = "E89"


class E91_KnowledgeObject(E90_SymbolicObject):
    """E91: Knowledge Object — structured knowledge"""

    class_code: str = "E91"


class E65_Creation(E63_BeginningOfExistence):
    """E65: Creation — the creation of a conceptual object"""

    class_code: str = "E65"


class E66_Formation(E63_BeginningOfExistence):
    """E66: Formation — the formation of a group"""

    class_code: str = "E66"


class E68_Dissolution(E64_EndOfExistence):
    """E68: Dissolution — the dissolution of a group"""

    class_code: str = "E68"


class E69_Death(E64_EndOfExistence):
    """E69: Death — the death of a person"""

    class_code: str = "E69"


class E10_TransferOfCustody(E7_Activity):
    """E10: Transfer of Custody — custody transfer of an object"""

    class_code: str = "E10"


class E11_Modification(E7_Activity):
    """E11: Modification — a physical modification of an object"""

    class_code: str = "E11"


class E12_Production(E7_Activity):
    """E12: Production — the creation of a human-made object"""

    class_code: str = "E12"


class E13_AttributeAssignment(E7_Activity):
    """E13: Attribute Assignment — the assignment of an attribute to an entity"""

    class_code: str = "E13"


class E85_Joining(E7_Activity):
    """E85: Joining — joining a group"""

    class_code: str = "E85"


class E86_Leaving(E7_Activity):
    """E86: Leaving — leaving a group"""

    class_code: str = "E86"


class E87_CurationActivity(E7_Activity):
    """E87: Curation Activity — a curation activity for a managed collection"""

    class_code: str = "E87"


class E8_Acquisition(E7_Activity):
    """E8: Acquisition — the acquisition of ownership of an object"""

    class_code: str = "E8"


class E9_Move(E7_Activity):
    """E9: Move — a physical relocation of an object"""

    class_code: str = "E9"


class E45_Address(E44_PlaceAppellation):
    """E45: Address — a postal or civic address"""

    class_code: str = "E45"


class E48_PlaceName(E44_PlaceAppellation):
    """E48: Place Name — a toponym or place name"""

    class_code: str = "E48"


class E50_Date(E49_TimeAppellation):
    """E50: Date — a calendar date expression"""

    class_code: str = "E50"


class E82_ActorAppellation(E75_ConceptualObjectAppellation):
    """E82: Actor Appellation — a name used to refer to an actor"""

    class_code: str = "E82"


class E83_TypeCreation(E65_Creation):
    """E83: Type Creation — the creation of a type concept"""

    class_code: str = "E83"


class E67_Birth(E66_Formation):
    """E67: Birth — the birth of a person"""

    class_code: str = "E67"


class E79_PartAddition(E11_Modification):
    """E79: Part Addition — the addition of a part to an object"""

    class_code: str = "E79"


class E80_PartRemoval(E11_Modification):
    """E80: Part Removal — the removal of a part from an object"""

    class_code: str = "E80"


class E81_Transformation(E11_Modification):
    """E81: Transformation — a transformation of an object into another"""

    class_code: str = "E81"


class E14_ConditionAssessment(E13_AttributeAssignment):
    """E14: Condition Assessment — an assessment of the condition of an object"""

    class_code: str = "E14"


class E15_IdentifierAssignment(E13_AttributeAssignment):
    """E15: Identifier Assignment — the assignment of an identifier to an entity"""

    class_code: str = "E15"


class E16_Measurement(E13_AttributeAssignment):
    """E16: Measurement — the measurement of a dimension"""

    class_code: str = "E16"


class E17_TypeAssignment(E13_AttributeAssignment):
    """E17: Type Assignment — the assignment of a type to an entity"""

    class_code: str = "E17"


class E96_Purchase(E8_Acquisition):
    """E96: Purchase — an acquisition by exchange of monetary value"""

    class_code: str = "E96"


class E51_ContactPoint(E45_Address):
    """E51: Contact Point — a contact point such as phone or email"""

    class_code: str = "E51"
