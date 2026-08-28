#!/usr/bin/env python3
"""把通过严格校验的统一导演方案编译为即梦或 MiniMax H3 提示词。"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import yaml

from director_plan import load_plan, material_groups, validate_plan
from quality_engine import auto_revise, evaluate_plan

BASE_H3 = ["integrated_multimodal_description", "overall_soundscape", "non_diegetic_music"]
REF_H3 = ["subject_definitions", "summary", "retention_analysis", "detailed_description", "overall_soundscape", "non_diegetic_music"]


def timeline_text(data, english=False):
    rows = []
    for shot in data["generation_clips"]:
        prefix = f"{shot['start']:g}-{shot['end']:g}s"
        if english:
            moments = ", ".join(f"{m['time']:g}s {m['event']}" for m in shot["editable_moments"])
            rows.append(
                f"{prefix}: purpose {shot['purpose']}; composition {shot['composition']}; primary action {shot['primary_action']}; "
                f"camera {shot['camera']}; main effect {shot['main_effect']}; editable moments {moments}; sound {shot['sound']}."
            )
        else:
            moments = "、".join(f"{m['time']:g}秒{m['event']}" for m in shot["editable_moments"])
            rows.append(
                f"{prefix}：用途{shot['purpose']}；构图{shot['composition']}；主要动作{shot['primary_action']}；"
                f"镜头{shot['camera']}；主特效{shot['main_effect']}；可剪辑节点{moments}；声音{shot['sound']}。"
            )
    return "\n".join(rows)


def material_label(item, index, h3=False):
    if h3:
        kind = {"image": "Picture", "video": "Video", "audio": "Audio"}[item["type"]]
        return f"<{kind} {index}>"
    kind = {"image": "图片", "video": "视频", "audio": "音频"}[item["type"]]
    return f"{kind}{index}"


def text_instruction(data, english=False):
    text = data["editorial_manifest"]
    if text["strategy"] == "none":
        return "No visible text is required." if english else "不需要画面文字。"
    if text["strategy"] == "post_production":
        return "Reserve clean negative space; typography will be added in post-production." if english else "预留干净空间，文字由后期添加。"
    serialized = json.dumps(text["items"], ensure_ascii=False)
    return f"Generate the following visible text exactly: {serialized}" if english else f"准确生成以下画面文字：{serialized}"


def mode_strategy(data, english=False):
    mode = data["target"]["generation_mode"]
    groups = material_groups(data)
    h3 = english
    def bound_label(material):
        return material_label(material, data["materials"].index(material) + 1, h3)
    if mode == "T2VA":
        return (
            "Text-to-video: establish the complete character appearance, environment and opening composition from text before executing the timeline."
            if english else "文生视频：根据文字完整建立角色外观、环境和开场构图，再执行时间线。"
        )
    if mode == "I2VA":
        label = bound_label(groups["start_frame"][0])
        return (
            f"Image-to-video. At 0s align exactly with {label}. Do not redesign its static appearance; animate forward from the visible pose, gaze, cloth and environment."
            if english else f"首帧生成：0秒严格对齐{label}，不要重新设计画面已有外观；从可见姿态、视线、衣料和环境自然向后运动。"
        )
    if mode == "L2VA":
        label = bound_label(groups["end_frame"][0])
        duration = data["project"]["duration"]
        return (
            f"Last-frame video. Design a plausible opening and progressively converge in pose, framing, scale and lighting so the final moment at {duration:g}s aligns exactly with {label}; do not cut abruptly into it."
            if english else f"尾帧生成：设计合理开场，逐步在姿态、构图、主体大小和光影上收束，{duration:g}秒严格对齐{label}，不能突然跳到尾帧。"
        )
    if mode == "FL2VA":
        first = bound_label(groups["start_frame"][0])
        last = bound_label(groups["end_frame"][0])
        duration = data["project"]["duration"]
        return (
            f"First-last-frame video. At 0s align exactly with {first}; at {duration:g}s align exactly with {last}. Preserve identity while following one continuous action path and consistent screen direction, with no teleport, identity rebuild or abrupt camera jump."
            if english else f"首尾帧生成：0秒严格对齐{first}，{duration:g}秒严格对齐{last}；保持角色身份，以单一连续动作路径和一致画面方向完成变化，禁止瞬移、重建角色或突然跳镜。"
        )
    labels = [material_label(m, i, h3) for i, m in enumerate(data["materials"], 1)]
    return (
        f"Multi-reference video: use {', '.join(labels)} only for their declared retained properties and timing; never inherit excluded identities, costumes or environments."
        if english else f"多参考生成：按登记的保留项和使用时间调用{'、'.join(labels)}，不得继承明确排除的身份、服装或环境。"
    )


def material_notes(data, h3=False):
    notes = []
    for index, material in enumerate(data["materials"], 1):
        label = material_label(material, index, h3)
        if h3:
            notes.append(
                f"{label}: role {material['role']}; anchor {material['anchor']}; retain {', '.join(material['retain'])}; "
                f"ignore {', '.join(material['ignore']) or 'nothing additional'}; timing {material['timing']}."
            )
        else:
            notes.append(
                f"{label}：用途{material['role']}；锚点{material['anchor']}；保留{'、'.join(material['retain'])}；"
                f"排除{'、'.join(material['ignore']) or '无额外项'}；使用时间{material['timing']}。"
            )
    return notes


def compile_jimeng(data):
    project, character, style = data["project"], data["character"], data["style"]
    mode = data["target"]["generation_mode"]
    full_identity = mode == "T2VA"
    subject = character["summary"] if full_identity else "沿用锚定图片中可见的角色身份与静态外观"
    prompt = (
        f"生成方式：{mode_strategy(data)}\n"
        f"创意方向：{data['direction']['emotional_goal']}；视觉重点{data['direction']['visual_focus']}；表现策略{data['direction']['presentation_strategy']}。\n"
        f"主体与环境：{subject}；{style['environment']}。\n"
        f"节奏：{data['rhythm']['bpm']:g} BPM；能量曲线{json.dumps(data['rhythm']['energy_curve'], ensure_ascii=False)}。\n"
        f"时间线动作：\n{timeline_text(data)}\n"
        "镜头与节奏：每个片段只执行一个主要动作、一个主要运镜和一个主特效，严格按时间连续推进。\n"
        f"光影与风格：{style['base_style']} + {style['visual_approach']}；{style['lighting']}。\n"
        f"声音：{data['audio_beat_manifest']['soundscape']}；音乐{data['audio_beat_manifest']['music']}；卡点{json.dumps(data['audio_beat_manifest']['events'], ensure_ascii=False)}。\n"
        f"文字：{text_instruction(data)}\n"
        f"一致性要求：固定{'、'.join(character['immutable_features'])}。"
    )
    reminder = (
        "文生视频无需上传或引用参考素材。"
        if mode == "T2VA"
        else "请按当前即梦界面的素材选择器关联素材；仅当界面实际显示时使用 @图片1 等标签，并核对上传顺序。"
    )
    return {
        "platform": "jimeng",
        "mode": mode,
        "prompt": prompt,
        "materials": material_notes(data),
        "reminder": reminder,
    }


def compile_h3(data, self_hosted=False):
    project, character, style = data["project"], data["character"], data["style"]
    mode = data["target"]["generation_mode"]
    identity = character["summary"] if mode == "T2VA" else "Preserve the anchored character appearance without redesign."
    detailed = (
        f"{project['duration']:g}s, {project['aspect_ratio']}. {mode_strategy(data, True)} "
        f"Character: {identity} Immutable identity: {', '.join(character['immutable_features'])}. "
        f"Creative direction: {data['direction']['emotional_goal']}; visual focus {data['direction']['visual_focus']}; strategy {data['direction']['presentation_strategy']}. "
        f"Environment: {style['environment']}. Style and lighting: {style['base_style']} + {style['visual_approach']}; {style['lighting']}. "
        f"Rhythm: {data['rhythm']['bpm']:g} BPM; energy curve {json.dumps(data['rhythm']['energy_curve'], ensure_ascii=False)}. "
        f"Text policy: {text_instruction(data, True)} Timeline:\n{timeline_text(data, True)}"
    )
    sound = data["audio_beat_manifest"]
    if mode == "Ref2VA":
        notes = material_notes(data, True)
        fields = {
            "subject_definitions": "\n".join(f"{material_label(m, i, True)}: {m['role']}." for i, m in enumerate(data["materials"], 1)),
            "summary": project["creative_intent"],
            "retention_analysis": "\n".join(notes),
            "detailed_description": detailed,
            "overall_soundscape": sound["soundscape"] + "; timed events " + json.dumps(sound["events"], ensure_ascii=False),
            "non_diegetic_music": sound["music"],
        }
    else:
        fields = {
            "integrated_multimodal_description": detailed,
            "overall_soundscape": sound["soundscape"] + "; timed events " + json.dumps(sound["events"], ensure_ascii=False),
            "non_diegetic_music": sound["music"],
        }
    result = {
        "platform": "minimax_h3_self_hosted" if self_hosted else "minimax_h3_official",
        "mode": mode,
        "prompt_fields": fields,
        "material_bindings": [
            {"label": material_label(m, i, True), "id": m["id"], "type": m["type"], "anchor": m["anchor"]}
            for i, m in enumerate(data["materials"], 1)
        ],
        "reminder": "H3 标签必须与实际素材绑定一致；提示词标签不是本地文件路径。",
    }
    if self_hosted:
        result["checkpoint"] = "H3-Base-Ref2VA" if mode == "Ref2VA" else "H3-Base-FL2VA"
        result["inference_parameters"] = {"status": "需要用户提供部署接口或请求示例后填写"}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=pathlib.Path)
    parser.add_argument("-o", "--output", type=pathlib.Path)
    args = parser.parse_args()
    try:
        data = load_plan(args.input)
        problems = validate_plan(data)
        if problems:
            raise ValueError("；".join(problems))
        quality = evaluate_plan(data)
        revisions = []
        if quality["decision"] != "PASS":
            data, revisions = auto_revise(data)
            quality = evaluate_plan(data)
        if quality["decision"] != "PASS":
            raise ValueError("质量门槛未通过：" + "；".join(quality["issues"]))
        platform = data["target"]["platform"]
        result = compile_jimeng(data) if platform == "jimeng" else compile_h3(data, platform == "minimax_h3_self_hosted")
        result["quality_report"] = quality
        result["automatic_revisions"] = revisions
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"无法编译：{exc}", file=sys.stderr)
        return 1
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
