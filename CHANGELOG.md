# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Renamed package from `collie` to `infoextract_cidoc`
- Foundation tooling: pre-commit, mypy, bandit, coverage
- MkDocs Material documentation site
- LangStruct extraction pipeline (replaces PydanticAI)
- GraphForge optional output module

## [0.1.0] - 2024-01-01

### Added
- Initial release with CIDOC CRM v7.1.3 support
- 99 E-class Pydantic models, 322 P-properties
- AI-powered information extraction via PydanticAI + Gemini 2.5 Flash
- NetworkX graph construction and social network analysis
- Markdown, Cypher, and NetworkX output formats
- Visualization module (matplotlib static, plotly interactive)
- Validation framework (cardinality, type alignment)
