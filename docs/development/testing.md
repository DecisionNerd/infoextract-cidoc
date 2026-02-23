# Testing

## Test Structure

```
src/infoextract_cidoc/tests/
├── unit/           # Fast, isolated unit tests
├── golden/         # Golden-file regression tests
└── test_networkx_integration.py
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `unit` | Fast, no external deps |
| `integration` | Multi-component tests |
| `golden` | Golden-file regression tests |
| `llm` | Requires live LLM API key (skipped in CI) |

## Running Tests

```bash
make test                                    # All tests
make test-unit                               # Unit tests
pytest -m "not llm" src/infoextract_cidoc/  # Skip LLM tests
pytest -k test_resolution                    # Run specific test
make coverage                                # With coverage report
```
