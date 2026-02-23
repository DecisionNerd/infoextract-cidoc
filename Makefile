.PHONY: lint format format-check type-check security test test-unit test-golden coverage check-coverage pre-push docs-serve docs-build clean

# --- Code quality ---

lint:
	uv run ruff check src/

format:
	uv run ruff format src/

format-check:
	uv run ruff format --check src/

type-check:
	uv run mypy src/infoextract_cidoc/

security:
	uv run bandit -c pyproject.toml -r src/infoextract_cidoc/

# --- Testing ---

test:
	uv run pytest src/infoextract_cidoc/tests/ -v

test-unit:
	uv run pytest src/infoextract_cidoc/tests/unit/ -v -m unit

test-golden:
	uv run pytest src/infoextract_cidoc/tests/golden/ -v -m golden

coverage:
	uv run pytest src/infoextract_cidoc/tests/ --cov=src/infoextract_cidoc --cov-report=term-missing --cov-report=xml

check-coverage:
	uv run pytest src/infoextract_cidoc/tests/ --cov=src/infoextract_cidoc --cov-fail-under=70

# --- Pre-push gate (mirrors CI) ---

pre-push: format-check lint type-check security check-coverage

# --- Documentation ---

docs-serve:
	uv run mkdocs serve

docs-build:
	uv run mkdocs build --strict

# --- Cleanup ---

clean:
	rm -rf .pytest_cache htmlcov .coverage coverage.xml test-results*.xml site/ dist/ build/ __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
