# infoextract-cidoc Quickstart Guide

Get up and running with infoextract-cidoc in minutes.

## What is infoextract-cidoc?

infoextract-cidoc (COLLIE) is a toolkit that combines:

- **LangStruct Extraction**: Single-pass entity and relationship extraction from unstructured text
- **CIDOC CRM Compliance**: Full implementation of CIDOC CRM v7.1.3 (99 classes, 322 properties)
- **NetworkX Analysis**: Social network analysis with centrality measures and community detection
- **Multiple Output Formats**: Markdown, Cypher (Neo4j/Memgraph), NetworkX, GraphForge

## Prerequisites

- Python 3.13+
- An LLM API key (Google Gemini, OpenAI, Anthropic, or any LiteLLM-compatible provider)

## Installation

```bash
pip install infoextract-cidoc

# With GraphForge support:
pip install infoextract-cidoc[graphforge]

# Development install:
git clone https://github.com/decisionnerd/infoextract-cidoc.git
cd infoextract-cidoc
uv sync
```

## API Key Setup

```bash
# Google Gemini (default model)
export GOOGLE_API_KEY="your-api-key-here"

# Or add to a .env file:
echo "GOOGLE_API_KEY=your-key" > .env

# Override the model:
export LANGSTRUCT_DEFAULT_MODEL="openai/gpt-4o-mini"
```

## Quick Start Examples

### 1. Run the Einstein Demo

The fastest way to see the full pipeline in action:

```bash
infoextract-cidoc demo --einstein
```

This runs the complete workflow: extract -> CRM mapping -> Markdown -> NetworkX -> visualization -> Cypher.

### 2. Extract Entities from Text

```bash
infoextract-cidoc extract --text "Marie Curie was born in Warsaw in 1867 and received the Nobel Prize in 1903."
```

### 3. Run Complete Workflow

```bash
infoextract-cidoc workflow --file biography.txt --all --output results/
```

## Python API

### Basic Extraction

```python
from infoextract_cidoc.extraction import LangStructExtractor, resolve_extraction, map_to_crm_entities

extractor = LangStructExtractor()

# Step 1: Extract (LangStruct fills LiteExtractionResult schema)
lite_result = extractor.extract(
    "Marie Curie was born in Warsaw in 1867. "
    "She received the Nobel Prize in Physics in 1903."
)

# Step 2: Resolve (assign stable UUIDs, filter broken links)
extraction_result = resolve_extraction(lite_result)

# Step 3: Map to CRM
entities, relations = map_to_crm_entities(extraction_result)

print(f"Extracted {len(entities)} entities and {len(relations)} relations")
```

### Async Extraction

```python
import asyncio
from infoextract_cidoc.extraction import LangStructExtractor, resolve_extraction, map_to_crm_entities

async def extract(text: str):
    extractor = LangStructExtractor()
    lite_result = await extractor.extract_async(text)
    extraction_result = resolve_extraction(lite_result)
    return map_to_crm_entities(extraction_result)

entities, relations = asyncio.run(extract("..."))
```

### Output Formats

```python
from infoextract_cidoc.io.to_markdown import to_markdown, MarkdownStyle, render_table
from infoextract_cidoc.io.to_cypher import generate_cypher_script
from infoextract_cidoc.io.to_networkx import to_networkx_graph, calculate_centrality_measures

# Markdown
for entity in entities:
    print(to_markdown(entity, MarkdownStyle.CARD))

# Summary table
print(render_table(entities))

# Cypher for Neo4j/Memgraph
cypher = generate_cypher_script(entities)
with open("entities.cypher", "w") as f:
    f.write(cypher)

# NetworkX graph
graph = to_networkx_graph(entities)
centrality = calculate_centrality_measures(graph)
```

### CRM Models Without AI

```python
from infoextract_cidoc.models.generated.e_classes import EE22_HumanMadeObject, EE21_Person
from infoextract_cidoc.models.base import CRMRelation
from infoextract_cidoc.io.to_cypher import generate_cypher_script

person = EE21_Person(label="Marie Curie")
obj = EE22_HumanMadeObject(label="Nobel Prize", type=["E55:Award"])

cypher = generate_cypher_script([person, obj])
```

## Extraction Pipeline Explained

The pipeline has three stages:

```
Text
  -> LangStructExtractor   # LLM fills LiteExtractionResult schema
  -> resolve_extraction    # Stage A: assign stable UUID5 IDs
                           # Stage B: resolve relationship refs, drop broken links
  -> map_to_crm_entities   # LiteEntity -> CRMEntity (E21/E5/E53/E22/E52)
  -> Outputs               # Markdown / Cypher / NetworkX / GraphForge
```

### LiteEntity vs CRMEntity

`LiteEntity` uses simple `ref_id` strings (e.g. `"person_1"`) so the LLM can consistently reference entities in relationships. The resolution stage converts these to stable UUID5 identifiers and deduplicates by label.

## Model Configuration

```python
# Use a specific model
extractor = LangStructExtractor(model="openai/gpt-4o-mini")

# Use env var
import os
os.environ["LANGSTRUCT_DEFAULT_MODEL"] = "anthropic/claude-3-haiku-20240307"
extractor = LangStructExtractor()

# Batch extraction
results = extractor.extract_batch([text1, text2, text3])
```

## Visualization

```python
from infoextract_cidoc.io.to_networkx import (
    to_networkx_graph, calculate_centrality_measures, find_communities
)
from infoextract_cidoc.visualization import plot_network_graph

graph = to_networkx_graph(entities)
centrality = calculate_centrality_measures(graph)
communities = find_communities(graph)

# Static matplotlib plot
plot_network_graph(
    graph,
    title="Entity Network",
    save_path="network.png",
    show_plot=False
)
```

## GraphForge Integration

Requires `pip install infoextract-cidoc[graphforge]`.

```python
from infoextract_cidoc.io.to_graphforge import to_graphforge_graph, to_graphforge_cypher

graph = to_graphforge_graph(entities, relations)
cypher = to_graphforge_cypher(entities, relations)
```

## Development Commands

```bash
make test          # Run all tests
make lint          # Run ruff
make format        # Auto-format with ruff
make type-check    # Run mypy
make security      # Run bandit
make pre-push      # Full CI gate
make docs-serve    # Serve docs locally
```

## Next Steps

- Read the full [API Reference](docs/reference/api.md)
- Explore [CIDOC CRM Models](docs/guide/crm-models.md)
- See [Output Formats](docs/guide/output-formats.md)
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
