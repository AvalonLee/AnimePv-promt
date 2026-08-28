# MiniMax H3 Base 模式格式

## 适用模式

| 模式 | 说明 | 开头标注 |
|---|---|---|
| T2VA | 纯文本生成完整音视频时间线 | 无 |
| I2VA | 从首帧图向前发展 | `Starting from @image1 as first frame` |
| FL2VA | 描述首帧到末帧的连续路径 | `Path from @image1 to @image2` |
| L2VA | 推断合理开场并收敛到末帧 | `Converging to @image1 as last frame` |

## 输出字段（顺序固定，三字段不可缺省）

### 字段 1：integrated_multimodal_description

完整音视频时间线描述，按镜头/时间分段。

每个镜头必须包含**六要素**：

| 要素 | 说明 |
|---|---|
| composition | 构图/景别（全景/中景/近景/特写） |
| subjects | 主体/角色（外貌、服装、姿态） |
| environment | 环境/背景 |
| actions | 动作/表情/特效动态 |
| camera | 运镜参数（固定/推/拉/横移/环绕/震动，含速度、振幅） |
| sound | 音效/对白/环境音 |

格式：

```
integrated_multimodal_description:
[0.0s-<镜头1结束时间>] <镜头1六要素描述>
[<镜头1结束时间>-<镜头2结束时间>] <镜头2六要素描述>
...
```

所选 base style 的锚定语（见 core/style-anchor.md，默认 modern-cel）必须贯穿所有镜头，可在时间线末尾统一声明。

### 字段 2：overall_soundscape

整体音景描述（环境音、音效、对白），与时间线对应：

```
overall_soundscape:
<整体音景描述，标注关键音效出现的时间点>
```

### 字段 3：non_diegetic_music

非叙事音乐描述（BGM 风格、节奏、情绪变化、与镜头节奏的配合）：

```
non_diegetic_music:
<BGM描述，含风格、节奏变化、情绪曲线>
```

## 输出规则

1. 重写章节用**英文**；对话、歌词、可见场景文本保留原始语言
2. 时长总和必须等于 `SESSION_SPEC.duration`
3. 禁止未解析的参考标签、与请求时长不匹配的时间线
4. I2VA/FL2VA/L2VA 模式必须在开头标注参考帧关系
5. 所选 base style 的专属禁止项必须明确写出（见 core/style-anchor.md）
