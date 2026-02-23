#!/usr/bin/env python3
"""
Code generator for CIDOC CRM property registry from YAML specifications.
Generates properties.py with P-registry and lookup tables.
"""

from pathlib import Path
from typing import Any

import yaml


def load_yaml_specs(specs_dir: Path) -> dict[str, Any]:
    """Load YAML specifications from the specs directory."""
    properties_file = specs_dir / "crm_properties.yaml"
    aliases_file = specs_dir / "aliases.yaml"

    with properties_file.open() as f:
        properties = yaml.safe_load(f)

    with aliases_file.open() as f:
        aliases = yaml.safe_load(f)

    return {"properties": properties, "aliases": aliases}


def generate_property_registry(properties: list[dict[str, Any]]) -> str:
    """Generate the P property registry dictionary."""
    registry_items = []

    for prop in properties:
        code = prop["code"]
        label = prop["label"]
        domain = prop["domain"]
        range_val = prop["range"]
        inverse = prop["inverse"]
        quantifier = prop["quantifier"]
        aliases = prop.get("aliases", [])
        notes = prop.get("notes", "")

        registry_item = f"""    "{code}": {{
        "label": "{label}",
        "domain": "{domain}",
        "range": "{range_val}",
        "inverse": "{inverse}",
        "quantifier": "{quantifier}",
        "aliases": {aliases},
        "notes": "{notes}"
    }}"""
        registry_items.append(registry_item)

    return "P = {\n" + ",\n".join(registry_items) + "\n}"


def generate_lookup_tables(properties: list[dict[str, Any]]) -> str:
    """Generate domain and range lookup tables."""
    domain_lookup = {}
    range_lookup = {}

    for prop in properties:
        code = prop["code"]
        domain = prop["domain"]
        range_val = prop["range"]

        if domain not in domain_lookup:
            domain_lookup[domain] = []
        domain_lookup[domain].append(code)

        if range_val not in range_lookup:
            range_lookup[range_val] = []
        range_lookup[range_val].append(code)

    # Generate domain lookup
    domain_items = []
    for domain, props in domain_lookup.items():
        domain_items.append(f'    "{domain}": {props}')
    domain_lookup_str = "DOMAIN = {\n" + ",\n".join(domain_items) + "\n}"

    # Generate range lookup
    range_items = []
    for range_val, props in range_lookup.items():
        range_items.append(f'    "{range_val}": {props}')
    range_lookup_str = "RANGE = {\n" + ",\n".join(range_items) + "\n}"

    return domain_lookup_str + "\n\n" + range_lookup_str


def generate_properties_file(specs: dict[str, Any], output_path: Path) -> None:
    """Generate the complete properties.py file."""
    properties = specs["properties"]
    specs["aliases"]

    # Generate header
    header = '''"""
Auto-generated CIDOC CRM property registry.
Generated from YAML specifications in codegen/specs/

This module provides:
- P: Dictionary of all P-properties with metadata
- DOMAIN: Lookup table from E-class to properties with that domain
- RANGE: Lookup table from E-class to properties with that range
"""

from typing import Dict, List, Any

'''

    # Generate property registry
    registry = generate_property_registry(properties)

    # Generate lookup tables
    lookups = generate_lookup_tables(properties)

    # Combine all parts
    full_content = header + registry + "\n\n" + lookups + "\n"

    # Write to file
    with output_path.open("w") as f:
        f.write(full_content)


def main():
    """Main code generation function."""
    # Get paths
    current_dir = Path(__file__).parent
    specs_dir = current_dir / "specs"
    output_path = current_dir.parent / "properties.py"

    # Load specifications
    specs = load_yaml_specs(specs_dir)

    # Generate properties file
    generate_properties_file(specs, output_path)


if __name__ == "__main__":
    main()
