# Tutorial: Analyzing a Biography

This tutorial walks through extracting and analyzing a historical biography.

## 1. Prepare Your Text

```python
text = """
Albert Einstein was born on March 14, 1879, in Ulm, in the Kingdom of Württemberg.
He developed the theory of special relativity in 1905 while working at the Swiss Patent Office.
In 1921, he received the Nobel Prize in Physics for his discovery of the photoelectric effect.
He died on April 18, 1955, in Princeton, New Jersey.
"""
```

## 2. Extract Entities

```python
from infoextract_cidoc.extraction import LangStructExtractor, resolve_extraction, map_to_crm_entities

extractor = LangStructExtractor()
lite_result = extractor.extract(text)
extraction_result = resolve_extraction(lite_result)
entities, relations = map_to_crm_entities(extraction_result)
```

## 3. Render to Markdown

```python
from infoextract_cidoc.io.to_markdown import to_markdown, MarkdownStyle, render_table

# Summary table
print(render_table(entities))

# Detailed card for each entity
for entity in entities:
    print(to_markdown(entity, MarkdownStyle.DETAILED))
```

## 4. Analyze with NetworkX

```python
from infoextract_cidoc.io.to_networkx import (
    to_networkx_graph, calculate_centrality_measures, find_communities
)

graph = to_networkx_graph(entities)
centrality = calculate_centrality_measures(graph)
communities = find_communities(graph)

print(f"Most central entity: {max(centrality['degree'], key=centrality['degree'].get)}")
```

## 5. Export to Cypher

```python
from infoextract_cidoc.io.to_cypher import generate_cypher_script

cypher = generate_cypher_script(entities)
with open("biography.cypher", "w") as f:
    f.write(cypher)
```
