#!/usr/bin/env python3
"""校验以提示词为先的案例库。"""
from __future__ import annotations
import pathlib, sys, yaml
REPO = pathlib.Path(__file__).resolve().parent.parent
RECORDS = REPO / "case-library" / "records"
INDEX = REPO / "case-library" / "index.yaml"
STATUSES = {"draft", "reviewed", "proven", "rejected"}
EVIDENCE = {"prompt_only", "user_reported", "output_observed"}

def validate_record(data: dict, rel: str) -> list[str]:
    errors = []
    if data.get("schema_version") != 3: errors.append(f"{rel}: schema_version 必须为 3")
    if not str(data.get("case_id") or "").strip(): errors.append(f"{rel}: 缺少 case_id")
    if data.get("status") not in STATUSES: errors.append(f"{rel}: status 无效")
    if data.get("evidence_level") not in EVIDENCE: errors.append(f"{rel}: evidence_level 无效")
    if not str((data.get("input") or {}).get("original_prompt") or "").strip(): errors.append(f"{rel}: 缺少 input.original_prompt")
    if not str((data.get("dedupe") or {}).get("fingerprint") or "").strip(): errors.append(f"{rel}: 缺少去重指纹")
    return errors

def main() -> int:
    problems, ids, fps = [], set(), set()
    files = sorted(RECORDS.glob("*.yaml")) if RECORDS.exists() else []
    for path in files:
        rel = path.relative_to(REPO).as_posix()
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict): problems.append(f"{rel}: 根节点必须是映射"); continue
        problems.extend(validate_record(data, rel))
        cid, fp = data.get("case_id"), (data.get("dedupe") or {}).get("fingerprint")
        if cid in ids: problems.append(f"{rel}: case_id 重复")
        if fp in fps: problems.append(f"{rel}: 原始提示词重复")
        ids.add(cid); fps.add(fp)
    index = yaml.safe_load(INDEX.read_text(encoding="utf-8")) or {}
    indexed = {x.get("case_id") for x in (index.get("case_library") or {}).get("records", []) if isinstance(x, dict)}
    if indexed != ids: problems.append("case-library/index.yaml 与 records/ 不一致")
    for problem in problems: print(f"CASE FAIL {problem}")
    print(f"\n已校验 {len(files)} 个案例；发现 {len(problems)} 个问题")
    return 1 if problems else 0

if __name__ == "__main__": sys.exit(main())
