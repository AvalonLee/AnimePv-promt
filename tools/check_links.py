#!/usr/bin/env python3
"""Verify that every relative Markdown link in the repo resolves to a real file."""
from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules"}
LINK = re.compile(r"\]\((?!https?://|#|mailto:)([^)]+)\)")


def main() -> int:
    broken: list[str] = []
    checked_files = 0
    checked_links = 0

    for path in sorted(REPO.rglob("*.md")):
        rel = path.relative_to(REPO).as_posix()
        if SKIP_DIRS & set(pathlib.PurePosixPath(rel).parts):
            continue

        checked_files += 1
        text = path.read_text(encoding="utf-8", errors="replace")

        for match in LINK.finditer(text):
            target = match.group(1).split("#")[0].strip()
            if not target:
                continue
            checked_links += 1
            if not (path.parent / target).exists():
                broken.append(f"{rel} -> {target}")

    for item in broken:
        print(f"BROKEN LINK {item}")

    print(
        f"\nchecked {checked_links} relative link(s) "
        f"across {checked_files} file(s); {len(broken)} broken"
    )
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
