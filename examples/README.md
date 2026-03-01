# Examples

Runnable end-to-end scripts that demonstrate the full infoextract-cidoc pipeline.

## Prerequisites

Install the package with visualization dependencies:

```bash
uv add infoextract-cidoc[viz]
# or
pip install infoextract-cidoc[viz]
```

Set an API key for LLM-powered extraction:

```bash
export GEMINI_API_KEY="your-key-here"
# or any LiteLLM-compatible model:
export LANGSTRUCT_DEFAULT_MODEL="openai/gpt-4o"
```

## Available Examples

### `einstein_demo.py`

Complete pipeline demo using Albert Einstein's biography as input text.

**What it does:**
1. Extracts entities and relationships from biographical text via LangStruct
2. Resolves them to stable UUID5-identified CRM entities
3. Renders Markdown cards, narratives, and a summary table
4. Builds a NetworkX graph and runs centrality / community analysis
5. Saves static (matplotlib) and interactive (plotly) network plots
6. Exports a Cypher script ready for Neo4j or Memgraph

**Run it:**

```bash
GEMINI_API_KEY=... python examples/einstein_demo.py
```

Output is written to `examples/output/einstein/`.

## Output Directory

Generated output (`examples/output/`) is git-ignored. Each example writes to
its own subdirectory under `output/`.
