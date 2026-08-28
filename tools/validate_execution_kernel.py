#!/usr/bin/env python3
"""检查唯一执行主链、模块路径和关键闭环没有再次断开。"""
from __future__ import annotations

import pathlib
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    problems = []
    flow = yaml.safe_load((REPO / "skill/execution-flow.yaml").read_text(encoding="utf-8"))["execution"]
    module_map = yaml.safe_load((REPO / "workflow/module-map.yaml").read_text(encoding="utf-8"))
    modules = module_map["modules"]
    if flow.get("source_of_truth") != "skill/execution-flow.yaml":
        problems.append("执行流程没有声明唯一来源")
    steps = [step for stage in flow["stages"] for step in stage["steps"]]
    missing_modules = sorted(set(steps) - set(modules))
    if missing_modules:
        problems.append("执行步骤缺模块映射：" + ", ".join(missing_modules))
    required_order = [
        "platform_selection",
        "generation_mode_selection",
        "material_registration",
        "build_director_plan",
        "director_plan_validation",
        "quality_scoring",
        "automatic_revision",
        "revised_plan_validation",
        "platform_prompt_compilation",
        "final_quality_check",
    ]
    positions = [steps.index(step) if step in steps else -1 for step in required_order]
    if positions != sorted(positions) or -1 in positions:
        problems.append("平台、完整方案、质量闭环和编译的执行顺序错误")
    for name, spec in modules.items():
        path = REPO / spec.get("path", "")
        if not path.is_file():
            problems.append(f"模块 {name} 指向不存在文件 {spec.get('path')}")
    for task, task_steps in flow["tasks"].items():
        for step in task_steps:
            if step in {stage["id"] for stage in flow["stages"]}:
                continue
            if step not in modules:
                problems.append(f"任务 {task} 引用了未知步骤 {step}")
    required_runtime = {"director_plan_validator", "quality_evaluator", "platform_compiler", "execution_kernel_validator"}
    if not required_runtime <= flow.get("runtime", {}).keys():
        problems.append("运行时缺少校验、质量或编译入口")
    schema = yaml.safe_load((REPO / "schema/director-plan.schema.yaml").read_text(encoding="utf-8"))
    required_fields = {"cast", "direction", "rhythm", "generation_clips", "editorial_manifest", "audio_beat_manifest"}
    if not required_fields <= set(schema.get("required", [])):
        problems.append("统一导演方案没有承载完整执行内核字段")
    compiler = (REPO / "tools/compile_platform_prompt.py").read_text(encoding="utf-8")
    for token in ("evaluate_plan", "auto_revise", "quality_report"):
        if token not in compiler:
            problems.append(f"平台编译器没有接入 {token}")
    for document in ("workflow/task-orchestrator.md", "workflow/production-flow.md"):
        text = (REPO / document).read_text(encoding="utf-8")
        if "skill/execution-flow.yaml" not in text:
            problems.append(f"{document} 没有引用唯一执行源")
    for problem in problems:
        print("KERNEL FAIL", problem)
    print(f"已检查 {len(steps)} 个执行步骤和 {len(modules)} 个模块映射；发现 {len(problems)} 个问题")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
