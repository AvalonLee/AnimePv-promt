#!/usr/bin/env python3
"""Guard against legacy project names leaking back in.

Legacy names: `AnimePV-H3` (pre-rename), `AstraForge Studio` / `星铸工坊`
(the intermediate mainline project). The current project name is
`AnimePv-promt`.

A few files intentionally document the renames (changelog, developer guide)
or implement the check itself, so they are allowlisted.
"""
from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
LEGACY_PATTERNS = [
    re.compile(r"animepv-h3", re.IGNORECASE),
    re.compile(r"astraforge", re.IGNORECASE),
    re.compile(r"星铸工坊"),
]
SKIP_DIRS = {".git", "node_modules"}
SUFFIXES = {".md", ".yaml", ".yml", ".py"}
ALLOWLIST = {
    "CHANGELOG.md",
    "docs/DEVELOPER_GUIDE.md",
    "docs/KINETIC-ENGINE-UPGRADE-PLAN.md",
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
            if any(p.search(line) for p in LEGACY_PATTERNS):
                hits.append(f"{rel}:{lineno}: {line.strip()}")

    for hit in hits:
        print(f"LEGACY NAME {hit}")

    if hits:
        print("\nLegacy name found. Migrate to 'AnimePv-promt'.")
        return 1

    print(f"scanned {scanned} file(s); naming migration clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
