"""
Shared shortcut-field → P-property mappings for CIDOC CRM entities.

Both the Cypher emitter and the NetworkX graph builder use this mapping to
expand entity shortcut fields into full CRM relationships.
"""

# Maps entity shortcut field name → P-property code
SHORTCUT_MAPPING: dict[str, str] = {
    "timespan": "P4",
    "took_place_at": "P7",
    "current_location": "P53",
    "produced_by": "P108",
    "begin_of_the_begin": "P79",
    "end_of_the_end": "P80",
}

# Maps P-property code → entity shortcut field name (inverse of SHORTCUT_MAPPING)
P_TO_SHORTCUT: dict[str, str] = {v: k for k, v in SHORTCUT_MAPPING.items()}

# Maps P-property code → entity field name for validation use
P_TO_FIELD: dict[str, str] = {
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
