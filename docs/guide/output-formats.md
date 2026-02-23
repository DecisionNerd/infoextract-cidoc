# Output Formats

## Markdown

Four rendering styles:

```python
from infoextract_cidoc.io.to_markdown import to_markdown, MarkdownStyle, render_table

to_markdown(entity, MarkdownStyle.CARD)      # Concise card
to_markdown(entity, MarkdownStyle.DETAILED)  # Full details
to_markdown(entity, MarkdownStyle.TABLE)     # Tabular row
to_markdown(entity, MarkdownStyle.NARRATIVE) # Prose narrative
render_table(entities)                        # Multi-entity table
```

## Cypher (Neo4j / Memgraph)

```python
from infoextract_cidoc.io.to_cypher import generate_cypher_script

cypher = generate_cypher_script(entities)
# Returns Cypher CREATE statements for graph database import
```

## NetworkX

```python
from infoextract_cidoc.io.to_networkx import to_networkx_graph

graph = to_networkx_graph(entities)
# Returns networkx.Graph with entity nodes and relationship edges
```

## GraphForge (Optional)

Requires `pip install infoextract-cidoc[graphforge]`.

```python
from infoextract_cidoc.io.to_graphforge import to_graphforge_graph, to_graphforge_cypher

graph = to_graphforge_graph(entities, relations)
cypher = to_graphforge_cypher(entities, relations)
```
