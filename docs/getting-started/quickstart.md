# Quickstart

Extract CIDOC CRM entities from text in minutes.

## Basic Extraction

```python
from infoextract_cidoc.extraction import LangStructExtractor, resolve_extraction, map_to_crm_entities

# Initialize extractor (reads LANGSTRUCT_DEFAULT_MODEL env var or uses gemini/gemini-2.5-flash)
extractor = LangStructExtractor()

# Extract from text
lite_result = extractor.extract(
    "Marie Curie was born in Warsaw in 1867 and died in Passy in 1934. "
    "She received the Nobel Prize in Physics in 1903."
)

# Resolve entities (assign stable UUIDs)
extraction_result = resolve_extraction(lite_result)

# Map to CRM entities
entities, relations = map_to_crm_entities(extraction_result)

print(f"Extracted {len(entities)} entities and {len(relations)} relations")
```

## CLI Usage

```bash
# Extract from text
infoextract-cidoc extract --text "Marie Curie was born in Warsaw in 1867."

# Extract from file
infoextract-cidoc extract --file biography.txt --output ./output/

# Run complete workflow (extract + analyze + visualize)
infoextract-cidoc workflow --text "..." --visualize

# Run Einstein demo
infoextract-cidoc demo --einstein
```

## Output Formats

```python
from infoextract_cidoc.io.to_markdown import to_markdown, MarkdownStyle, render_table
from infoextract_cidoc.io.to_cypher import generate_cypher_script
from infoextract_cidoc.io.to_networkx import to_networkx_graph

# Markdown
for entity in entities:
    print(to_markdown(entity, MarkdownStyle.CARD))

# Cypher (Neo4j/Memgraph)
cypher = generate_cypher_script(entities)
print(cypher)

# NetworkX graph
graph = to_networkx_graph(entities)
print(f"Nodes: {graph.number_of_nodes()}, Edges: {graph.number_of_edges()}")
```
