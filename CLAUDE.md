# CLAUDE.md - Project Context for AI Assistants

## Project: infoextract-cidoc

**Purpose**: AI-powered CIDOC CRM v7.1.3 information extraction from unstructured text, targeting cultural heritage and genealogical data.

## Architecture

```
Text Input
  -> LangStruct Extractor (LiteExtractionResult)
  -> Entity Resolution (stable UUID assignment via uuid5)
  -> Relationship Resolution (broken link rejection)
  -> CRM Mapping (lite entities -> CRMEntity + CRMRelation)
  -> Outputs: Markdown / Cypher / NetworkX / GraphForge
```

## Key Files

| File | Role |
|------|------|
| `src/infoextract_cidoc/extraction/lite_schema.py` | LiteEntity, LiteRelationship, LiteExtractionResult |
| `src/infoextract_cidoc/extraction/resolution.py` | EntityRegistry, resolve_extraction() |
| `src/infoextract_cidoc/extraction/crm_mapper.py` | map_to_crm_entities() |
| `src/infoextract_cidoc/extraction/langstruct_extractor.py` | LangStructExtractor |
| `src/infoextract_cidoc/extraction/models.py` | ExtractionResult, ExtractedEntity (stable interface) |
| `src/infoextract_cidoc/models/base.py` | CRMEntity, CRMRelation (stable mapping target) |
| `src/infoextract_cidoc/main.py` | CLI orchestrator |
| `src/infoextract_cidoc/io/` | Output modules (markdown, cypher, networkx, graphforge) |

## CIDOC CRM Entity Types

- **E21**: Person (biographical data: birth/death, occupation)
- **E5**: Event (temporal, participant, location data)
- **E53**: Place (geographic: coordinates, country, region)
- **E22**: Human-Made Object (material, creator, condition)
- **E52**: Time-Span (temporal precision, duration)

## Development Commands

```bash
make test          # Run all tests
make lint          # Run ruff
make format        # Auto-format with ruff
make type-check    # Run mypy
make security      # Run bandit
make pre-push      # Full CI: format-check + lint + type-check + security + coverage
make docs-serve    # Serve docs locally
make docs-build    # Build static docs site
```

## Test Markers

- `@pytest.mark.unit` - fast, no external deps
- `@pytest.mark.integration` - multi-component tests
- `@pytest.mark.golden` - golden-file regression tests
- `@pytest.mark.llm` - requires live LLM API key (skipped in CI)

## Package Notes

- Python 3.13+, uses `uv` for dependency management
- Package: `infoextract_cidoc` (PyPI: `infoextract-cidoc`)
- CLI: `infoextract-cidoc extract --text "..."` or `infoextract-cidoc workflow`
- Optional dep: `pip install infoextract-cidoc[graphforge]` for GraphForge output
- Models in `src/infoextract_cidoc/models/generated/` are auto-generated from `codegen/specs/`; do not edit manually
