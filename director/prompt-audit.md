# Prompt Quality Audit

用于 `TASK_OPTIMIZE` —— 回答「为什么我的 H3 效果不好？」

---

## 1. 角色一致性检查

- 发型是否固定
- 服装是否固定
- 配色是否固定
- 是否存在互相冲突的描述

---

## 2. 视频可生成性检查

❌ 反例：

> 镜头绕角色 360 度旋转，同时高速推进，同时人物奔跑

✅ 修正：

> 2.5D side parallax movement, slow push-in, character runs across frame

---

## 3. AI 风险检测

自动标记：

- 3D 倾向词（PBR / render / octane / 3D CGI）
- 真人摄影词（photograph / DSLR / bokeh / film camera）
- 复杂物理动作（cloth simulation / fluid / debris）
- 超大量角色（crowd / army / group battle）
- 不可能镜头（simultaneous orbit + push-in + subject sprint）

---

## 4. 输出

在输出前追加 Rhythm Audit：

- BPM 是否被换算为事件时间点，而不只是音乐形容词
- 是否混淆 Micro-shot 与 Generation Clip
- Action 是否连续超过 1.2s 没有新事件
- 主动作是否包含 anticipation / impact / recovery
- 高潮能量是否高于开场
- 单个 Generation Clip 是否超过一个主动作 / 运镜 / 主特效

```yaml
audit_report:
  character_consistency:
    score:
    issues: []
  generation_feasibility:
    score:
    issues: []
  risk_flags: []
  rhythm_issues: []
  pv_rhythm_score:
  rewritten_prompt:
  expected_improvement:
```
