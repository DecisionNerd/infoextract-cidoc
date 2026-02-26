# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-02-26

### Changed
- Broadened Python support from 3.13-only to 3.12+; test matrix now covers 3.12/3.13 × Ubuntu/macOS/Windows (floor set by `langstruct>=0.2.0`)

## [0.1.1] - 2026-02-25

### Changed
- Migrated P-property registry from bespoke YAML spec to LinkML (`codegen/cidoc_crm_properties.yaml`); `generate_registry.py` replaced by `generate_properties.py` using `SchemaView`
- `properties.py` regenerated with identical `P`/`DOMAIN` interface; dead `RANGE` dict removed
- Fixed all pre-existing `make pre-push` gate failures: 38 mypy errors, bandit B324 (MD5), coverage threshold
- Improved CI/CD: parallel jobs, cross-platform test matrix, hard quality gates, label-based workflows

## [0.1.0] - 2026-02-23

### Added
- CIDOC CRM v7.1.3 complete coverage: 99 E-class Pydantic models, 322 P-properties
- LangStruct extraction pipeline: `LangStructExtractor`, `resolve_extraction`, `map_to_crm_entities`
- Lite entity schema (`LiteEntity`, `LiteRelationship`, `LiteExtractionResult`) for single-pass LLM extraction
- Entity resolution with stable UUID5 identifiers, label deduplication, and broken-link rejection
- CRM mapping layer dispatching to E21 Person, E5 Event, E53 Place, E22 Object, E52 Time-Span
- NetworkX graph construction and social network analysis (centrality, communities)
- Markdown output (4 styles: card, detailed, table, narrative)
- Cypher emitter for Neo4j and Memgraph
- GraphForge optional output module (`pip install infoextract-cidoc[graphforge]`)
- Visualization module (matplotlib static, plotly interactive)
- Validation framework (cardinality enforcement, type alignment)
- CLI: `infoextract-cidoc extract | analyze | workflow | demo`
- MkDocs Material documentation site
- Full CI/CD: GitHub Actions (test, docs, publish, changelog-check, pr-labeler, release-tracking)
- Pre-commit hooks (ruff, mypy, bandit, markdownlint)
- 85 tests (100% passing)
