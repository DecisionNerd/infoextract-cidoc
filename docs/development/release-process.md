# Release Process

## Version Bump

```bash
python scripts/bump_version.py 0.2.0
```

This updates `pyproject.toml` and `src/infoextract_cidoc/__init__.py`.

## CHANGELOG

Update `CHANGELOG.md`:
1. Rename `[Unreleased]` to `[0.2.0] - YYYY-MM-DD`
2. Add new `[Unreleased]` section at top

## Release

1. Commit: `git commit -m "chore: bump version to 0.2.0"`
2. Tag: `git tag v0.2.0`
3. Push: `git push origin main --tags`
4. Create GitHub release - PyPI publish triggers automatically
