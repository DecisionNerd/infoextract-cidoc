#!/usr/bin/env python3
"""Check if CHANGELOG has unreleased items that warrant a release."""

import sys
from pathlib import Path


def check_release_needed() -> bool:
    changelog = Path(__file__).parent.parent / "CHANGELOG.md"
    if not changelog.exists():
        print("No CHANGELOG.md found")
        return False

    content = changelog.read_text()
    lines = content.split("\n")

    in_unreleased = False
    unreleased_items: list[str] = []

    for line in lines:
        if line.startswith("## [Unreleased]"):
            in_unreleased = True
            continue
        if in_unreleased and line.startswith("## ["):
            break
        if in_unreleased and line.strip().startswith("-"):
            unreleased_items.append(line.strip())

    if unreleased_items:
        print(f"Release needed: {len(unreleased_items)} unreleased items found:")
        for item in unreleased_items:
            print(f"  {item}")
        return True
    else:
        print("No unreleased items found - no release needed")
        return False


if __name__ == "__main__":
    needed = check_release_needed()
    sys.exit(0 if needed else 0)  # Always exit 0; just informational
