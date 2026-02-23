#!/usr/bin/env python3
"""Bump version in pyproject.toml and src/infoextract_cidoc/__init__.py."""

import re
import sys
from pathlib import Path


def bump_version(new_version: str) -> None:
    root = Path(__file__).parent.parent

    # Update pyproject.toml
    pyproject = root / "pyproject.toml"
    content = pyproject.read_text()
    content = re.sub(
        r'^version = "[^"]*"',
        f'version = "{new_version}"',
        content,
        flags=re.MULTILINE,
    )
    pyproject.write_text(content)
    print(f"Updated pyproject.toml: version = {new_version!r}")

    # Update __init__.py
    init_file = root / "src" / "infoextract_cidoc" / "__init__.py"
    content = init_file.read_text()
    content = re.sub(
        r'^__version__ = "[^"]*"',
        f'__version__ = "{new_version}"',
        content,
        flags=re.MULTILINE,
    )
    init_file.write_text(content)
    print(f"Updated __init__.py: __version__ = {new_version!r}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <new_version>")
        sys.exit(1)
    bump_version(sys.argv[1])
