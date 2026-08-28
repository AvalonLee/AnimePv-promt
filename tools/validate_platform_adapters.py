#!/usr/bin/env python3
"""验证三套平台适配器、五种编译策略和严格拒绝路径。"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
BASE = ["integrated_multimodal_description", "overall_soundscape", "non_diegetic_music"]
REF = ["subject_definitions", "summary", "retention_analysis", "detailed_description", "overall_soundscape", "non_diegetic_music"]
VALID = {
    "jimeng-t2va.yaml": "T2VA",
    "jimeng-i2va.yaml": "I2VA",
    "h3-l2va.yaml": "L2VA",
    "h3-fl2va.yaml": "FL2VA",
    "h3-ref2va.yaml": "Ref2VA",
}


def run_compiler(path: pathlib.Path):
    return subprocess.run(
        [sys.executable, str(REPO / "tools/compile_platform_prompt.py"), str(path)],
        capture_output=True,
        text=True,
    )


def main():
    problems = []
    adapters = {p.stem: yaml.safe_load(p.read_text(encoding="utf-8")) for p in (REPO / "platform-adapters").glob("*.yaml")}
    if len(adapters) != 3:
        problems.append("平台适配器必须正好为 3 个")

    outputs = {}
    for filename, expected_mode in VALID.items():
        path = REPO / "examples/platform-adapters" / filename
        run = run_compiler(path)
        if run.returncode:
            problems.append(f"{filename} 编译失败：{run.stderr.strip()}")
            continue
        out = json.loads(run.stdout)
        outputs[expected_mode] = out
        if out.get("mode") != expected_mode:
            problems.append(f"{filename} 生成方式错误")
        if out["platform"].startswith("minimax"):
            expected_fields = REF if expected_mode == "Ref2VA" else BASE
            if list(out["prompt_fields"]) != expected_fields:
                problems.append(f"{filename} H3 字段顺序错误")
        if expected_mode != "T2VA" and not out.get("material_bindings", out.get("materials")):
            problems.append(f"{filename} 缺少素材绑定")
        if expected_mode == "T2VA" and (out.get("materials") or "@图片" in json.dumps(out, ensure_ascii=False)):
            problems.append(f"{filename} 文生模式不应包含素材引用")

    expected_phrases = {
        "T2VA": "完整建立角色外观",
        "I2VA": "不要重新设计画面已有外观",
        "L2VA": "progressively converge",
        "FL2VA": "one continuous action path",
        "Ref2VA": "only for their declared retained properties",
    }
    for mode, phrase in expected_phrases.items():
        out = outputs.get(mode, {})
        body = out.get("prompt") or json.dumps(out.get("prompt_fields") or {}, ensure_ascii=False)
        if phrase not in body:
            problems.append(f"{mode} 没有执行专属编译策略")
    fl_body = json.dumps(outputs.get("FL2VA", {}).get("prompt_fields") or {}, ensure_ascii=False)
    if "At 0s align exactly with <Picture 2>; at 6s align exactly with <Picture 1>" not in fl_body:
        problems.append("FL2VA 没有按实际素材绑定识别首帧和尾帧")

    invalid_dir = REPO / "benchmark/director-plan-invalid"
    invalid_files = sorted(invalid_dir.glob("*.yaml"))
    for path in invalid_files:
        run = run_compiler(path)
        if run.returncode == 0:
            problems.append(f"{path.name} 应被拒绝但编译成功")

    for problem in problems:
        print("ADAPTER FAIL", problem)
    print(f"已校验 {len(adapters)} 个平台适配器、{len(VALID)} 种编译策略和 {len(invalid_files)} 个拒绝样例；发现 {len(problems)} 个问题")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
