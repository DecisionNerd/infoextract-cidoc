#!/usr/bin/env python3
"""
Code generator for CIDOC CRM Pydantic models from the LinkML schema.

Uses LinkML SchemaView to traverse the class hierarchy defined in
cidoc_crm.yaml and emits clean Pydantic V2 model code.

Run via:  uv run python src/infoextract_cidoc/codegen/generate_models.py
Or:       make codegen
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from linkml_runtime.utils.schemaview import SchemaView


def _topological_order(sv: SchemaView) -> list[str]:
    """Return class names in topological order (parents before children)."""
    all_classes = sv.all_classes()
    in_degree: dict[str, int] = dict.fromkeys(all_classes, 0)
    children: dict[str, list[str]] = {name: [] for name in all_classes}

    for name, cls in all_classes.items():
        if cls.is_a and cls.is_a in all_classes:
            in_degree[name] += 1
            children[cls.is_a].append(name)

    queue: deque[str] = deque(
        name for name, degree in in_degree.items() if degree == 0
    )
    order: list[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in sorted(children[node]):  # sorted for determinism
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    return order


def _generate_class(sv: SchemaView, class_name: str) -> str:
    """Render a single Pydantic V2 class definition."""
    cls = sv.get_class(class_name)

    # Derive E-code: "E22_HumanMadeObject" -> "E22"
    code = class_name.split("_")[0]

    # Determine Python parent
    parent = cls.is_a if cls.is_a else "CRMEntity"

    # Own slots only — subclasses inherit via Python class hierarchy
    own_slot_names: list[str] = list(cls.slots or [])

    # Build field lines
    field_lines: list[str] = []
    for slot_name in own_slot_names:
        slot = sv.get_slot(slot_name)
        desc = (slot.description or "").replace('"', '\\"')
        field_lines.append(
            f'    {slot_name}: UUID | None = Field(None, description="{desc}")'
        )

    body = "\n".join(field_lines) if field_lines else "    pass"
    description = (cls.description or f"{code}: {class_name}").replace('"', '\\"')

    return (
        f'class {class_name}({parent}):\n'
        f'    """{description}"""\n'
        f"\n"
        f'    class_code: str = "{code}"\n'
        f"\n"
        f"{body}\n"
    )


def generate(schema_path: Path, output_path: Path) -> None:
    """Generate e_classes.py from the LinkML schema at *schema_path*."""
    sv = SchemaView(str(schema_path))
    order = _topological_order(sv)

    header = '''\
"""
Auto-generated CIDOC CRM E-class models.
Source of truth: codegen/cidoc_crm.yaml (LinkML schema)

DO NOT EDIT — regenerate with: make codegen
"""

from __future__ import annotations

from uuid import UUID

from pydantic import Field

from infoextract_cidoc.models.base import CRMEntity


'''

    classes = "\n\n".join(_generate_class(sv, name) for name in order)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(header + classes + "\n")


def main() -> None:
    """Entry point for code generation."""
    here = Path(__file__).parent
    schema = here / "cidoc_crm.yaml"
    output = here.parent / "models" / "generated" / "e_classes.py"
    generate(schema, output)
    print(f"Generated {output}")


if __name__ == "__main__":
    main()
