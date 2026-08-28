# MiniMax H3 Ref2VA 全参考模式格式

## 适用场景

用户提供多张参考图、参考视频或参考音频，需要基于多参考素材生成视频。
为每个参考素材分配唯一标签，在所有章节中保持一致。

## 输出字段（顺序固定，六字段不可缺省）

### 字段 1：subject_definitions

为每个参考素材分配标签并定义：

```
subject_definitions:
- @image1: <首帧/角色参考图描述>
- @image2: <其他参考图描述>
- @video1: <参考视频描述（如有）>
- @audio1: <参考音频描述（如有）>
```

标签规则：

- 图片用 `@imageN`，视频用 `@videoN`，音频用 `@audioN`
- 编号从 1 开始，按素材类型独立编号
- 标签在所有六个字段中保持一致，禁止中途改名

### 字段 2：summary

整体内容摘要，1-2 句话概括 PV 主题与叙事弧：

```
summary:
<整体摘要>
```

### 字段 3：retention_analysis

保留分析，明确哪些参考元素必须保留、哪些可调整：

```
retention_analysis:
- Must retain: <必须保留的参考元素，如角色外貌、服装、特定pose>
- May adjust: <可调整元素，如背景、光影、运镜细节>
- Style constraint: All outputs must maintain the selected 2D base style
  (default modern-cel: cel shading, clean outlines, flat color blocks,
  hard-edged shadows, 12fps limited animation;
  see core/style-anchor.md for painterly / watercolor / vector /
  manhwa / western-comic anchors and their forbidden lists)
```

### 字段 4：detailed_description

详细时间线描述，结构同 Base 模式的 `integrated_multimodal_description`，
但需标注参考标签出现的精确时间点。

每个镜头必须包含六要素：composition / subjects / environment / actions / camera / sound

所选 base style 的锚定语必须贯穿（默认 modern-cel；见 core/style-anchor.md）。

### 字段 5：overall_soundscape

整体音景描述，标注 `@audio1` 等参考音频出现的时间点。

### 字段 6：non_diegetic_music

非叙事音乐描述。

## 输出规则

1. 重写章节用英文；对话、歌词、可见场景文本保留原始语言
2. 参考标签在所有六个字段中保持一致，禁止未解析的标签
3. 时长总和必须等于 `SESSION_SPEC.duration`
4. 每个镜头按六要素描述
5. 标注参考内容出现的精确时间点
6. retention_analysis 中必须包含 Style constraint
