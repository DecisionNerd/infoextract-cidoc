"""CRM mapping layer: ExtractedEntity/ExtractedRelationship -> CRMEntity/CRMRelation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from infoextract_cidoc.models.base import CRMEntity, CRMRelation
from infoextract_cidoc.models.generated.e_classes import (
    E1_CRMEntity,
    E2_TemporalEntity,
    E3_ConditionState,
    E4_Period,
    E5_Event,
    E6_Destruction,
    E7_Activity,
    E8_Acquisition,
    E9_Move,
    E10_TransferOfCustody,
    E11_Modification,
    E12_Production,
    E13_AttributeAssignment,
    E14_ConditionAssessment,
    E15_IdentifierAssignment,
    E16_Measurement,
    E17_TypeAssignment,
    E18_PhysicalThing,
    E19_PhysicalObject,
    E20_BiologicalObject,
    E21_Person,
    E22_HumanMadeObject,
    E23_ConceptualObject,
    E24_PhysicalManMadeThing,
    E25_ManMadeFeature,
    E26_PhysicalFeature,
    E27_Site,
    E28_ConceptualObject,
    E29_DesignOrProcedure,
    E30_Right,
    E31_Document,
    E32_AuthorityDocument,
    E33_LinguisticObject,
    E34_Inscription,
    E35_Title,
    E36_VisualItem,
    E37_Mark,
    E38_Image,
    E39_Actor,
    E40_LegalBody,
    E41_Appellation,
    E42_Identifier,
    E43_Place,
    E44_PlaceAppellation,
    E45_Address,
    E46_Section,
    E47_SpatialCoordinates,
    E48_PlaceName,
    E49_TimeAppellation,
    E50_Date,
    E51_ContactPoint,
    E52_TimeSpan,
    E53_Place,
    E54_Dimension,
    E55_Type,
    E56_Language,
    E57_Material,
    E58_MeasurementUnit,
    E59_PrimitiveValue,
    E60_Number,
    E61_TimePrimitive,
    E62_String,
    E63_BeginningOfExistence,
    E64_EndOfExistence,
    E65_Creation,
    E66_Formation,
    E67_Birth,
    E68_Dissolution,
    E69_Death,
    E70_Thing,
    E71_HumanMadeThing,
    E72_LegalObject,
    E73_InformationObject,
    E74_Group,
    E75_ConceptualObjectAppellation,
    E76_ConceptualObjectIdentifier,
    E77_PersistentItem,
    E78_CuratedHolding,
    E79_PartAddition,
    E80_PartRemoval,
    E81_Transformation,
    E82_ActorAppellation,
    E83_TypeCreation,
    E84_InformationCarrier,
    E85_Joining,
    E86_Leaving,
    E87_CurationActivity,
    E88_PropositionalObject,
    E89_PropositionalStatement,
    E90_SymbolicObject,
    E91_KnowledgeObject,
    E92_SpacetimeVolume,
    E93_Presence,
    E94_Space,
    E95_SpacetimePrimitive,
    E96_Purchase,
    E97_MonetaryAmount,
    E98_Currency,
    E99_ProductType,
)

if TYPE_CHECKING:
    from infoextract_cidoc.extraction.models import (
        ExtractedEntity,
        ExtractionResult,
    )

# Dispatch table: E-code string → generated CRM subclass
_CLASS_CODE_MAP: dict[str, type[CRMEntity]] = {
    "E1": E1_CRMEntity,
    "E2": E2_TemporalEntity,
    "E3": E3_ConditionState,
    "E4": E4_Period,
    "E5": E5_Event,
    "E6": E6_Destruction,
    "E7": E7_Activity,
    "E8": E8_Acquisition,
    "E9": E9_Move,
    "E10": E10_TransferOfCustody,
    "E11": E11_Modification,
    "E12": E12_Production,
    "E13": E13_AttributeAssignment,
    "E14": E14_ConditionAssessment,
    "E15": E15_IdentifierAssignment,
    "E16": E16_Measurement,
    "E17": E17_TypeAssignment,
    "E18": E18_PhysicalThing,
    "E19": E19_PhysicalObject,
    "E20": E20_BiologicalObject,
    "E21": E21_Person,
    "E22": E22_HumanMadeObject,
    "E23": E23_ConceptualObject,
    "E24": E24_PhysicalManMadeThing,
    "E25": E25_ManMadeFeature,
    "E26": E26_PhysicalFeature,
    "E27": E27_Site,
    "E28": E28_ConceptualObject,
    "E29": E29_DesignOrProcedure,
    "E30": E30_Right,
    "E31": E31_Document,
    "E32": E32_AuthorityDocument,
    "E33": E33_LinguisticObject,
    "E34": E34_Inscription,
    "E35": E35_Title,
    "E36": E36_VisualItem,
    "E37": E37_Mark,
    "E38": E38_Image,
    "E39": E39_Actor,
    "E40": E40_LegalBody,
    "E41": E41_Appellation,
    "E42": E42_Identifier,
    "E43": E43_Place,
    "E44": E44_PlaceAppellation,
    "E45": E45_Address,
    "E46": E46_Section,
    "E47": E47_SpatialCoordinates,
    "E48": E48_PlaceName,
    "E49": E49_TimeAppellation,
    "E50": E50_Date,
    "E51": E51_ContactPoint,
    "E52": E52_TimeSpan,
    "E53": E53_Place,
    "E54": E54_Dimension,
    "E55": E55_Type,
    "E56": E56_Language,
    "E57": E57_Material,
    "E58": E58_MeasurementUnit,
    "E59": E59_PrimitiveValue,
    "E60": E60_Number,
    "E61": E61_TimePrimitive,
    "E62": E62_String,
    "E63": E63_BeginningOfExistence,
    "E64": E64_EndOfExistence,
    "E65": E65_Creation,
    "E66": E66_Formation,
    "E67": E67_Birth,
    "E68": E68_Dissolution,
    "E69": E69_Death,
    "E70": E70_Thing,
    "E71": E71_HumanMadeThing,
    "E72": E72_LegalObject,
    "E73": E73_InformationObject,
    "E74": E74_Group,
    "E75": E75_ConceptualObjectAppellation,
    "E76": E76_ConceptualObjectIdentifier,
    "E77": E77_PersistentItem,
    "E78": E78_CuratedHolding,
    "E79": E79_PartAddition,
    "E80": E80_PartRemoval,
    "E81": E81_Transformation,
    "E82": E82_ActorAppellation,
    "E83": E83_TypeCreation,
    "E84": E84_InformationCarrier,
    "E85": E85_Joining,
    "E86": E86_Leaving,
    "E87": E87_CurationActivity,
    "E88": E88_PropositionalObject,
    "E89": E89_PropositionalStatement,
    "E90": E90_SymbolicObject,
    "E91": E91_KnowledgeObject,
    "E92": E92_SpacetimeVolume,
    "E93": E93_Presence,
    "E94": E94_Space,
    "E95": E95_SpacetimePrimitive,
    "E96": E96_Purchase,
    "E97": E97_MonetaryAmount,
    "E98": E98_Currency,
    "E99": E99_ProductType,
}

# Map P-property codes to entity shortcut field names
_SHORTCUT_P_TO_FIELD: dict[str, str] = {
    "P4": "timespan",
    "P7": "took_place_at",
    "P53": "current_location",
    "P108": "produced_by",
    "P79": "begin_of_the_begin",
    "P80": "end_of_the_end",
}


def _entity_to_crm(
    entity: ExtractedEntity, shortcut_kwargs: dict[str, Any]
) -> CRMEntity:
    """Map an ExtractedEntity to a typed CRM subclass, populating shortcut fields."""
    cls = _CLASS_CODE_MAP.get(entity.class_code, CRMEntity)
    # Only pass shortcut fields that the target class actually defines
    valid_shortcuts = {k: v for k, v in shortcut_kwargs.items() if k in cls.model_fields}
    return cls(
        id=entity.id,
        class_code=entity.class_code,
        label=entity.label,
        notes=entity.description,
        source_text=entity.source_text,
        type=[entity.class_code],
        **valid_shortcuts,
    )


def map_to_crm_entities(
    result: ExtractionResult,
) -> tuple[list[CRMEntity], list[CRMRelation]]:
    """Map an ExtractionResult to CRM entities and relations.

    Args:
        result: Resolved ExtractionResult from resolve_extraction().

    Returns:
        Tuple of (crm_entities, crm_relations).
    """
    # Build a lookup from source entity ID to shortcut field kwargs
    shortcut_lookup: dict[str, dict[str, Any]] = {}
    for rel in result.relationships:
        field = _SHORTCUT_P_TO_FIELD.get(rel.property_code)
        if field:
            src = str(rel.source_id)
            if src not in shortcut_lookup:
                shortcut_lookup[src] = {}
            shortcut_lookup[src][field] = rel.target_id

    crm_entities = [
        _entity_to_crm(e, shortcut_lookup.get(str(e.id), {}))
        for e in result.entities
    ]

    crm_relations = [
        CRMRelation(
            src=rel.source_id,
            type=rel.property_code,
            tgt=rel.target_id,
            props=None,
            source_text=rel.source_text,
        )
        for rel in result.relationships
    ]

    return crm_entities, crm_relations
