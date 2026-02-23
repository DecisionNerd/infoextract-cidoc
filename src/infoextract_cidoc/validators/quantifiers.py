"""
Quantifier validation utilities for CIDOC CRM.
Enforces cardinality rules with configurable severity.
"""

import logging
from enum import Enum
from typing import Any

from infoextract_cidoc.models.base import CRMEntity, CRMValidationError, CRMValidationWarning
from infoextract_cidoc.properties import P

logger = logging.getLogger(__name__)


class ValidationSeverity(str, Enum):
    """Validation severity levels."""

    WARN = "warn"
    RAISE = "raise"
    IGNORE = "ignore"


def enforce_quantifier(
    entity: CRMEntity,
    p_code: str,
    values: list[Any],
    severity: ValidationSeverity = ValidationSeverity.WARN,
) -> None:
    """
    Enforce quantifier rules for a property on an entity.

    Args:
        entity: The CRM entity
        p_code: P-property code (e.g., "P108")
        values: List of values for the property
        severity: How to handle violations (warn, raise, ignore)

    Raises:
        CRMValidationError: If severity is RAISE and quantifier is violated
        CRMValidationWarning: If severity is WARN and quantifier is violated
    """
    if severity == ValidationSeverity.IGNORE:
        return

    if p_code not in P:
        logger.warning("Unknown property code: %s", p_code)
        return

    quantifier = P[p_code]["quantifier"]
    domain = P[p_code]["domain"]

    # Check if entity class matches domain
    if entity.class_code != domain:
        logger.info(
            "Entity %s does not match domain %s for property %s",
            entity.class_code,
            domain,
            p_code,
        )
        return

    # Parse quantifier
    min_count, max_count = _parse_quantifier(quantifier)

    # Check cardinality
    actual_count = len(values) if values else 0

    if actual_count < min_count:
        message = f"Property {p_code} requires at least {min_count} values, got {actual_count}"
        _handle_violation(message, severity, entity)

    if max_count is not None and actual_count > max_count:
        message = (
            f"Property {p_code} allows at most {max_count} values, got {actual_count}"
        )
        _handle_violation(message, severity, entity)


def validate_entity_quantifiers(
    entity: CRMEntity, severity: ValidationSeverity = ValidationSeverity.WARN
) -> list[str]:
    """
    Validate all quantifier rules for an entity.

    Args:
        entity: The CRM entity to validate
        severity: How to handle violations

    Returns:
        List of validation messages
    """
    messages = []

    # Get all properties that apply to this entity's class
    from infoextract_cidoc.properties import DOMAIN

    applicable_properties = DOMAIN.get(entity.class_code, [])

    for p_code in applicable_properties:
        try:
            # Get values for this property from the entity
            values = _get_property_values(entity, p_code)

            # Validate quantifier
            enforce_quantifier(entity, p_code, values, severity)

        except (CRMValidationError, CRMValidationWarning) as e:
            messages.append(str(e))
        except Exception as e:
            logger.exception("Error validating property %s", p_code)
            messages.append(f"Error validating property {p_code}: {e}")

    return messages


def _parse_quantifier(quantifier: str) -> tuple[int, int | None]:
    """
    Parse quantifier string into min/max counts.

    Args:
        quantifier: Quantifier string (e.g., "0..1", "1..*", "1..1")

    Returns:
        Tuple of (min_count, max_count) where max_count can be None for "*"
    """
    if ".." not in quantifier:
        msg = f"Invalid quantifier format: {quantifier}"
        raise ValueError(msg)

    min_part, max_part = quantifier.split("..")

    min_count = int(min_part)

    max_count = None if max_part == "*" else int(max_part)

    return min_count, max_count


def _handle_violation(
    message: str,
    severity: ValidationSeverity,
    entity: CRMEntity,
) -> None:
    """
    Handle a quantifier violation based on severity.

    Args:
        message: Violation message
        severity: How to handle the violation
        entity: The entity that violated the rule
        p_code: The property code that was violated
    """
    full_message = f"{message} (Entity: {entity.id}, Class: {entity.class_code})"

    if severity == ValidationSeverity.RAISE:
        raise CRMValidationError(full_message)
    if severity == ValidationSeverity.WARN:
        logger.warning(full_message)
        # Also issue a warning that can be caught
        import warnings

        warnings.warn(full_message, CRMValidationWarning, stacklevel=2)
    # IGNORE is handled in the calling function


def _get_property_values(entity: CRMEntity, p_code: str) -> list[Any]:
    """
    Get values for a property from an entity.

    Args:
        entity: The CRM entity
        p_code: P-property code

    Returns:
        List of values for the property
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
            return value
        return [value]

    return []


def validate_batch_quantifiers(
    entities: list[CRMEntity], severity: ValidationSeverity = ValidationSeverity.WARN
) -> dict[str, list[str]]:
    """
    Validate quantifiers for a batch of entities.

    Args:
        entities: List of CRM entities to validate
        severity: How to handle violations

    Returns:
        Dictionary mapping entity IDs to validation messages
    """
    results = {}

    for entity in entities:
        messages = validate_entity_quantifiers(entity, severity)
        if messages:
            results[entity.id] = messages

    return results


def get_quantifier_summary(entities: list[CRMEntity]) -> dict[str, Any]:
    """
    Get a summary of quantifier validation results.

    Args:
        entities: List of CRM entities to analyze

    Returns:
        Summary dictionary with validation statistics
    """
    total_entities = len(entities)
    validation_results = validate_batch_quantifiers(entities, ValidationSeverity.WARN)

    entities_with_issues = len(validation_results)
    total_issues = sum(len(messages) for messages in validation_results.values())

    return {
        "total_entities": total_entities,
        "entities_with_issues": entities_with_issues,
        "total_issues": total_issues,
        "validation_results": validation_results,
    }
