#!/usr/bin/env python3
"""
Code generator for CIDOC CRM Pydantic models from YAML specifications.
Generates e_classes.py with all E-class models.
"""

from pathlib import Path
from typing import Any

import yaml


def load_yaml_specs(specs_dir: Path) -> dict[str, Any]:
    """Load YAML specifications from the specs directory."""
    classes_file = specs_dir / "crm_classes.yaml"
    properties_file = specs_dir / "crm_properties.yaml"
    aliases_file = specs_dir / "aliases.yaml"

    with classes_file.open() as f:
        classes = yaml.safe_load(f)

    with properties_file.open() as f:
        properties = yaml.safe_load(f)

    with aliases_file.open() as f:
        aliases = yaml.safe_load(f)

    return {"classes": classes, "properties": properties, "aliases": aliases}


def generate_class_model(
    class_spec: dict[str, Any], classes: list[dict[str, Any]]
) -> str:
    """Generate Pydantic model code for a single E-class."""
    code = class_spec["code"]
    label = class_spec["label"]
    abstract = class_spec.get("abstract", False)
    parents = class_spec.get("parents", [])
    canonical_fields = class_spec.get("canonical_fields", [])
    shortcuts = class_spec.get("shortcuts", [])

    # Convert label to Python class name
    class_name = f"E{code}_{label.replace(' ', '').replace('-', '')}"

    # Determine parent class
    if parents:
        # Find the parent class spec to get its label
        parent_code = parents[0]
        parent_spec = next((c for c in classes if c["code"] == parent_code), None)
        if parent_spec:
            parent_label = parent_spec["label"]
            parent_class = (
                f"E{parent_code}_{parent_label.replace(' ', '').replace('-', '')}"
            )
        else:
            parent_class = "CRMEntity"
    else:
        parent_class = "CRMEntity"

    # Generate shortcut fields
    shortcut_fields = []
    for shortcut in shortcuts:
        shortcut["property"]
        alias_field = shortcut["alias_field"]
        field_type = shortcut.get("field_type", "UUID")
        shortcut_fields.append(f"    {alias_field}: Optional[{field_type}] = None")

    shortcut_fields_str = "\n".join(shortcut_fields) if shortcut_fields else "    pass"

    # Generate docstring
    docstring = f'    """CIDOC CRM {code}: {label}'
    if abstract:
        docstring += " (Abstract)"
    docstring += '"""'

    return f"""class {class_name}({parent_class}):
{docstring}
    class_code: str = "{code}"

{shortcut_fields_str}

    class Config:
        json_schema_extra = {{
            "description": "{label}",
            "canonical_fields": {canonical_fields}
        }}
"""


def generate_models_file(specs: dict[str, Any], output_path: Path) -> None:
    """Generate the complete e_classes.py file."""
    classes = specs["classes"]

    # Generate imports and base class
    header = '''"""
Auto-generated CIDOC CRM E-class models.
Generated from YAML specifications in codegen/specs/
"""

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from ..base import CRMEntity


'''

    # Generate all class models
    class_models = []
    for class_spec in classes:
        model_code = generate_class_model(class_spec, classes)
        class_models.append(model_code)

    # Combine header and models
    full_content = header + "\n\n".join(class_models)

    # Write to file
    with output_path.open("w") as f:
        f.write(full_content)


def main():
    """Main code generation function."""
    # Get paths
    current_dir = Path(__file__).parent
    specs_dir = current_dir / "specs"
    output_path = current_dir.parent / "models" / "generated" / "e_classes.py"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load specifications
    specs = load_yaml_specs(specs_dir)

    # Generate models
    generate_models_file(specs, output_path)


if __name__ == "__main__":
    main()
