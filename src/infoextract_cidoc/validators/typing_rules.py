"""
Domain/range typing validation for CIDOC CRM.
Validates that relationships align with property domain/range constraints.
"""

import logging
from typing import Any

from infoextract_cidoc.models.base import (
    CRMEntity,
    CRMValidationError,
    CRMValidationWarning,
)
from infoextract_cidoc.properties import DOMAIN, P

from .quantifiers import ValidationSeverity

logger = logging.getLogger(__name__)


def validate_domain_range_alignment(
    source_entity: CRMEntity,
    target_entity: CRMEntity,
    p_code: str,
    severity: ValidationSeverity = ValidationSeverity.WARN,
) -> None:
    """
    Validate that a relationship aligns with domain/range constraints.

    Args:
        source_entity: Source entity of the relationship
        target_entity: Target entity of the relationship
        p_code: P-property code for the relationship
        severity: How to handle violations

    Raises:
        CRMValidationError: If severity is RAISE and alignment is violated
        CRMValidationWarning: If severity is WARN and alignment is violated
    """
    if severity == ValidationSeverity.IGNORE:
        return

    if p_code not in P:
        logger.warning("Unknown property code: %s", p_code)
        return

    property_info = P[p_code]
    expected_domain = str(property_info["domain"])
    expected_range = str(property_info["range"])

    # Check domain alignment
    if not _is_class_compatible(source_entity.class_code, expected_domain):
        message = f"Entity {source_entity.id} (class {source_entity.class_code}) does not match domain {expected_domain} for property {p_code}"
        _handle_violation(message, severity, source_entity, target_entity, p_code)

    # Check range alignment
    if not _is_class_compatible(target_entity.class_code, expected_range):
        message = f"Entity {target_entity.id} (class {target_entity.class_code}) does not match range {expected_range} for property {p_code}"
        _handle_violation(message, severity, source_entity, target_entity, p_code)


def validate_entity_typing(
    entity: CRMEntity,
    entity_lookup: dict[str, CRMEntity],
    severity: ValidationSeverity = ValidationSeverity.WARN,
) -> list[str]:
    """
    Validate typing rules for an entity against a lookup table.

    Args:
        entity: The CRM entity to validate
        entity_lookup: Dictionary mapping entity IDs to entities
        severity: How to handle violations

    Returns:
        List of validation messages
    """
    messages = []

    # Get all properties that apply to this entity's class
    applicable_properties = DOMAIN.get(entity.class_code, [])

    for p_code in applicable_properties:
        try:
            # Get target entity IDs for this property
            target_ids = _get_property_target_ids(entity, p_code)

            for target_id in target_ids:
                if target_id in entity_lookup:
                    target_entity = entity_lookup[target_id]
                    validate_domain_range_alignment(
                        entity, target_entity, p_code, severity
                    )
                else:
                    logger.info(
                        "Target entity %s not found in lookup for property %s",
                        target_id,
                        p_code,
                    )

        except (CRMValidationError, CRMValidationWarning) as e:
            messages.append(str(e))
        except Exception as e:
            logger.exception("Error validating typing for property %s", p_code)
            messages.append(f"Error validating typing for property {p_code}: {e}")

    return messages


def validate_batch_typing(
    entities: list[CRMEntity], severity: ValidationSeverity = ValidationSeverity.WARN
) -> dict[str, list[str]]:
    """
    Validate typing rules for a batch of entities.

    Args:
        entities: List of CRM entities to validate
        severity: How to handle violations

    Returns:
        Dictionary mapping entity IDs to validation messages
    """
    # Create entity lookup
    entity_lookup = {str(entity.id): entity for entity in entities}

    results = {}

    for entity in entities:
        messages = validate_entity_typing(entity, entity_lookup, severity)
        if messages:
            results[str(entity.id)] = messages

    return results


def _is_class_compatible(entity_class: str, expected_class: str) -> bool:
    """
    Check if an entity class is compatible with an expected class.

    Args:
        entity_class: The entity's class code
        expected_class: The expected class code

    Returns:
        True if compatible, False otherwise
    """
    # Direct match
    if entity_class == expected_class:
        return True

    # Check inheritance hierarchy
    # This is a simplified version - in practice, you'd want to load
    # the full inheritance hierarchy from the YAML specs
    inheritance_map = {
        "E2": ["E1"],
        "E3": ["E2", "E1"],
        "E4": ["E2", "E1"],
        "E5": ["E2", "E1"],
        "E6": ["E5", "E2", "E1"],
        "E7": ["E5", "E2", "E1"],
        "E8": ["E7", "E5", "E2", "E1"],
        "E9": ["E7", "E5", "E2", "E1"],
        "E10": ["E7", "E5", "E2", "E1"],
        "E11": ["E7", "E5", "E2", "E1"],
        "E12": ["E7", "E5", "E2", "E1"],
        "E13": ["E7", "E5", "E2", "E1"],
        "E14": ["E13", "E7", "E5", "E2", "E1"],
        "E15": ["E13", "E7", "E5", "E2", "E1"],
        "E16": ["E13", "E7", "E5", "E2", "E1"],
        "E17": ["E13", "E7", "E5", "E2", "E1"],
        "E18": ["E1"],
        "E19": ["E18", "E1"],
        "E20": ["E19", "E18", "E1"],
        "E21": ["E20", "E19", "E18", "E1"],
        "E22": ["E19", "E18", "E1"],
        "E23": ["E1"],
        "E24": ["E18", "E1"],
        "E25": ["E24", "E18", "E1"],
        "E26": ["E18", "E1"],
        "E27": ["E26", "E18", "E1"],
        "E28": ["E23", "E1"],
        "E29": ["E28", "E23", "E1"],
        "E30": ["E28", "E23", "E1"],
        "E31": ["E28", "E23", "E1"],
        "E32": ["E31", "E28", "E23", "E1"],
        "E33": ["E28", "E23", "E1"],
        "E34": ["E33", "E28", "E23", "E1"],
        "E35": ["E33", "E28", "E23", "E1"],
        "E36": ["E28", "E23", "E1"],
        "E37": ["E36", "E28", "E23", "E1"],
        "E38": ["E36", "E28", "E23", "E1"],
        "E39": ["E1"],
        "E40": ["E39", "E1"],
        "E41": ["E28", "E23", "E1"],
        "E42": ["E28", "E23", "E1"],
        "E43": ["E1"],
        "E44": ["E41", "E28", "E23", "E1"],
        "E45": ["E44", "E41", "E28", "E23", "E1"],
        "E46": ["E43", "E1"],
        "E47": ["E28", "E23", "E1"],
        "E48": ["E44", "E41", "E28", "E23", "E1"],
        "E49": ["E41", "E28", "E23", "E1"],
        "E50": ["E49", "E41", "E28", "E23", "E1"],
        "E51": ["E45", "E44", "E41", "E28", "E23", "E1"],
        "E52": ["E1"],
        "E53": ["E43", "E1"],
        "E54": ["E28", "E23", "E1"],
        "E55": ["E28", "E23", "E1"],
        "E56": ["E55", "E28", "E23", "E1"],
        "E57": ["E55", "E28", "E23", "E1"],
        "E58": ["E55", "E28", "E23", "E1"],
        "E59": ["E1"],
        "E60": ["E59", "E1"],
        "E61": ["E59", "E1"],
        "E62": ["E59", "E1"],
        "E63": ["E5", "E2", "E1"],
        "E64": ["E5", "E2", "E1"],
        "E65": ["E63", "E5", "E2", "E1"],
        "E66": ["E63", "E5", "E2", "E1"],
        "E67": ["E66", "E63", "E5", "E2", "E1"],
        "E68": ["E64", "E5", "E2", "E1"],
        "E69": ["E64", "E5", "E2", "E1"],
        "E70": ["E1"],
        "E71": ["E70", "E1"],
        "E72": ["E70", "E1"],
        "E73": ["E70", "E1"],
        "E74": ["E39", "E1"],
        "E75": ["E41", "E28", "E23", "E1"],
        "E76": ["E42", "E28", "E23", "E1"],
        "E77": ["E1"],
        "E78": ["E77", "E1"],
        "E79": ["E11", "E7", "E5", "E2", "E1"],
        "E80": ["E11", "E7", "E5", "E2", "E1"],
        "E81": ["E11", "E7", "E5", "E2", "E1"],
        "E82": ["E75", "E41", "E28", "E23", "E1"],
        "E83": ["E65", "E63", "E5", "E2", "E1"],
        "E84": ["E73", "E70", "E1"],
        "E85": ["E7", "E5", "E2", "E1"],
        "E86": ["E7", "E5", "E2", "E1"],
        "E87": ["E7", "E5", "E2", "E1"],
        "E88": ["E28", "E23", "E1"],
        "E89": ["E88", "E28", "E23", "E1"],
        "E90": ["E28", "E23", "E1"],
        "E91": ["E90", "E28", "E23", "E1"],
        "E92": ["E1"],
        "E93": ["E92", "E1"],
        "E94": ["E92", "E1"],
        "E95": ["E59", "E1"],
        "E96": ["E92", "E1"],
        "E97": ["E28", "E23", "E1"],
        "E98": ["E55", "E28", "E23", "E1"],
        "E99": ["E55", "E28", "E23", "E1"],
    }

    # Check if expected_class is in the inheritance chain
    inheritance_chain = inheritance_map.get(entity_class, [])
    return expected_class in inheritance_chain


def _get_property_target_ids(entity: CRMEntity, p_code: str) -> list[str]:
    """
    Get target entity IDs for a property from an entity.

    Args:
        entity: The CRM entity
        p_code: P-property code

    Returns:
        List of target entity IDs
    """
    # Map P-codes to entity fields
    p_to_field = {
        "P1": "identifiers",
        "P2": "type",
        "P3": "notes",
        "P4": "timespan",
        "P7": "took_place_at",
        "P11": "participants",
        "P53": "current_location",
        "P79": "begin_of_the_begin",
        "P80": "end_of_the_end",
        "P108": "produced_by",
    }

    field_name = p_to_field.get(p_code)
    if not field_name:
        return []

    if hasattr(entity, field_name):
        value = getattr(entity, field_name)
        if value is None:
            return []
        if isinstance(value, list):
            return [str(v) for v in value]
        return [str(value)]

    return []


def _handle_violation(
    message: str,
    severity: ValidationSeverity,
    source_entity: CRMEntity,
    target_entity: CRMEntity,
    p_code: str,
) -> None:
    """
    Handle a typing violation based on severity.

    Args:
        message: Violation message
        severity: How to handle the violation
        source_entity: Source entity of the relationship
        target_entity: Target entity of the relationship
        p_code: The property code that was violated
    """
    full_message = f"{message} (Property: {p_code}, Source: {source_entity.id}, Target: {target_entity.id})"

    if severity == ValidationSeverity.RAISE:
        raise CRMValidationError(full_message)
    if severity == ValidationSeverity.WARN:
        logger.warning(full_message)
        # Also issue a warning that can be caught
        import warnings

        warnings.warn(full_message, CRMValidationWarning, stacklevel=2)
    # IGNORE is handled in the calling function


def get_typing_summary(entities: list[CRMEntity]) -> dict[str, Any]:
    """
    Get a summary of typing validation results.

    Args:
        entities: List of CRM entities to analyze

    Returns:
        Summary dictionary with validation statistics
    """
    total_entities = len(entities)
    validation_results = validate_batch_typing(entities, ValidationSeverity.WARN)

    entities_with_issues = len(validation_results)
    total_issues = sum(len(messages) for messages in validation_results.values())

    return {
        "total_entities": total_entities,
        "entities_with_issues": entities_with_issues,
        "total_issues": total_issues,
        "validation_results": validation_results,
    }
