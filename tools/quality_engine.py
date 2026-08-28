#!/usr/bin/env python3
"""效果优先质量评分与安全的结构化自动修改。"""
from __future__ import annotations

import copy
from typing import Any

from director_plan import validate_plan


def evaluate_plan(data: dict[str, Any]) -> dict[str, Any]:
    structural = validate_plan(data)
    scores = {
        "character_consistency": 0,
        "core_visual_effect": 0,
        "performance_lifelike": 0,
        "motion_camera_rhythm": 0,
        "creative_intent_match": 0,
        "ending_memory_point": 0,
    }
    issues = list(structural)
    if structural:
        return {"scores": scores, "total": 0, "hard_gates": {"structure": False, "rhythm": False, "quality": False}, "issues": issues, "decision": "REVISE"}

    immutable = data["character"]["immutable_features"]
    scores["character_consistency"] = 30 if len(immutable) >= 4 else 20
    if data["cast"]["mode"] != "single" and not data["cast"]["relationships"]:
        scores["character_consistency"] -= 10

    direction = data["direction"]
    scores["core_visual_effect"] = 20 if direction["visual_focus"] and data["style"]["visual_approach"] else 12
    performance = data.get("performance_direction") or {}
    moments = performance.get("lifelike_moments") or []
    scores["performance_lifelike"] = 5 if all(performance.get(x) for x in ("baseline", "stimulus", "reaction", "recovery")) and moments else 0
    if scores["performance_lifelike"] < 5:
        issues.append("人物表演缺少完整的事件与反应链")
    scores["creative_intent_match"] = 15 if data["project"]["creative_intent"] and direction["emotional_goal"] else 8

    rhythm = data["rhythm"]
    micro_times = [float(x["time"]) for x in rhythm["micro_shots"]]
    duration = float(data["project"]["duration"])
    gaps = [b - a for a, b in zip([0.0] + micro_times, micro_times + [duration])]
    max_gap = max(gaps) if gaps else duration
    energy = rhythm["energy_curve"]
    peak = max((x["energy"] for x in energy), default=0)
    opening = energy[0]["energy"] if energy else 0
    strategy = direction["presentation_strategy"]
    climax_required = strategy in {"action_burst", "ability_showcase"}
    rhythm_pass = max_gap <= 1.2 and (not climax_required or peak > opening)
    scores["motion_camera_rhythm"] = 20 if rhythm_pass else 10
    if max_gap > 1.2:
        issues.append(f"连续 {max_gap:.2f} 秒没有快切事件")
    if climax_required and peak <= opening:
        issues.append("动作或能力展示的高潮能量没有高于开场")

    last_clip = data["generation_clips"][-1]
    end_events = [x for x in rhythm["beat_events"] if x["time"] >= duration - min(2.0, duration * 0.3)]
    memorable = bool(end_events) and any(word in (last_clip["purpose"] + " " + last_clip["primary_action"]) for word in ("定格", "收势", "揭示", "记忆", "final", "settle", "reveal"))
    scores["ending_memory_point"] = 10 if memorable else 5
    if not memorable:
        issues.append("结尾缺少明确记忆事件或收束姿态")

    total = sum(scores.values())
    hard = {"structure": True, "rhythm": rhythm_pass, "quality": total >= 80}
    return {"scores": scores, "total": total, "hard_gates": hard, "issues": issues, "decision": "PASS" if all(hard.values()) else "REVISE"}


def auto_revise(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """只修复不改变用户创意的节奏与结尾结构；不能安全推断的内容留给人工。"""
    revised = copy.deepcopy(data)
    changes: list[str] = []
    rhythm = revised.get("rhythm") or {}
    energy = rhythm.get("energy_curve") or []
    strategy = (revised.get("direction") or {}).get("presentation_strategy")
    if energy and strategy in {"action_burst", "ability_showcase"}:
        opening = energy[0].get("energy", 0)
        peak_item = max(energy[1:] or energy, key=lambda x: x.get("energy", 0))
        if peak_item.get("energy", 0) <= opening:
            peak_item["energy"] = min(100, opening + 10)
            changes.append("提高高潮能量，使其高于开场")
    duration = (revised.get("project") or {}).get("duration")
    events = rhythm.get("beat_events") or []
    if duration and not any(x.get("time", -1) >= duration - min(2.0, duration * 0.3) for x in events):
        events.append({"time": duration, "type": "final_hit", "visual": "结尾姿态或视觉记忆点"})
        events.sort(key=lambda x: x["time"])
        changes.append("补充结尾节拍事件")
    if changes:
        revised.setdefault("revision_log", []).extend(changes)
    return revised, changes
