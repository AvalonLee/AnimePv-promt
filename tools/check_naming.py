#!/usr/bin/env python3
"""Guard against the legacy `AnimePV-H3` project name leaking back in.

A few files intentionally document the rename (changelog, developer guide) or
implement the check itself, so they are allowlisted.
"""
from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
PATTERN = re.compile(r"animepv", re.IGNORECASE)
SKIP_DIRS = {".git", "node_modules"}
SUFFIXES = {".md", ".yaml", ".yml", ".py"}
ALLOWLIST = {
    "CHANGELOG.md",
    "docs/DEVELOPER_GUIDE.md",
    "tools/README.md",
    "tools/check_naming.py",
}


def main() -> int:
    hits: list[str] = []
    scanned = 0

    for path in sorted(REPO.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        rel = path.relative_to(REPO).as_posix()
        if SKIP_DIRS & set(pathlib.PurePosixPath(rel).parts):
            continue
        if rel in ALLOWLIST:
            continue

        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            if PATTERN.search(line):
                hits.append(f"{rel}:{lineno}: {line.strip()}")

    for hit in hits:
        print(f"LEGACY NAME {hit}")

    if hits:
        print("\nLegacy name found. Migrate to 'AstraForge Studio'.")
        return 1

    print(f"scanned {scanned} file(s); naming migration clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
