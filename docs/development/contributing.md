# Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for the full contributing guide.

## Development Setup

```bash
git clone https://github.com/decisionnerd/infoextract-cidoc.git
cd infoextract-cidoc
uv sync
uv run pre-commit install
```

## Running Tests

```bash
make test        # All tests
make test-unit   # Unit tests only
make test-golden # Golden tests only
```
