#!/usr/bin/env python3
"""评估导演方案；可执行安全自动修改并输出修改后方案。"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import yaml

from director_plan import load_plan
from quality_engine import auto_revise, evaluate_plan


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=pathlib.Path)
    parser.add_argument("--auto-revise", action="store_true")
    parser.add_argument("-o", "--output", type=pathlib.Path)
    args = parser.parse_args()
    try:
        data = load_plan(args.input)
        report = evaluate_plan(data)
        changes = []
        if args.auto_revise and report["decision"] != "PASS":
            data, changes = auto_revise(data)
            report = evaluate_plan(data)
        result = {"quality_report": report, "automatic_revisions": changes}
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
            result["revised_plan"] = str(args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if report["decision"] == "PASS" else 1
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"无法评估：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
