#!/usr/bin/env python3
"""Verify the declared project version and Chinese brand name stay in sync.

Version and brand strings live in several places (skill manifest, release
manifest, SKILL.md, README badge, doc headers). They drift silently, so
this asserts they all agree.
"""
from __future__ import annotations

import pathlib
import re
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent

EXPECTED_NAME_ZH = "AnimePv-promt"


def read_yaml(rel: str):
    path = REPO / rel
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    problems: list[str] = []
    versions: dict[str, str] = {}

    # 1. skill manifest is the source of truth
    manifest = read_yaml("skill/manifest.yaml") or {}
    skill = manifest.get("skill") or {}
    truth = str(skill.get("version") or "")
    if not truth:
        print("cannot determine version from skill/manifest.yaml")
        return 1
    versions["skill/manifest.yaml"] = truth

    if skill.get("name_zh") != EXPECTED_NAME_ZH:
        problems.append(
            f"skill/manifest.yaml: name_zh is {skill.get('name_zh')!r}, "
            f"expected {EXPECTED_NAME_ZH!r}"
        )

    # 2. release manifest
    release = (read_yaml("release/release-manifest.yaml") or {}).get("release") or {}
    project = release.get("project") or {}
    if project.get("version"):
        versions["release/release-manifest.yaml"] = str(project["version"])
    if project.get("name_zh") != EXPECTED_NAME_ZH:
        problems.append(
            f"release/release-manifest.yaml: name_zh is "
            f"{project.get('name_zh')!r}, expected {EXPECTED_NAME_ZH!r}"
        )
    tag = release.get("git_tag")
    if tag and tag != f"v{truth}":
        problems.append(
            f"release/release-manifest.yaml: git_tag {tag} does not match v{truth}"
        )

    # 3. SKILL.md header
    skill_md = (REPO / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)", skill_md, re.MULTILINE)
    if m:
        versions["SKILL.md"] = m.group(1)
    else:
        problems.append("SKILL.md: no 'Version: X.Y.Z' header found")
    if EXPECTED_NAME_ZH not in skill_md:
        problems.append(f"SKILL.md: missing Chinese brand name {EXPECTED_NAME_ZH}")

    # 4. README badge
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    m = re.search(r"badge/version-([0-9]+\.[0-9]+\.[0-9]+)-", readme)
    if m:
        versions["README.md badge"] = m.group(1)
    else:
        problems.append("README.md: no version badge found")
    if EXPECTED_NAME_ZH not in readme:
        problems.append(f"README.md: missing Chinese brand name {EXPECTED_NAME_ZH}")

    # all declared versions must agree
    mismatched = {k: v for k, v in versions.items() if v != truth}
    for where, got in mismatched.items():
        problems.append(f"{where}: version {got} does not match {truth}")

    for item in problems:
        print(f"VERSION FAIL {item}")

    print(
        f"\nproject version {truth}, brand {EXPECTED_NAME_ZH}; "
        f"checked {len(versions)} declaration site(s); {len(problems)} problem(s)"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
