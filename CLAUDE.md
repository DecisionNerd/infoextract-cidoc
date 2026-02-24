# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

AI-powered CIDOC CRM v7.1.3 information extraction from unstructured text, targeting cultural heritage and genealogical data. Uses [LangStruct](https://github.com/DecisionNerd/langstruct) (a DSPy wrapper) for LLM-backed structured extraction.

## Commands

```bash
# Development
make lint          # ruff check src/
make format        # ruff format src/
make type-check    # mypy
make security      # bandit

# Testing
make test          # all tests (excluding llm marker)
make test-unit     # unit tests only
make test-golden   # golden-file regression tests
make coverage      # with --cov report

# Single test
uv run pytest src/infoextract_cidoc/tests/unit/test_pipeline_integration.py -v
uv run pytest -k "test_source_text" -v

# LLM e2e (requires Gemini key)
GEMINI_API_KEY=... uv run pytest src/infoextract_cidoc/tests/test_llm_e2e.py -m llm -v

# Pre-push gate (mirrors CI)
make pre-push      # format-check + lint + type-check + security + coverage
```

## Architecture

### Extraction pipeline (the core flow)

```
Text
  → LangStructExtractor.extract()        # LangStruct/DSPy → LiteExtractionResult
  → resolve_extraction()                 # LiteExtractionResult → ExtractionResult
  → map_to_crm_entities()               # ExtractionResult → (list[CRMEntity], list[CRMRelation])
  → Output modules                       # Markdown / Cypher / NetworkX / GraphForge
```

### Two-schema design (critical to understand)

The pipeline uses **two separate entity schemas** that serve different purposes:

**Lite schema** (`extraction/lite_schema.py`) — what the LLM fills in:
- `LiteEntity`: uses `ref_id` strings (e.g. `"person_1"`) instead of UUIDs so the LLM can write consistent cross-references. Has `source_snippet` for provenance.
- `LiteRelationship`: links entities by `source_ref`/`target_ref` string IDs.
- `LiteExtractionResult`: the raw LLM output bag.

**Resolved schema** (`extraction/models.py`) — after UUID assignment:
- `ExtractedEntity` and typed subclasses (`PersonExtraction`, `EventExtraction`, `PlaceExtraction`, `ObjectExtraction`, `TimeExtraction`) — carry stable UUIDs, rich typed fields, and `source_text`.
- `ExtractedRelationship`: links via UUID `source_id`/`target_id`. Broken links (refs to non-existent entities) are silently dropped here.
- `ExtractionResult`: the resolved bag passed downstream.

**Resolution** (`extraction/resolution.py`) maps entity types to subclasses via `_ENTITY_TYPE_MAP` and generates stable UUID5s from a fixed namespace + label, so re-extracting the same entity always yields the same UUID.

### CRM layer (`models/base.py`)

`CRMEntity` and `CRMRelation` are the stable output targets. `CRMEntity` is subclassed for specific E-classes (`E21_Person`, `E5_Event`, `E53_Place`, `E22_HumanMadeObject`, `E52_TimeSpan`, etc.). Subclasses add **shortcut fields** — UUID references to related entities (e.g. `E5_Event.timespan`, `E22_HumanMadeObject.produced_by`) that the Cypher emitter expands into P-property edges.

`models/generated/e_classes.py` contains the full CIDOC CRM class hierarchy auto-generated from YAML specs in `codegen/specs/`. **Do not edit it manually.**

### Output modules (`io/`)

| Module | Entry point | Notes |
|--------|------------|-------|
| `to_markdown.py` | `to_markdown(entity, MarkdownStyle.CARD)` | CARD / DETAILED / NARRATIVE / TABLE styles |
| `to_cypher.py` | `generate_cypher_script(entities)` | Idempotent MERGE/UNWIND for Neo4j/Memgraph |
| `to_networkx/` | `to_networkx_graph(entities)` | NetworkX DiGraph; analysis + visualization helpers |
| `to_graphforge.py` | `to_graphforge_graph(entities, rels)` | Optional dep: `pip install infoextract-cidoc[graphforge]` |

The Cypher emitter derives **all edges from entity shortcut fields** (not from `CRMRelation` directly). `CRMRelation.source_text` is stored but not yet emitted as a Cypher relationship property.

### LangStructExtractor (`extraction/langstruct_extractor.py`)

Wraps LangStruct with `use_sources=True` (populates `source_snippet`). Default model: `LANGSTRUCT_DEFAULT_MODEL` env var, falling back to `gemini/gemini-3-flash-preview`. Model string is LiteLLM-compatible so any provider works. `extract()` is synchronous; `extract_async()` wraps it in `asyncio.to_thread`.

## Test layout

```
tests/
  unit/          # @pytest.mark.unit — fast, no I/O
  golden/        # @pytest.mark.golden — snapshot regression (test_museum_object.py)
  test_networkx_integration.py   # @pytest.mark.integration
  test_llm_e2e.py                # @pytest.mark.llm — skipped without GEMINI_API_KEY
```

Golden tests in `tests/golden/` compare serialised output against checked-in fixtures. Update fixtures with `--update-snapshots` (or by deleting the fixture file) when output changes intentionally.

## Key constraints

- **Python 3.13+**, `uv` for all dependency management (not pip/poetry directly).
- `models/generated/` is auto-generated — edit `codegen/specs/` YAML instead.
- `CRMEntity` uses Pydantic V1-style `@validator` and `class Config` (migration to V2 `@field_validator` / `model_config` is pending).
- `F401` is marked `unfixable` in ruff config — remove unused imports manually.
- LLM tests are excluded from CI and from `make test`; run them explicitly with `-m llm`.
