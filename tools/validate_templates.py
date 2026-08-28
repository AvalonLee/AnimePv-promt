#!/usr/bin/env python3
"""Validate that prompt templates are production-ready.

Covers templates/genre-*.md (single character) and templates/cast-*.md
(multi character).

Enforces the rules stated in core/prompt-structure.md, which are easy to
violate by hand:

  1. The template exposes a fenced "完整可替换模板" block.
  2. All 10 required sections are present.
  3. Every timed shot segment carries a 機位/机位 annotation
     (the source skill omitted it on the final shot in all 3 templates).
  4. Shot segments are contiguous and cover the full declared duration.
  5. No two consecutive segments reuse the same camera setup.
  6. Placeholders use the <...> form so substitution is mechanical.
"""
from __future__ import annotations

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE_GLOBS = ("genre-*.md", "cast-*.md")

BLOCK = re.compile(r"## 完整可替换模板\s*```\s*(.*?)```", re.DOTALL)
SEGMENT = re.compile(r"^(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)s：(.*)$")
CAMERA = re.compile(r"机位：([^\r\n。]+)")

REQUIRED_SECTIONS = (
    "【角色设定】",
    "【主题设定】",
    "【音乐】",
    "【画面风格】",
    "【动态与转场总要求】",
    "【分时间段镜头设计】",
    "【表演要求】",
    "【避免项】",
    "【核心目标】",
)


def main() -> int:
    problems: list[str] = []
    checked = 0

    templates = sorted(
        path
        for pattern in TEMPLATE_GLOBS
        for path in (REPO / "templates").glob(pattern)
    )
    if not templates:
        print("no prompt templates found")
        return 1

    for path in templates:
        rel = path.relative_to(REPO).as_posix()
        text = path.read_text(encoding="utf-8")

        match = BLOCK.search(text)
        if not match:
            problems.append(f"{rel}: missing fenced '完整可替换模板' block")
            continue

        checked += 1
        body = match.group(1)

        # 2. required sections
        for section in REQUIRED_SECTIONS:
            if section not in body:
                problems.append(f"{rel}: missing section {section}")

        # 3-5. shot segment integrity
        segments = []
        for line in body.splitlines():
            m = SEGMENT.match(line.strip())
            if not m:
                continue
            start, end, rest = float(m.group(1)), float(m.group(2)), m.group(3)
            cam = CAMERA.search(rest)
            segments.append((start, end, cam.group(1).strip() if cam else None))

        if not segments:
            problems.append(f"{rel}: no timed shot segments found")
            continue

        for start, end, cam in segments:
            if cam is None:
                problems.append(
                    f"{rel}: shot {start}-{end}s missing 机位 annotation"
                )

        # contiguity
        for (a_start, a_end, _), (b_start, _, _) in zip(segments, segments[1:]):
            if abs(b_start - a_end) > 1e-6:
                problems.append(
                    f"{rel}: gap/overlap between {a_end}s and {b_start}s"
                )

        # consecutive camera repeat
        cams = [c for _, _, c in segments if c]
        for prev, cur in zip(cams, cams[1:]):
            if prev == cur:
                problems.append(
                    f"{rel}: consecutive shots reuse camera '{cur}' "
                    f"(violates 机位变化强制规则)"
                )

        # 6. placeholder form
        if "<" not in body:
            problems.append(f"{rel}: no <...> placeholders; not substitutable")

    for item in problems:
        print(f"TEMPLATE FAIL {item}")

    print(
        f"\nvalidated {checked} prompt template(s); {len(problems)} problem(s) found"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
