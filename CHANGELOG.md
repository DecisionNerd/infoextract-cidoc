# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
