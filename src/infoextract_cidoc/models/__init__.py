"""CRM models package for infoextract-cidoc."""

from .base import (
    CRMEntity,
    CRMRelation,
    CRMValidationError,
    CRMValidationWarning,
)
from .generated.e_classes import (
    E5_Event,
    E7_Activity,
    E8_Acquisition,
    E12_Production,
    E21_Person,
    E22_HumanMadeObject,
    E35_Title,
    E42_Identifier,
    E52_TimeSpan,
    E53_Place,
    E74_Group,
)

__all__ = [
    "CRMEntity",
    "CRMRelation",
    "CRMValidationError",
    "CRMValidationWarning",
    "E5_Event",
    "E7_Activity",
    "E8_Acquisition",
    "E12_Production",
    "E21_Person",
    "E22_HumanMadeObject",
    "E35_Title",
    "E42_Identifier",
    "E52_TimeSpan",
    "E53_Place",
    "E74_Group",
]
