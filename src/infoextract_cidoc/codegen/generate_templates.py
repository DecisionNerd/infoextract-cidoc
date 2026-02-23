#!/usr/bin/env python3
"""
Code generator for Markdown and Cypher templates from YAML specifications.
Generates template stubs for custom formatting beyond defaults.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any


def load_yaml_specs(specs_dir: Path) -> Dict[str, Any]:
    """Load YAML specifications from the specs directory."""
    classes_file = specs_dir / "crm_classes.yaml"
    properties_file = specs_dir / "crm_properties.yaml"
    aliases_file = specs_dir / "aliases.yaml"
    
    with open(classes_file, 'r') as f:
        classes = yaml.safe_load(f)
    
    with open(properties_file, 'r') as f:
        properties = yaml.safe_load(f)
    
    with open(aliases_file, 'r') as f:
        aliases = yaml.safe_load(f)
    
    return {
        "classes": classes,
        "properties": properties,
        "aliases": aliases
    }


def generate_markdown_template(class_spec: Dict[str, Any], aliases: Dict[str, Any]) -> str:
    """Generate Markdown template for a class."""
    code = class_spec["code"]
    label = class_spec["label"]
    canonical_fields = class_spec.get("canonical_fields", [])
    
    # Get friendly class name
    class_name = aliases.get("classes", {}).get(code, label)
    
    template = f"""# {class_name} Template

## Header
### {code} · {class_name} — {{{{ label or id }}}} ({{{{ id }}}})

## Body
{% for field in canonical_fields %}
{% if field in entity %}
- **{field.replace('_', ' ').title()}**: {{{{ entity[field] }}}}
{% endif %}
{% endfor %}

## Notes
{% if entity.notes %}
{entity.notes}
{% endif %}

## Relationships
{% for rel in relationships %}
- **{rel.type}**: {rel.tgt}
{% endfor %}
"""
    
    return template


def generate_cypher_template(class_spec: Dict[str, Any]) -> str:
    """Generate Cypher template for a class."""
    code = class_spec["code"]
    label = class_spec["label"]
    
    template = f"""-- Cypher template for {code}: {label}

-- Node creation
MERGE (n:CRM:{code} {{id: $id}})
SET n.label = $label,
    n.class_code = "{code}",
    n.notes = $notes,
    n.type = $type

-- Relationship creation
{% for rel in relationships %}
MATCH (src:CRM {{id: $src_id}})
MATCH (tgt:CRM {{id: $tgt_id}})
MERGE (src)-[:`{rel.type}`]->(tgt)
{% endfor %}

-- Constraints
CREATE CONSTRAINT {code.lower()}_id IF NOT EXISTS FOR (n:{code}) REQUIRE n.id IS UNIQUE;
"""
    
    return template


def generate_templates_file(specs: Dict[str, Any], output_dir: Path) -> None:
    """Generate template files for all classes."""
    classes = specs["classes"]
    aliases = specs["aliases"]
    
    # Create templates directory
    templates_dir = output_dir / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Generate templates for each class
    for class_spec in classes:
        code = class_spec["code"]
        
        # Generate Markdown template
        markdown_template = generate_markdown_template(class_spec, aliases)
        markdown_file = templates_dir / f"{code}_markdown.j2"
        with open(markdown_file, 'w') as f:
            f.write(markdown_template)
        
        # Generate Cypher template
        cypher_template = generate_cypher_template(class_spec)
        cypher_file = templates_dir / f"{code}_cypher.j2"
        with open(cypher_file, 'w') as f:
            f.write(cypher_template)
    
    print(f"Generated templates in {templates_dir}")
    print(f"Created {len(classes) * 2} template files")


def main():
    """Main code generation function."""
    # Get paths
    current_dir = Path(__file__).parent
    specs_dir = current_dir / "specs"
    output_dir = current_dir.parent
    
    # Load specifications
    specs = load_yaml_specs(specs_dir)
    
    # Generate templates
    generate_templates_file(specs, output_dir)


if __name__ == "__main__":
    main()
