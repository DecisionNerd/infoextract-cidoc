# Examples

The [`examples/`](https://github.com/decisionnerd/infoextract-cidoc/tree/main/examples) directory contains runnable end-to-end scripts.

## Prerequisites

```bash
pip install infoextract-cidoc[viz]
export GEMINI_API_KEY="your-key-here"
```

Any [LiteLLM-compatible](https://docs.litellm.ai/docs/providers) model works via `LANGSTRUCT_DEFAULT_MODEL`:

```bash
export LANGSTRUCT_DEFAULT_MODEL="openai/gpt-4o"
```

## Einstein Biography Demo

**Script**: [`examples/einstein_demo.py`](https://github.com/decisionnerd/infoextract-cidoc/blob/main/examples/einstein_demo.py)

Runs the complete pipeline on Albert Einstein's biography:

```
Text (einstein.md)
  → LangStructExtractor.extract()        # LLM extraction
  → resolve_extraction()                 # stable UUID5 assignment
  → map_to_crm_entities()               # typed E-class instances
  → Markdown reports                     # CARD, NARRATIVE, TABLE styles
  → NetworkX graph + analysis            # centrality, communities
  → matplotlib / plotly visualizations  # static + interactive
  → Cypher script                        # Neo4j / Memgraph import
```

**Run:**

```bash
GEMINI_API_KEY=... python examples/einstein_demo.py
```

**Output** (written to `examples/output/einstein/`):

| Path | Contents |
|------|----------|
| `markdown/entity_*.md` | Individual entity cards |
| `markdown/entities_summary.md` | Full entity table |
| `markdown/narrative_*.md` | Narrative descriptions for key entities |
| `plots/network_overview.png` | Static network graph |
| `plots/community_structure.png` | Community detection plot |
| `plots/degree_centrality.png` | Degree centrality heatmap |
| `plots/interactive_network.html` | Interactive plotly network |
| `einstein_network.cypher` | Cypher MERGE script |
| `network_summary.md` | Network statistics summary |

## Adding Your Own Example

1. Create `examples/your_example.py`
2. Use the standard three-step pipeline:

```python
from infoextract_cidoc.extraction import (
    LangStructExtractor,
    resolve_extraction,
    map_to_crm_entities,
)

extractor = LangStructExtractor()
lite_result = extractor.extract(your_text)
extraction_result = resolve_extraction(lite_result)
entities, relations = map_to_crm_entities(extraction_result)
```

3. Output to `examples/output/your_example/` (git-ignored).
