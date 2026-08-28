#!/usr/bin/env python3
"""验证质量门槛、可安全自动修改项和不可自动猜测项。"""
from __future__ import annotations

import copy
import pathlib

from director_plan import load_plan
from quality_engine import auto_revise, evaluate_plan

REPO = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    problems = []
    base = load_plan(REPO / "examples/platform-adapters/jimeng-t2va.yaml")
    if evaluate_plan(base)["decision"] != "PASS":
        problems.append("基准方案未通过质量门槛")

    recoverable = copy.deepcopy(base)
    for item in recoverable["rhythm"]["energy_curve"]:
        item["energy"] = 75
    recoverable["rhythm"]["beat_events"] = [x for x in recoverable["rhythm"]["beat_events"] if x["time"] < 4]
    if evaluate_plan(recoverable)["decision"] != "REVISE":
        problems.append("低高潮和缺结尾事件没有触发修改")
    revised, changes = auto_revise(recoverable)
    if len(changes) != 2 or evaluate_plan(revised)["decision"] != "PASS":
        problems.append("安全自动修改没有修复高潮和结尾")

    manual = copy.deepcopy(base)
    manual["rhythm"]["micro_shots"] = [{"time": 0, "event": "开场"}, {"time": 5, "event": "结尾"}]
    manual_revised, _ = auto_revise(manual)
    if evaluate_plan(manual_revised)["decision"] != "REVISE":
        problems.append("需要创作判断的节奏空档不应被自动猜测修复")

    for problem in problems:
        print("QUALITY LOOP FAIL", problem)
    print(f"已校验通过、自动修改和人工返修三条质量路径；发现 {len(problems)} 个问题")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
