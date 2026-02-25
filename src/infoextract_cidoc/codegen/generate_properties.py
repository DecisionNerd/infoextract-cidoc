#!/usr/bin/env python3
"""
Code generator for the CIDOC CRM property registry from the LinkML schema.

Reads cidoc_crm_properties.yaml and emits properties.py with the P and DOMAIN
dicts.  Replaces the old codegen/generate_registry.py.

Run via:  uv run python src/infoextract_cidoc/codegen/generate_properties.py
Or:       make codegen
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

from linkml_runtime.utils.schemaview import SchemaView

if TYPE_CHECKING:
    from linkml_runtime.linkml_model.meta import SlotDefinition


def _sort_key(code: str) -> tuple[int, int]:
    """Sort P-codes numerically, forward before inverse: P1 < P1i < P2 < P2i."""
    m = re.match(r"P(\d+)(i?)$", code)
    if not m:
        return (999999, 0)
    return (int(m.group(1)), 1 if m.group(2) else 0)


def generate(schema_path: Path, output_path: Path) -> None:
    """Generate properties.py from the LinkML properties schema."""
    sv = SchemaView(str(schema_path))
    all_slots = sv.all_slots()

    # Collect only slots that carry a crm_code annotation (skips shortcut slots
    # inherited from cidoc_crm.yaml which have no such annotation).
    crm_slots: list[tuple[str, SlotDefinition]] = []
    for slot_name, slot in all_slots.items():
        annotations = slot.annotations or {}
        if "crm_code" in annotations:
            crm_slots.append((slot_name, slot))

    # Sort by P-code numerically, forward before inverse
    crm_slots.sort(key=lambda item: _sort_key(item[1].annotations["crm_code"].value))

    # ── build P dict entries ──────────────────────────────────────────────────
    p_entries: list[str] = []
    domain_lookup: dict[str, list[str]] = {}

    for _slot_name, slot in crm_slots:
        ann = slot.annotations
        code: str = ann["crm_code"].value
        label: str = ann["crm_label"].value
        quantifier: str = ann["quantifier"].value
        notes: str = ann["notes"].value

        # Bare E-codes: "E2_TemporalEntity" → "E2"
        domain_full: str = slot.domain or ""
        range_full: str = slot.range or ""
        domain_code = domain_full.split("_")[0] if domain_full else ""
        range_code = range_full.split("_")[0] if range_full else ""

        # Resolve inverse slot → its crm_code annotation
        inverse_slot_name: str = slot.inverse or ""
        inverse_code = ""
        if inverse_slot_name and inverse_slot_name in all_slots:
            inv_slot = all_slots[inverse_slot_name]
            inv_ann = inv_slot.annotations or {}
            if "crm_code" in inv_ann:
                inverse_code = inv_ann["crm_code"].value

        aliases: list[str] = list(slot.aliases or [])

        # Escape any embedded double-quotes so the f-string literals are safe
        label_esc = label.replace('"', '\\"')
        notes_esc = notes.replace('"', '\\"')

        entry = (
            f'    "{code}": {{\n'
            f'        "label": "{label_esc}",\n'
            f'        "domain": "{domain_code}",\n'
            f'        "range": "{range_code}",\n'
            f'        "inverse": "{inverse_code}",\n'
            f'        "quantifier": "{quantifier}",\n'
            f'        "aliases": {aliases!r},\n'
            f'        "notes": "{notes_esc}",\n'
            f"    }}"
        )
        p_entries.append(entry)

        if domain_code:
            domain_lookup.setdefault(domain_code, []).append(code)

    # ── build DOMAIN dict entries ─────────────────────────────────────────────
    domain_entries: list[str] = []
    for ecode, codes in domain_lookup.items():
        domain_entries.append(f'    "{ecode}": {codes!r}')

    header = '''\
"""
Auto-generated CIDOC CRM property registry.
Source of truth: codegen/cidoc_crm_properties.yaml (LinkML schema)

DO NOT EDIT — regenerate with: make codegen

This module provides:
- P: Dictionary of all P-properties with metadata
- DOMAIN: Lookup table from E-class to properties with that domain
"""

'''

    p_dict = "P = {\n" + ",\n".join(p_entries) + "\n}\n"
    domain_dict = "DOMAIN = {\n" + ",\n".join(domain_entries) + "\n}\n"

    output_path.write_text(header + p_dict + "\n" + domain_dict)


def main() -> None:
    """Entry point for code generation."""
    here = Path(__file__).parent
    schema = here / "cidoc_crm_properties.yaml"
    output = here.parent / "properties.py"
    generate(schema, output)
    print(f"Generated {output}")


if __name__ == "__main__":
    main()
