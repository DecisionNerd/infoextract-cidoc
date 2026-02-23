"""
Unit tests for CRM validators.
"""

from uuid import uuid4

import pytest

from ...models.generated.e_classes import (
    EE12_Production,
    EE22_HumanMadeObject,
)
from ...validators.quantifiers import (
    ValidationSeverity,
    enforce_quantifier,
    validate_entity_quantifiers,
)
from ...validators.typing_rules import (
    validate_batch_typing,
    validate_domain_range_alignment,
)


class TestQuantifierValidation:
    """Test quantifier validation functionality."""

    def test_enforce_quantifier_valid(self):
        """Test quantifier enforcement with valid values."""
        entity = EE22_HumanMadeObject(id=uuid4(), class_code="E22")

        # P108 has quantifier "0..1" - should allow 0 or 1 values
        enforce_quantifier(entity, "P108", [], ValidationSeverity.WARN)
        enforce_quantifier(entity, "P108", [uuid4()], ValidationSeverity.WARN)

    def test_enforce_quantifier_too_many(self):
        """Test quantifier enforcement with too many values."""
        entity = EE22_HumanMadeObject(id=uuid4(), class_code="E22")

        # P108 has quantifier "0..1" - should not allow 2 values
        with pytest.raises(Exception):  # Should raise CRMValidationError
            enforce_quantifier(
                entity, "P108", [uuid4(), uuid4()], ValidationSeverity.RAISE
            )

    def test_enforce_quantifier_too_few(self):
        """Test quantifier enforcement with too few values."""
        entity = EE12_Production(id=uuid4(), class_code="E12")

        # P108i has quantifier "0..*" - should allow 0 values
        enforce_quantifier(entity, "P108i", [], ValidationSeverity.WARN)

    def test_validate_entity_quantifiers(self):
        """Test entity quantifier validation."""
        entity = EE22_HumanMadeObject(
            id=uuid4(),
            class_code="E22",
            produced_by=uuid4(),  # This should be valid
        )

        messages = validate_entity_quantifiers(entity, ValidationSeverity.WARN)
        # Should not have validation errors for a valid entity
        assert len(messages) == 0


class TestTypingValidation:
    """Test typing validation functionality."""

    def test_validate_domain_range_alignment_valid(self):
        """Test domain/range alignment with valid entities."""
        source = EE22_HumanMadeObject(id=uuid4(), class_code="E22")
        target = EE12_Production(id=uuid4(), class_code="E12")

        # P108: E22 -> E12 should be valid
        validate_domain_range_alignment(source, target, "P108", ValidationSeverity.WARN)

    def test_validate_domain_range_alignment_invalid(self):
        """Test domain/range alignment with invalid entities."""
        source = EE22_HumanMadeObject(id=uuid4(), class_code="E22")
        target = EE22_HumanMadeObject(id=uuid4(), class_code="E22")

        # P108: E22 -> E12 should be invalid with E22 target
        with pytest.raises(Exception):  # Should raise CRMValidationError
            validate_domain_range_alignment(
                source, target, "P108", ValidationSeverity.RAISE
            )

    def test_validate_batch_typing(self):
        """Test batch typing validation."""
        entities = [
            EE22_HumanMadeObject(id=uuid4(), class_code="E22"),
            EE12_Production(id=uuid4(), class_code="E12"),
        ]

        results = validate_batch_typing(entities, ValidationSeverity.WARN)
        # Should not have validation errors for valid entities
        assert len(results) == 0


class TestValidationSeverity:
    """Test validation severity handling."""

    def test_warn_severity(self):
        """Test that WARN severity issues warnings but doesn't raise."""
        entity = EE22_HumanMadeObject(id="obj_001", class_code="E22")

        # This should issue a warning but not raise an exception
        enforce_quantifier(
            entity, "P108", ["prod_001", "prod_002"], ValidationSeverity.WARN
        )

    def test_raise_severity(self):
        """Test that RAISE severity raises exceptions."""
        entity = EE22_HumanMadeObject(id="obj_001", class_code="E22")

        # This should raise an exception
        with pytest.raises(Exception):
            enforce_quantifier(
                entity, "P108", ["prod_001", "prod_002"], ValidationSeverity.RAISE
            )

    def test_ignore_severity(self):
        """Test that IGNORE severity doesn't validate."""
        entity = EE22_HumanMadeObject(id="obj_001", class_code="E22")

        # This should not raise an exception or issue warnings
        enforce_quantifier(
            entity, "P108", ["prod_001", "prod_002"], ValidationSeverity.IGNORE
        )
