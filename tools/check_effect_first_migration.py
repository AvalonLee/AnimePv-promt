#!/usr/bin/env python3
"""阻止旧商业流程和字段重新进入运行时文件。"""
from __future__ import annotations
import pathlib, sys
REPO=pathlib.Path(__file__).resolve().parent.parent
SCANNED=[REPO/"SKILL.md",REPO/"README.md",REPO/"skill",REPO/"workflow",REPO/"schema",REPO/"core",REPO/"director",REPO/"library",REPO/"templates",REPO/"platform-adapters",REPO/"docs",REPO/"benchmark",REPO/"examples",REPO/"references",REPO/".github"]
FORBIDDEN=["commercial_director","commercial_goal","commercial_value","commercial_hook","theme_engine","variation_engine","event-director","gacha","advertisement","商业定位","商业价值","商业目标","广告投放","抽卡","Theme Selector","Variation Engine"]

def main():
    problems=[]; count=0
    files=[]
    for root in SCANNED:
        files += [root] if root.is_file() else list(root.rglob("*.md"))+list(root.rglob("*.yaml"))+list(root.rglob("*.py"))
    for path in files:
        count+=1; text=path.read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token not in text: continue
            problems.append(f"{path.relative_to(REPO)}: 残留 {token}")
    for p in problems: print("MIGRATION FAIL",p)
    print(f"已扫描 {count} 个运行时文件；发现 {len(problems)} 个旧商业残留")
    return 1 if problems else 0
if __name__=="__main__": raise SystemExit(main())
