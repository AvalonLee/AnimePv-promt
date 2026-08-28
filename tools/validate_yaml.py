#!/usr/bin/env python3
"""Validate all YAML component/schema files in AstraForge Studio.

Checks:
  1. Every *.yaml / *.yml file parses.
  2. Every entry under a top-level `components:` list declares id / risk.
  3. Shot-level components (camera, action, expression, transition) also
     declare the scoring fields required by the Developer Guide.

Creative direction and Style are composition layers rather than shot-level
components, so they are exempt from the scoring requirement.
"""
from __future__ import annotations

import pathlib
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".github", "node_modules"}
REQUIRED_COMPONENT_FIELDS = ("id", "slug", "risk")
REQUIRED_SCORE_FIELDS = ("stability_score", "impact_score")
SCORED_LIBRARIES = ("camera", "action", "expression", "transition")


def yaml_files() -> list[pathlib.Path]:
    files = []
    for path in sorted(REPO.rglob("*.y*ml")):
        if SKIP_DIRS & set(path.relative_to(REPO).parts):
            continue
        files.append(path)
    return files


def needs_scores(rel_path: str) -> bool:
    parts = pathlib.PurePosixPath(rel_path).parts
    return len(parts) > 1 and parts[0] == "library" and parts[1] in SCORED_LIBRARIES


def main() -> int:
    parse_errors: list[str] = []
    schema_errors: list[str] = []
    checked = 0
    components_seen = 0
    ids: dict[str, str] = {}
    slugs: dict[str, str] = {}

    for path in yaml_files():
        rel = path.relative_to(REPO).as_posix()
        try:
            docs = list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
        except yaml.YAMLError as exc:
            parse_errors.append(f"{rel}: {str(exc).splitlines()[0]}")
            continue

        checked += 1
        scored = needs_scores(rel)

        for doc in docs:
            if not isinstance(doc, dict):
                continue
            components = doc.get("components")
            if not isinstance(components, list):
                continue
            for index, component in enumerate(components):
                if not isinstance(component, dict):
                    schema_errors.append(f"{rel}: components[{index}] is not a mapping")
                    continue

                components_seen += 1
                label = component.get("id", f"components[{index}]")

                for field in REQUIRED_COMPONENT_FIELDS:
                    if field not in component:
                        schema_errors.append(f"{rel}: {label} missing '{field}'")

                if scored:
                    for field in REQUIRED_SCORE_FIELDS:
                        if field not in component:
                            schema_errors.append(f"{rel}: {label} missing '{field}'")

                component_id = component.get("id")
                if isinstance(component_id, str):
                    if component_id in ids:
                        schema_errors.append(
                            f"{rel}: duplicate id '{component_id}' "
                            f"(also in {ids[component_id]})"
                        )
                    else:
                        ids[component_id] = rel

                slug = component.get("slug")
                if isinstance(slug, str):
                    if slug in slugs:
                        schema_errors.append(
                            f"{rel}: duplicate slug '{slug}' "
                            f"(also in {slugs[slug]})"
                        )
                    else:
                        slugs[slug] = rel

    for line in parse_errors:
        print(f"PARSE FAIL  {line}")
    for line in schema_errors:
        print(f"SCHEMA FAIL {line}")

    total = len(parse_errors) + len(schema_errors)
    print(
        f"\nvalidated {checked} YAML file(s), "
        f"{components_seen} component(s), {len(slugs)} slug(s); "
        f"{total} problem(s) found"
    )
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
