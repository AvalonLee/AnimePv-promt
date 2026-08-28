#!/usr/bin/env python3
"""严格校验一个或多个统一导演方案。"""
from __future__ import annotations

import argparse
import pathlib
import sys

import yaml

from director_plan import load_plan, validate_plan


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=pathlib.Path)
    args = parser.parse_args()
    files: list[pathlib.Path] = []
    for path in args.paths:
        files.extend(sorted(path.glob("*.yaml")) if path.is_dir() else [path])
    failures = 0
    for path in files:
        try:
            problems = validate_plan(load_plan(path))
        except (OSError, ValueError, yaml.YAMLError) as exc:
            problems = [str(exc)]
        if problems:
            failures += 1
            for problem in problems:
                print(f"PLAN FAIL {path}: {problem}")
        else:
            print(f"PLAN PASS {path}")
    print(f"已校验 {len(files)} 个导演方案；{failures} 个不通过")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
