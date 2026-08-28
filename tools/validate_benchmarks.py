#!/usr/bin/env python3
"""Validate AstraForge benchmark cases against the component libraries.

This catches drift between benchmark expectations and the actual libraries:
  1. Every benchmark declares the required fields.
  2. Referenced genre / theme / variation / template names exist.
  3. Referenced components exist in the component libraries.
  4. Declared risk budgets do not exceed the genre + duration limits.
  5. Six-dimension scores sum to the declared final_score.
"""
from __future__ import annotations

import pathlib
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
CASES_DIR = REPO / "benchmark" / "test-cases"

REQUIRED_TOP = ("benchmark", "input", "expected_routing", "scores")
REQUIRED_META = ("id", "name", "dimension", "status")

# Effective limits, mirroring core/quality-engine/risk-budget-gate.yaml
ACTION_LIMIT_BY_DURATION = {"5s": 1, "10s": 2, "15s": 2, "30s": 3}
ACTION_LIMIT_BY_GENRE = {"action": 2, "daily": 2, "magic": 2}

# Genre ceilings are baselines; these conditions raise them.
# Mirrors genre_ceiling_uplift in core/quality-engine/risk-budget-gate.yaml
ACTION_UPLIFT = (
    {"genre": "magic", "duration": "30s", "rarity": "SSR", "action_limit": 3},
    {"genre": "action", "duration": "30s", "rarity": None, "action_limit": 3},
)


def effective_action_limit(genre: str, duration: str, rarity: str | None) -> int:
    """Effective budget = min(genre, duration), then apply any uplift."""
    base = min(
        ACTION_LIMIT_BY_GENRE.get(genre, 99),
        ACTION_LIMIT_BY_DURATION.get(duration, 99),
    )
    for rule in ACTION_UPLIFT:
        if rule["genre"] != genre or rule["duration"] != duration:
            continue
        if rule["rarity"] is not None and rule["rarity"] != rarity:
            continue
        base = max(base, rule["action_limit"])
    return base
EFFECT_LIMIT_BY_DURATION = {"5s": 1, "10s": 2, "15s": 2, "30s": 3}

# Screen weight budget from core/multi-character/weight-rules.yaml
CHARACTER_BUDGET = 70
STABILITY_CAP_BY_CAST = {1: 35, 2: 32, 3: 28, 4: 24}
CONTRAST_DIMENSIONS_REQUIRED = 2

SCORE_KEYS = (
    "generation_stability",
    "character_consistency",
    "shot_feasibility",
    "visual_impact",
    "creative_intent_match",
    "art_direction",
)


def load_component_slugs() -> set[str]:
    """Collect canonical component slugs from the library YAML files.

    Slugs are declared explicitly rather than derived from ids, because id
    segmentation is not reliably reversible (e.g. camera.hero.low_angle.v1
    is referenced everywhere as `hero-low-angle`).
    """
    names: set[str] = set()
    for path in (REPO / "library").rglob("*.y*ml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        for component in data.get("components") or []:
            if not isinstance(component, dict):
                continue
            slug = component.get("slug")
            if isinstance(slug, str):
                names.add(slug)
    return names


def load_yaml_ids(rel: str, list_key: str, id_key: str = "id") -> set[str]:
    path = REPO / rel
    if not path.exists():
        return set()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return set()
    out: set[str] = set()
    for item in data.get(list_key) or []:
        if isinstance(item, dict) and isinstance(item.get(id_key), str):
            out.add(item[id_key])
    return out


def main() -> int:
    problems: list[str] = []

    if not CASES_DIR.exists():
        print(f"benchmark cases directory missing: {CASES_DIR}")
        return 1

    components = load_component_slugs()
    templates = {p.stem for p in (REPO / "templates").glob("*.md")}

    cases = sorted(CASES_DIR.glob("*.yaml"))
    if not cases:
        print("no benchmark cases found")
        return 1

    genres_seen: set[str] = set()
    dimensions_seen: set[str] = set()

    for path in cases:
        rel = path.relative_to(REPO).as_posix()
        data = yaml.safe_load(path.read_text(encoding="utf-8"))

        if not isinstance(data, dict):
            problems.append(f"{rel}: not a mapping")
            continue

        for field in REQUIRED_TOP:
            if field not in data:
                problems.append(f"{rel}: missing top-level '{field}'")

        meta = data.get("benchmark") or {}
        for field in REQUIRED_META:
            if field not in meta:
                problems.append(f"{rel}: benchmark missing '{field}'")
        dimensions_seen.add(str(meta.get("dimension")))

        routing = data.get("expected_routing") or {}
        genre = routing.get("genre")
        if genre:
            genres_seen.add(genre)
            if genre not in ACTION_LIMIT_BY_GENRE:
                problems.append(f"{rel}: unknown genre '{genre}'")


        template = routing.get("template")
        if template and templates and template not in templates:
            problems.append(f"{rel}: unknown template '{template}'")

        # Component existence
        for category, names in (data.get("expected_components") or {}).items():
            for name in names or []:
                if components and name not in components:
                    problems.append(
                        f"{rel}: {category} component '{name}' not found in library/"
                    )

        # Risk budget must respect genre + duration
        duration = ((data.get("input") or {}).get("session_spec") or {}).get("duration")
        budget = data.get("risk_budget") or {}
        declared_action = budget.get("max_action_level")
        if declared_action is not None and genre and duration:
            allowed = effective_action_limit(
                genre, str(duration), routing.get("rarity")
            )
            if declared_action > allowed:
                problems.append(
                    f"{rel}: max_action_level {declared_action} exceeds "
                    f"effective limit {allowed} (genre={genre}, "
                    f"duration={duration}, rarity={routing.get('rarity')})"
                )

        declared_effect = budget.get("max_effect_level")
        if declared_effect is not None and duration:
            allowed_effect = EFFECT_LIMIT_BY_DURATION.get(str(duration), 99)
            rarity = routing.get("rarity")
            if rarity == "SSR":
                allowed_effect += 1
            if declared_effect > allowed_effect:
                problems.append(
                    f"{rel}: max_effect_level {declared_effect} exceeds "
                    f"effective limit {allowed_effect} (duration={duration}, rarity={rarity})"
                )

        # ---- Multi-character (cast) assertions ----
        cast = data.get("cast") or {}
        if cast:
            members = cast.get("members") or []
            size = cast.get("size")

            if size is not None and len(members) != size:
                problems.append(
                    f"{rel}: cast.size is {size} but {len(members)} member(s) listed"
                )

            weights = [
                m.get("screen_weight")
                for m in members
                if isinstance(m, dict) and m.get("screen_weight") is not None
            ]
            if weights:
                total_weight = sum(weights)
                if total_weight != CHARACTER_BUDGET:
                    problems.append(
                        f"{rel}: screen_weight sums to {total_weight}, "
                        f"expected {CHARACTER_BUDGET}"
                    )

            by_role = {
                m.get("role"): m
                for m in members
                if isinstance(m, dict)
            }
            lead, second = by_role.get("lead"), by_role.get("second")
            if lead is None:
                problems.append(f"{rel}: cast has no 'lead' member")
            if lead and second:
                lw, sw = lead.get("screen_weight"), second.get("screen_weight")
                if isinstance(lw, (int, float)) and isinstance(sw, (int, float)):
                    if lw < sw * 1.5:
                        problems.append(
                            f"{rel}: lead weight {lw} must be >= 1.5x second {sw}"
                        )

            # anchor sides must be unique to keep composition stable
            anchors = [
                m.get("anchor_side") for m in members
                if isinstance(m, dict) and m.get("anchor_side")
            ]
            if len(anchors) != len(set(anchors)):
                problems.append(
                    f"{rel}: duplicate anchor_side; each member needs a distinct anchor"
                )

            # contrast requirement
            contrast = data.get("contrast_check") or {}
            cnt = contrast.get("count")
            if isinstance(cnt, int) and cnt < CONTRAST_DIMENSIONS_REQUIRED:
                problems.append(
                    f"{rel}: contrast_check count {cnt} below required "
                    f"{CONTRAST_DIMENSIONS_REQUIRED}"
                )

            # stability cap by cast size
            declared_cast = (data.get("benchmark") or {}).get("cast_size") or size
            cap = STABILITY_CAP_BY_CAST.get(declared_cast)
            stability = (data.get("scores") or {}).get("generation_stability")
            if cap is not None and isinstance(stability, (int, float)):
                if stability > cap:
                    problems.append(
                        f"{rel}: generation_stability {stability} exceeds cap {cap} "
                        f"for cast_size {declared_cast}"
                    )

        # Scores must add up
        scores = data.get("scores") or {}
        final = scores.get("final_score")
        parts = [scores.get(k, 0) for k in SCORE_KEYS]
        if final is not None and any(parts):
            total = sum(p for p in parts if isinstance(p, (int, float)))
            if total != final:
                problems.append(
                    f"{rel}: score components sum to {total} but final_score is {final}"
                )

    # Coverage assertions
    for required_genre in ("action", "daily", "magic"):
        if required_genre not in genres_seen:
            problems.append(f"coverage gap: no benchmark exercises genre '{required_genre}'")
    for required_dim in ("genre", "cast", "concept-sheet"):
        if required_dim not in dimensions_seen:
            problems.append(
                f"coverage gap: no benchmark declares dimension '{required_dim}'"
            )

    for item in problems:
        print(f"BENCHMARK FAIL {item}")

    print(
        f"\nvalidated {len(cases)} benchmark case(s); "
        f"genres covered: {sorted(genres_seen)}; {len(problems)} problem(s)"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
