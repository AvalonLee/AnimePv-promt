#!/usr/bin/env python3
"""摄取一条以原始提示词为唯一必填项的案例。"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import pathlib
import re
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
RECORDS = REPO / "case-library" / "records"
INDEX = REPO / "case-library" / "index.yaml"


def slugify(value: str) -> str:
    value = value.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")[:72]


def normalize(raw: dict) -> dict:
    input_data = raw.setdefault("input", {})
    prompt = str(input_data.get("original_prompt") or "").strip()
    if not prompt:
        raise ValueError("唯一必填项 input.original_prompt 不能为空")

    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    case_id = slugify(str(raw.get("case_id") or raw.get("title") or f"case-{digest[:10]}"))
    raw["schema_version"] = 3
    raw["case_id"] = case_id
    raw.setdefault("title", f"提示词案例 {digest[:8]}")
    raw.setdefault("status", "reviewed" if raw.get("user_claimed_success") else "draft")
    raw.setdefault("review", {}).setdefault("analyzed_at", dt.date.today().isoformat())

    observed = raw.get("observed_output") or {}
    report = raw.get("user_report") or {}
    if observed.get("video_ref") or observed.get("analysis"):
        evidence = "output_observed"
    elif report:
        evidence = "user_reported"
    else:
        evidence = "prompt_only"
    raw["evidence_level"] = evidence
    raw.setdefault("reusable_patterns", {}).setdefault("validation_state", "待验证" if evidence == "prompt_only" else "有补充证据")
    raw.setdefault("dedupe", {})["fingerprint"] = digest[:16]
    raw["dedupe"].setdefault("related_cases", [])
    return raw


def validate(data: dict) -> list[str]:
    problems = []
    if not str((data.get("input") or {}).get("original_prompt") or "").strip():
        problems.append("缺少 input.original_prompt")
    if data.get("evidence_level") not in {"prompt_only", "user_reported", "output_observed"}:
        problems.append("evidence_level 无效")
    if data.get("status") not in {"draft", "reviewed", "proven", "rejected"}:
        problems.append("status 无效")
    return problems


def rebuild_index() -> None:
    records = []
    for path in sorted(RECORDS.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        records.append({
            "case_id": data.get("case_id"), "title": data.get("title"),
            "status": data.get("status"), "evidence_level": data.get("evidence_level"),
            "platform": (data.get("applicability") or {}).get("platform"),
            "model_version": (data.get("applicability") or {}).get("model_version"),
            "generation_mode": (data.get("applicability") or {}).get("generation_mode"),
            "content_type": (data.get("applicability") or {}).get("content_type"),
            "path": path.relative_to(REPO).as_posix(),
            "fingerprint": (data.get("dedupe") or {}).get("fingerprint"),
        })
    INDEX.write_text(yaml.safe_dump({"case_library": {"schema_version": 3, "records": records}}, allow_unicode=True, sort_keys=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=pathlib.Path)
    parser.add_argument("--title")
    parser.add_argument("--content-type")
    parser.add_argument("--platform")
    parser.add_argument("--generation-mode")
    parser.add_argument("--claimed-success", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    source_text = args.input.read_text(encoding="utf-8")
    if args.input.suffix.lower() == ".txt":
        raw = {"input": {"original_prompt": source_text}}
        if args.title: raw["title"] = args.title
        if args.claimed_success: raw["user_claimed_success"] = True
        applicability = {}
        if args.content_type: applicability["content_type"] = args.content_type
        if args.platform: applicability["platform"] = args.platform
        if args.generation_mode: applicability["generation_mode"] = args.generation_mode
        if applicability: raw["applicability"] = applicability
    else:
        raw = yaml.safe_load(source_text)
    if not isinstance(raw, dict):
        print("输入根节点必须是映射")
        return 1
    try:
        data = normalize(raw)
    except ValueError as exc:
        print(exc)
        return 1
    problems = validate(data)
    if problems:
        print("\n".join(problems))
        return 1
    if args.validate_only:
        print(f"案例有效：{data['case_id']}（{data['evidence_level']}）")
        return 0
    RECORDS.mkdir(parents=True, exist_ok=True)
    target = RECORDS / f"{data['case_id']}.yaml"
    known = {((yaml.safe_load(p.read_text(encoding='utf-8')) or {}).get('dedupe') or {}).get('fingerprint') for p in RECORDS.glob('*.yaml')}
    if data["dedupe"]["fingerprint"] in known:
        print("检测到重复原始提示词")
        return 1
    if target.exists():
        print("案例编号已存在")
        return 1
    target.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    rebuild_index()
    print(f"已入库 {target.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
