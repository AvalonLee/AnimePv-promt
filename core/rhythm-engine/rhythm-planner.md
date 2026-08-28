# Rhythm Planner

在 Composer 之后、Shot Planner 之前，把“动感”编译为可执行时间结构。

## 三种时间单位

1. **Beat Event**：观众感知到的节奏刺激。可以是切镜，也可以是姿态、表情、文字、图形或闪帧变化。
2. **Micro-shot**：最终剪辑单位。Action 通常为 `0.25-0.80s`。
3. **Generation Clip**：交给视频模型的连续片段，建议 `2-4s`，只允许一个主动作、一个运镜、一个主特效。

禁止再把“15 秒 8-10 个大段”称为 Action 快切。大段只能作为生成片段；每个大段必须声明可剪辑节点。

## 工作流

1. 依据 Genre 选 BPM，计算 `beat_duration = 60 / bpm`。
2. 先画能量曲线，再安排镜头，不允许从组件库随机拼镜头后补节奏。
3. 为强拍分配事件；不要求每拍切场景，但 Action 连续 `>1.2s` 不得毫无新事件。
4. 将动作拆成 `anticipation → impact → recovery`。
5. 把 Micro-shot 聚合成 2-4 秒 Generation Clip；聚合后仍须满足 H3 单动作规则。
6. 输出 Director Package 与 Model Prompt 两层结果。

## Beat Grid 输出

```yaml
beat_grid:
  bpm: 150
  beat_duration: 0.4s
  events:
    - { time: 0.0s, strength: downbeat, type: expression_hit, content: eye_flash }
    - { time: 0.4s, strength: accent, type: hard_cut, content: weapon_macro }
    - { time: 0.8s, strength: downbeat, type: graphic_hit, content: silhouette_reveal }
```

时间必须递增并落在 SESSION_SPEC 内。事件描述只写可见变化，不写“更燃”“更有感觉”等主观词。

## Generation Clip 输出

```yaml
generation_clips:
  - id: GC01
    time: 0.0-3.0s
    primary_action: draw_sword
    camera_motion: short_push_in
    primary_effect: blade_flash
    start_pose: hand_on_hilt
    end_pose: low_angle_guard
    editable_moments:
      - { time: 0.0s, frame: eye_closeup }
      - { time: 0.6s, frame: hand_on_hilt }
      - { time: 1.2s, frame: blade_flash }
      - { time: 2.2s, frame: sword_arc }
      - { time: 2.8s, frame: final_pose }
```

## 双层交付

- **Director Package**：能量曲线、Beat Grid、Micro-shot List、Generation Clip List、剪辑/声音提示、评分。
- **Model Prompt**：一次只编译一个 Generation Clip；只保留主体锁定、起止姿态、主动作、运镜、主特效、速度、必要负向约束。

完整模板不得作为一条 15 秒 Prompt 原样投喂模型，除非目标模型已通过案例证明能稳定执行多镜头时间轴。
