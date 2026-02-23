# infoextract-cidoc (COLLIE)

**Classful Ontology for Life-Events Information Extraction**

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-pytest-blue.svg)](https://pytest.org/)
[![Package: uv](https://img.shields.io/badge/package%20manager-uv-orange.svg)](https://github.com/astral-sh/uv)
[![CIDOC CRM](https://img.shields.io/badge/CIDOC%20CRM-v7.1.3-green.svg)](https://www.cidoc-crm.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-red.svg)](https://pydantic.dev/)
[![Neo4j Compatible](https://img.shields.io/badge/Neo4j-Compatible-blue.svg)](https://neo4j.com/)
[![Memgraph Compatible](https://img.shields.io/badge/Memgraph-Compatible-purple.svg)](https://memgraph.com/)

![COLLIE logo](collie-logo.png)

A developer-friendly toolkit for working with the **CIDOC CRM v7.1.3** in modern data workflows. infoextract-cidoc provides complete Pydantic models (99 classes, 322 properties), LangStruct-powered AI extraction, Markdown renderers, and Cypher emitters that bridge the gap between conceptual rigor and developer usability.

## Why infoextract-cidoc?

Cultural heritage and information extraction projects often need a **CRM-compliant backbone** without the overhead of RDF stacks. infoextract-cidoc:

- Keeps the conceptual rigor of CIDOC CRM
- Provides lean, open-world Pydantic validation
- Outputs formats directly usable by LLMs (Markdown) and LPGs (Cypher)
- Prioritizes ergonomics and performance for real-world extraction pipelines
- Zero RDF/OWL/JSON-LD dependencies

## Quick Start

> For a comprehensive getting started guide, see [QUICKSTART.md](QUICKSTART.md)

### Installation

```bash
pip install infoextract-cidoc

# With GraphForge graph database integration:
pip install infoextract-cidoc[graphforge]

# Using uv:
uv add infoextract-cidoc
```

### AI Extraction (New Pipeline)

```python
from infoextract_cidoc.extraction import LangStructExtractor, resolve_extraction, map_to_crm_entities
from infoextract_cidoc.io.to_markdown import to_markdown, MarkdownStyle

# Extract from text (set GOOGLE_API_KEY or LANGSTRUCT_DEFAULT_MODEL env var)
extractor = LangStructExtractor()
lite_result = extractor.extract(
    "Albert Einstein was born on March 14, 1879, in Ulm, Germany. "
    "He won the Nobel Prize in Physics in 1921."
)

# Resolve to stable UUIDs
extraction_result = resolve_extraction(lite_result)

# Map to CIDOC CRM entities
crm_entities, crm_relations = map_to_crm_entities(extraction_result)

# Render to Markdown
for entity in crm_entities:
    print(to_markdown(entity, MarkdownStyle.CARD))
```

### CRM Models (No AI Needed)

```python
from infoextract_cidoc.models.generated.e_classes import EE22_HumanMadeObject
from infoextract_cidoc.io.to_markdown import to_markdown, MarkdownStyle
from infoextract_cidoc.io.to_cypher import generate_cypher_script

# Create a CRM entity (string IDs are automatically converted to UUIDs)
vase = EE22_HumanMadeObject(
    id="obj_001",
    label="Ancient Greek Vase",
    type=["E55:Vessel", "E55:Ceramic"]
)

# Render as Markdown
markdown = to_markdown(vase, MarkdownStyle.CARD)

# Generate Cypher for Neo4j/Memgraph
cypher = generate_cypher_script([vase])
```

## CLI

```bash
# Extract entities from text
infoextract-cidoc extract --text "Marie Curie was born in Warsaw in 1867."

# Extract from file
infoextract-cidoc extract --file biography.txt --output ./output/

# Run complete workflow
infoextract-cidoc workflow --file biography.txt --all --output results/

# Run Einstein demo
infoextract-cidoc demo --einstein
```

## Core Features

### AI-Powered Information Extraction
- **LangStruct pipeline** for single-pass entity and relationship extraction
- **Entity Resolution** with stable UUID5 identifiers and deduplication
- **Relationship Resolution** with broken link detection and logging
- **CRM Mapping** to E21 Person, E5 Event, E53 Place, E22 Object, E52 Time-Span
- DSPy optimization support for fine-tuning extraction quality
- Works with any LiteLLM-compatible model (Gemini, OpenAI, Anthropic, etc.)

### Pydantic Models
- Complete CIDOC CRM v7.1.3 coverage (99 E-classes, 322 P-properties)
- Flexible UUID handling with automatic string-to-UUID conversion
- Canonical JSON schema with stable IDs and explicit cross-references
- Auto-generated from curated YAML specifications

#### Class Naming Convention

- **Official CIDOC CRM**: `E1`, `E22`, `E96` (class codes)
- **Python Classes**: `EE1_CRMEntity`, `EE22_HumanMadeObject`, `EE96_Purchase`
- **Pattern**: `E{code}_{label_without_spaces}`

### Markdown Renderers
- **Entity Cards**: Concise summaries optimized for LLM prompts
- **Detailed Narratives**: Rich descriptions with full context
- **Tabular Summaries**: Structured data presentation

### NetworkX Integration
- Direct conversion from CRM entities to NetworkX graphs
- Built-in social network analysis (centrality, communities)
- Temporal network analysis for historical data

### Output Formats
- **Markdown** (4 styles): entity cards, detailed, tabular, narrative
- **Cypher**: idempotent MERGE/UNWIND scripts for Neo4j/Memgraph
- **NetworkX**: graph objects for programmatic analysis
- **GraphForge** (optional): `pip install infoextract-cidoc[graphforge]`

### Validation Framework
- Cardinality enforcement (configurable from warnings to strict)
- Type alignment validation
- Extensible validation profiles

## Complete Workflow

```python
from infoextract_cidoc.extraction import LangStructExtractor, resolve_extraction, map_to_crm_entities
from infoextract_cidoc.io.to_networkx import to_networkx_graph
from infoextract_cidoc.io.to_cypher import generate_cypher_script
from infoextract_cidoc.visualization import plot_network_graph

# 1. Extract entities via LangStruct
extractor = LangStructExtractor()
lite_result = await extractor.extract_async("""
Albert Einstein was born on March 14, 1879, in Ulm, Germany.
He developed the theory of relativity and won the Nobel Prize in 1921.
""")

# 2. Resolve and map to CRM
extraction_result = resolve_extraction(lite_result)
crm_entities, crm_relations = map_to_crm_entities(extraction_result)

# 3. Serialize as canonical JSON
json_data = [entity.model_dump(mode='json') for entity in crm_entities]

# 4. Convert to NetworkX graph for social network analysis
graph = to_networkx_graph(crm_entities)

# 5. Visualize the network
plot_network_graph(graph, title="Einstein's Life Network")

# 6. Export to Cypher for graph database persistence
cypher_script = generate_cypher_script(crm_entities)
```

## Project Structure

```
src/infoextract_cidoc/
├── extraction/           # AI extraction pipeline
│   ├── lite_schema.py   # LangStruct output schema
│   ├── resolution.py    # Entity/relationship resolution
│   ├── crm_mapper.py    # CRM mapping layer
│   └── langstruct_extractor.py  # LangStructExtractor
├── models/               # Pydantic CRM models
│   ├── base.py          # CRMEntity, CRMRelation
│   └── generated/       # Auto-generated E-classes (99)
├── io/                   # Output modules
│   ├── to_markdown.py   # Markdown renderers
│   ├── to_cypher.py     # Cypher emitters
│   ├── to_networkx/     # NetworkX conversion
│   └── to_graphforge.py # GraphForge (optional)
├── validators/           # Validation framework
├── visualization/        # matplotlib/plotly plots
├── codegen/              # YAML -> Pydantic generation
└── tests/                # Test suite (77 tests)
```

## Testing

```bash
make test           # Run all tests
make test-unit      # Unit tests only
make coverage       # With coverage report
make pre-push       # Full CI: lint + type-check + security + coverage
```

## Documentation

- **[Quickstart](QUICKSTART.md)** - Getting started guide
- **[Contributing](CONTRIBUTING.md)** - Development workflow
- **[Changelog](CHANGELOG.md)** - Version history
- **[HOWTOs](docs/HOWTOs.md)** - Comprehensive modeling guide
- **[CIDOC CRM Standard](docs/cidoc-crm-standard.md)** - Official specification

## Project Status

- **Phase 1**: Complete - Core CIDOC CRM implementation
- **Phase 2**: Complete - LangStruct extraction pipeline, validation, full CRM coverage
- **Phase 3**: Planned - Profile packs and additional analysis tools

**Current Coverage**: 99 E-classes, 322 P-properties (complete CRM 7.1.3)
**Test Status**: 77 tests passing (100% success rate)
**CI/CD**: GitHub Actions with uv, ruff, mypy, bandit, codecov

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- CIDOC CRM Working Group for the foundational ontology
- Pydantic team for the excellent validation framework
- Neo4j community for Cypher language inspiration

---

**Made with care for the cultural heritage and information extraction community**
