# infoextract-cidoc

**AI-powered CIDOC CRM v7.1.3 information extraction for cultural heritage and genealogical data.**

infoextract-cidoc (COLLIE) bridges the gap between conceptual rigor and developer usability by combining:

- **AI Extraction**: LangStruct-powered entity and relationship extraction from unstructured text
- **CIDOC CRM Models**: Full coverage of 99 E-classes and 322 P-properties
- **Multiple Outputs**: Markdown, Cypher (Neo4j/Memgraph), NetworkX graphs, and GraphForge

## Quick Example

```python
from infoextract_cidoc.extraction import LangStructExtractor, resolve_extraction, map_to_crm_entities
from infoextract_cidoc.io.to_markdown import to_markdown, MarkdownStyle

extractor = LangStructExtractor()
lite_result = extractor.extract("Albert Einstein was born in Ulm in 1879.")
extraction_result = resolve_extraction(lite_result)
entities, relations = map_to_crm_entities(extraction_result)

for entity in entities:
    print(to_markdown(entity, MarkdownStyle.CARD))
```

## Features

- **LangStruct Extraction** with DSPy optimization support
- **Entity Resolution** with stable UUID5 identifiers
- **CIDOC CRM Mapping** to E21 Person, E5 Event, E53 Place, E22 Object, E52 Time-Span
- **Relationship Resolution** with broken link detection and logging
- **NetworkX Integration** for social network analysis
- **Visualization** with matplotlib (static) and plotly (interactive)
- **GraphForge Integration** (optional) for graph database workflows

## Installation

```bash
pip install infoextract-cidoc
# With GraphForge support:
pip install infoextract-cidoc[graphforge]
```

## License

MIT License. See [LICENSE](https://github.com/decisionnerd/infoextract-cidoc/blob/main/LICENSE).
