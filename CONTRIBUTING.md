# Contributing to infoextract-cidoc

Thank you for your interest in contributing!

## Development Setup

1. Install [uv](https://docs.astral.sh/uv/): `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/decisionnerd/infoextract-cidoc.git
   cd infoextract-cidoc
   uv sync
   ```
3. Install pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

## Development Workflow

- **Run tests**: `make test`
- **Lint**: `make lint`
- **Format**: `make format`
- **Type check**: `make type-check`
- **All checks**: `make pre-push`

## Pull Request Guidelines

1. Fork the repository and create a feature branch from `main`
2. Write tests for new functionality
3. Update `CHANGELOG.md` with your changes under `[Unreleased]`
4. Ensure `make pre-push` passes
5. Submit a pull request with a clear description

## Commit Messages

Follow conventional commits format:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `test:` test additions or changes
- `refactor:` code refactoring
- `ci:` CI/CD changes
- `chore:` maintenance tasks

## Test Markers

- `unit` - fast, isolated unit tests
- `integration` - tests requiring multiple components
- `golden` - golden-file regression tests
- `llm` - tests requiring a live LLM API key (skipped in CI by default)
