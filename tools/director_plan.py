#!/usr/bin/env python3
"""v2.2 统一导演方案的读取、严格校验与跨字段规则。"""
from __future__ import annotations

import pathlib
from typing import Any

import yaml

PLATFORMS = {"jimeng", "minimax_h3_official", "minimax_h3_self_hosted"}
MODES = {"T2VA", "I2VA", "L2VA", "FL2VA", "Ref2VA"}
TEXT_STRATEGIES = {"post_production", "model_generated", "none"}
CONTENT_TYPES = {"action", "daily", "magic", "story", "poster_motion", "multi_character"}
CREATIVE_DIRECTIONS = {"kinetic_peak", "emotional_closeup", "mystical_reveal", "relationship_tension", "graphic_identity"}
PRESENTATION_STRATEGIES = {"action_burst", "emotional_showcase", "ability_showcase", "relationship_interaction", "story_scene", "poster_motion"}
CAST_COUNTS = {"single": (1, 1), "duo": (2, 2), "trio": (3, 3), "squad": (4, 4)}
MATERIAL_TYPES = {"image", "video", "audio"}
ANCHORS = {"start_frame", "end_frame", "reference"}
ROOT_FIELDS = {"project", "character", "cast", "direction", "style", "performance_direction", "rhythm", "generation_clips", "editorial_manifest", "audio_beat_manifest", "materials", "target", "revision_log"}
CLIP_FIELDS = {"start", "end", "purpose", "composition", "primary_action", "camera", "main_effect", "sound", "editable_moments"}


def load_plan(path: pathlib.Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("根节点必须是对象")
    return data


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _extra(value: Any, allowed: set[str], label: str, problems: list[str]) -> None:
    if isinstance(value, dict):
        for key in value.keys() - allowed:
            problems.append(f"{label} 包含不支持字段 {key}")


def _continuous_ranges(rows: Any, duration: Any, label: str, problems: list[str], max_duration: float | None = None) -> None:
    if not isinstance(rows, list) or not rows:
        problems.append(f"{label} 至少包含一项")
        return
    cursor = 0.0
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict) or not _number(row.get("start")) or not _number(row.get("end")):
            problems.append(f"{label}[{index}] 的 start/end 必须是数字")
            continue
        start, end = float(row["start"]), float(row["end"])
        if abs(start - cursor) > 0.001:
            problems.append(f"{label}[{index}] 应从 {cursor:g} 秒开始，不能有空档或重叠")
        if end <= start:
            problems.append(f"{label}[{index}] 结束时间必须晚于开始时间")
        if max_duration is not None and end - start > max_duration + 0.001:
            problems.append(f"{label}[{index}] 时长超过 {max_duration:g} 秒上限")
        cursor = end
    if _number(duration) and abs(cursor - float(duration)) > 0.001:
        problems.append(f"{label} 结束于 {cursor:g} 秒，与总时长 {duration:g} 秒不一致")


def material_groups(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    materials = data.get("materials") or []
    return {anchor: [m for m in materials if isinstance(m, dict) and m.get("anchor") == anchor] for anchor in ANCHORS}


def validate_plan(data: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    _extra(data, ROOT_FIELDS, "根节点", problems)
    required = ROOT_FIELDS - {"revision_log"}
    for section in required:
        if section not in data:
            problems.append(f"缺少顶层字段 {section}")
    if problems:
        return problems
    for section in ("project", "character", "cast", "direction", "style", "performance_direction", "rhythm", "editorial_manifest", "audio_beat_manifest", "target"):
        if not isinstance(data[section], dict):
            problems.append(f"{section} 必须是对象")
    for section in ("generation_clips", "materials"):
        if not isinstance(data[section], list):
            problems.append(f"{section} 必须是列表")
    if problems:
        return problems

    project = data["project"]
    _extra(project, {"title", "duration", "aspect_ratio", "content_type", "creative_intent"}, "project", problems)
    for field in ("title", "aspect_ratio", "creative_intent"):
        if not _nonempty(project.get(field)):
            problems.append(f"project.{field} 必须是非空文字")
    duration = project.get("duration")
    if not _number(duration) or duration <= 0:
        problems.append("project.duration 必须是正数")
    if project.get("content_type") not in CONTENT_TYPES:
        problems.append("project.content_type 不受支持")

    character = data["character"]
    _extra(character, {"summary", "immutable_features", "allowed_variations"}, "character", problems)
    if not _nonempty(character.get("summary")):
        problems.append("character.summary 必须是非空文字")
    immutable = character.get("immutable_features")
    if not isinstance(immutable, list) or len(immutable) < 4 or any(not _nonempty(x) for x in immutable):
        problems.append("character.immutable_features 至少填写4个非空固定特征")
    elif len(set(immutable)) != len(immutable):
        problems.append("character.immutable_features 不能重复")
    if not isinstance(character.get("allowed_variations"), list):
        problems.append("character.allowed_variations 必须是列表")

    cast = data["cast"]
    _extra(cast, {"mode", "members", "relationships"}, "cast", problems)
    mode = cast.get("mode")
    members = cast.get("members")
    if mode not in CAST_COUNTS:
        problems.append("cast.mode 不受支持")
    if not isinstance(members, list):
        problems.append("cast.members 必须是列表")
    else:
        if mode in CAST_COUNTS and not (CAST_COUNTS[mode][0] <= len(members) <= CAST_COUNTS[mode][1]):
            problems.append(f"cast.mode={mode} 与成员数量不一致")
        member_ids = []
        for index, member in enumerate(members, 1):
            if not isinstance(member, dict) or not _nonempty(member.get("id")) or not _nonempty(member.get("role")):
                problems.append(f"cast.members[{index}] 必须包含非空 id 和 role")
            else:
                member_ids.append(member["id"])
        if len(member_ids) != len(set(member_ids)):
            problems.append("cast.members 的 id 不能重复")
    relationships = cast.get("relationships")
    if not isinstance(relationships, list):
        problems.append("cast.relationships 必须是列表")
    elif mode == "single" and relationships:
        problems.append("单角色方案不能声明角色关系")
    elif mode in {"duo", "trio", "squad"} and not relationships:
        problems.append("多角色方案必须声明角色关系")

    direction = data["direction"]
    _extra(direction, {"creative_direction", "secondary_direction", "presentation_strategy", "emotional_goal", "visual_focus"}, "direction", problems)
    if direction.get("creative_direction") not in CREATIVE_DIRECTIONS:
        problems.append("direction.creative_direction 不受支持")
    if direction.get("secondary_direction") not in (None, "") and direction.get("secondary_direction") not in CREATIVE_DIRECTIONS:
        problems.append("direction.secondary_direction 不受支持")
    if direction.get("presentation_strategy") not in PRESENTATION_STRATEGIES:
        problems.append("direction.presentation_strategy 不受支持")
    for field in ("emotional_goal", "visual_focus"):
        if not _nonempty(direction.get(field)):
            problems.append(f"direction.{field} 必须是非空文字")

    style = data["style"]
    _extra(style, {"base_style", "visual_approach", "enhancements", "environment", "lighting"}, "style", problems)
    for field in ("base_style", "visual_approach", "environment", "lighting"):
        if not _nonempty(style.get(field)):
            problems.append(f"style.{field} 必须是非空文字")
    if not isinstance(style.get("enhancements"), list):
        problems.append("style.enhancements 必须是列表")

    performance = data["performance_direction"]
    _extra(performance, {"baseline", "stimulus", "reaction", "recovery", "lifelike_moments"}, "performance_direction", problems)
    for field in ("baseline", "stimulus", "reaction", "recovery"):
        if not _nonempty(performance.get(field)):
            problems.append(f"performance_direction.{field} 必须是非空文字")
    moments = performance.get("lifelike_moments")
    allowed_moments = {"unfinished_action", "expression_transition", "external_interruption", "attention_shift", "motion_afterglow", "relationship_reaction"}
    if not isinstance(moments, list) or not moments:
        problems.append("performance_direction.lifelike_moments 至少包含一个生命感瞬间")
    else:
        for index, moment in enumerate(moments, 1):
            if not isinstance(moment, dict) or moment.get("type") not in allowed_moments or not _nonempty(moment.get("description")):
                problems.append(f"performance_direction.lifelike_moments[{index}] 类型或描述无效")

    rhythm = data["rhythm"]
    _extra(rhythm, {"bpm", "energy_curve", "beat_events", "micro_shots"}, "rhythm", problems)
    bpm = rhythm.get("bpm")
    if not _number(bpm) or bpm <= 0:
        problems.append("rhythm.bpm 必须是正数")
    energy = rhythm.get("energy_curve")
    _continuous_ranges(energy, duration, "rhythm.energy_curve", problems)
    if isinstance(energy, list):
        for index, item in enumerate(energy, 1):
            if not isinstance(item, dict) or not _number(item.get("energy")) or not 0 <= item.get("energy", -1) <= 100 or not _nonempty(item.get("purpose")):
                problems.append(f"rhythm.energy_curve[{index}] 需要0—100能量值和用途")
    beat_events = rhythm.get("beat_events")
    if not isinstance(beat_events, list) or len(beat_events) < 2:
        problems.append("rhythm.beat_events 至少包含2个事件")
    else:
        for index, event in enumerate(beat_events, 1):
            if not isinstance(event, dict) or not _number(event.get("time")) or not 0 <= event.get("time", -1) <= duration or not _nonempty(event.get("type")) or not _nonempty(event.get("visual")):
                problems.append(f"rhythm.beat_events[{index}] 时间或事件内容无效")
    micro = rhythm.get("micro_shots")
    if not isinstance(micro, list) or len(micro) < 2:
        problems.append("rhythm.micro_shots 至少包含2个快切事件")
    else:
        times = []
        for index, event in enumerate(micro, 1):
            if not isinstance(event, dict) or not _number(event.get("time")) or not 0 <= event.get("time", -1) <= duration or not _nonempty(event.get("event")):
                problems.append(f"rhythm.micro_shots[{index}] 时间或内容无效")
            else:
                times.append(float(event["time"]))
        if times != sorted(times) or len(times) != len(set(times)):
            problems.append("rhythm.micro_shots 时间必须递增且不能重复")

    clips = data["generation_clips"]
    _continuous_ranges(clips, duration, "generation_clips", problems, max_duration=4.0)
    for index, clip in enumerate(clips, 1):
        if not isinstance(clip, dict):
            continue
        _extra(clip, CLIP_FIELDS, f"generation_clips[{index}]", problems)
        for field in CLIP_FIELDS - {"start", "end", "editable_moments"}:
            if not isinstance(clip.get(field), str) or (field != "main_effect" and not clip.get(field).strip()):
                problems.append(f"generation_clips[{index}].{field} 必须是文字")
        moments = clip.get("editable_moments")
        if not isinstance(moments, list) or not 3 <= len(moments) <= 6:
            problems.append(f"generation_clips[{index}].editable_moments 必须有3—6个可剪辑节点")
        else:
            for moment in moments:
                if not isinstance(moment, dict) or not _number(moment.get("time")) or not _nonempty(moment.get("event")) or not clip["start"] <= moment.get("time", -1) <= clip["end"]:
                    problems.append(f"generation_clips[{index}] 包含无效可剪辑节点")

    editorial = data["editorial_manifest"]
    _extra(editorial, {"strategy", "items"}, "editorial_manifest", problems)
    strategy, items = editorial.get("strategy"), editorial.get("items")
    if strategy not in TEXT_STRATEGIES or not isinstance(items, list):
        problems.append("editorial_manifest 的文字策略或项目格式无效")
    elif strategy == "none" and items:
        problems.append("完全无文字时 editorial_manifest.items 必须为空")
    elif strategy in {"post_production", "model_generated"}:
        if not items:
            problems.append("选择文字策略后至少需要一个文字项目")
        for index, item in enumerate(items, 1):
            required_item = {"content", "start", "end", "position", "appearance", "effect"}
            if not isinstance(item, dict) or not required_item <= item.keys():
                problems.append(f"editorial_manifest.items[{index}] 信息不完整")
            elif not _number(item["start"]) or not _number(item["end"]) or not (0 <= item["start"] < item["end"] <= duration):
                problems.append(f"editorial_manifest.items[{index}] 时间超出范围")

    audio = data["audio_beat_manifest"]
    _extra(audio, {"soundscape", "music", "bpm", "events"}, "audio_beat_manifest", problems)
    if not isinstance(audio.get("soundscape"), str) or not isinstance(audio.get("music"), str):
        problems.append("audio_beat_manifest 的环境声和音乐必须是文字")
    if audio.get("bpm") != bpm:
        problems.append("audio_beat_manifest.bpm 必须与 rhythm.bpm 一致")
    audio_events = audio.get("events")
    if not isinstance(audio_events, list):
        problems.append("audio_beat_manifest.events 必须是列表")
    else:
        for index, event in enumerate(audio_events, 1):
            if not isinstance(event, dict) or not _number(event.get("time")) or not 0 <= event.get("time", -1) <= duration or not _nonempty(event.get("sound")):
                problems.append(f"audio_beat_manifest.events[{index}] 无效")

    target = data["target"]
    _extra(target, {"platform", "generation_mode", "model_version"}, "target", problems)
    platform, generation_mode = target.get("platform"), target.get("generation_mode")
    if platform not in PLATFORMS:
        problems.append("target.platform 不受支持")
    if generation_mode not in MODES:
        problems.append("target.generation_mode 不受支持")
    if not _nonempty(target.get("model_version")):
        problems.append("target.model_version 必须填写")

    materials = data["materials"]
    ids = set()
    for index, material in enumerate(materials, 1):
        allowed = {"id", "type", "anchor", "role", "retain", "ignore", "timing"}
        if not isinstance(material, dict):
            problems.append(f"materials[{index}] 必须是对象")
            continue
        _extra(material, allowed, f"materials[{index}]", problems)
        if not allowed <= material.keys():
            problems.append(f"materials[{index}] 字段不完整")
            continue
        material_id = material["id"]
        if not _nonempty(material_id) or material_id in ids:
            problems.append(f"materials[{index}] id 为空或重复")
        ids.add(material_id)
        if material["type"] not in MATERIAL_TYPES or material["anchor"] not in ANCHORS:
            problems.append(f"materials[{index}] 类型或锚点无效")
        if material["anchor"] in {"start_frame", "end_frame"} and material["type"] != "image":
            problems.append(f"materials[{index}] 首尾帧锚点必须是图片")
        retain, ignore = material["retain"], material["ignore"]
        if not isinstance(retain, list) or not retain or not isinstance(ignore, list):
            problems.append(f"materials[{index}] 保留项或排除项无效")
        elif set(retain) & set(ignore):
            problems.append(f"materials[{index}] 保留项与排除项不能重复")
        if not _nonempty(material["role"]) or not _nonempty(material["timing"]):
            problems.append(f"materials[{index}] 必须写清用途和时间")

    groups = material_groups(data)
    if generation_mode == "T2VA" and materials:
        problems.append("文生视频不能登记参考素材")
    if generation_mode == "I2VA" and (len(groups["start_frame"]) != 1 or len(materials) != 1):
        problems.append("首帧模式必须且只能登记一张 start_frame 图片")
    if generation_mode == "L2VA" and (len(groups["end_frame"]) != 1 or len(materials) != 1):
        problems.append("尾帧模式必须且只能登记一张 end_frame 图片")
    if generation_mode == "FL2VA" and (len(groups["start_frame"]) != 1 or len(groups["end_frame"]) != 1 or len(materials) != 2):
        problems.append("首尾帧模式必须且只能登记一张首帧和一张尾帧图片")
    if generation_mode == "Ref2VA":
        if len(materials) < 2 or groups["start_frame"] or groups["end_frame"]:
            problems.append("多参考模式至少登记两份 reference 素材")
        if platform and platform.startswith("minimax"):
            counts = {kind: sum(m.get("type") == kind for m in materials if isinstance(m, dict)) for kind in MATERIAL_TYPES}
            if len(materials) > 12 or counts["image"] > 9 or counts["video"] > 3 or counts["audio"] > 3:
                problems.append("H3 多参考超过总数12或图片9/视频3/音频3限制")
    if "revision_log" in data and not isinstance(data["revision_log"], list):
        problems.append("revision_log 必须是列表")
    return problems
