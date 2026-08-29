# Character Release Director（角色展示导演器）

15 秒角色 PV 自动导演器，适用于角色展示 / 角色上线场景。

Input: 角色设定卡
Output: 8 镜快切角色展示结构

> 本文件与 v2.5.0 的 rhythm-engine（双时间尺度：micro-shot → generation clip）、
> performance-direction（表演四段）和 creative-direction（创意方向）配合使用。
> 固定节奏为纯视觉节奏方案，不替代 rhythm-planner 的 Beat Grid 生成，
> 落地时须先经 rhythm-planner 拆解为 micro-shot 再聚合为 generation clip。

---

## 固定节奏（快切默认）

```
0-1.5s    HOOK（英雄镜头 1）
1.5-3s    IDENTITY 快切
3-4.5s    DETAIL 特写
4.5-6s    PERSONALITY 蓄力
6-8s      SIGNATURE 爆发（英雄镜头 2）
8-9.5s    ACTION 多角度快切
9.5-11.5s POWER 定格（英雄镜头 3）
11.5-15s  TITLE 结尾定格
```

默认单镜 1-2s，禁止用慢速长镜头填满全片。

---

## Shot 01 — Hook（0-1.5s，英雄镜头 1）

目标：让观众第一眼记住角色。

| 角色类型 | Camera | Expression | Action |
|---|---|---|---|
| cool_female | eye-reveal | cool-gaze | head-turn |
| sweet_female | hand-to-camera | playful-wink | hand-gesture |
| fantasy | eye-reveal | elegant-smile | — |
| cyber_female | detail-macro | confident-smirk | hand-gesture |

运镜：低机位仰拍快速上摇甩镜，0.3s 内收束到贴脸。

---

## Shot 02 — Identity（1.5-3s，多角度快切）

固定调用 `beauty-showcase`。

原因：角色 PV 第一目标不是剧情，是**角色识别**。

展示顺序（每 0.5s 换一个角度）：

```
Face → Hair → Outfit → Signature Item
```

---

## Shot 03 — Detail（3-4.5s）

标志物 macro 特写，快速部分环绕 90-120°，急停定格。

---

## Shot 04 — Personality（4.5-6s）

| 角色类型 | Expression | Action |
|---|---|---|
| cool | confident-smirk | weapon-reveal |
| sweet | sweet-smile | hair-flip |
| elegant | elegant-smile | gesture |

运镜：小角度环绕 30-45° + 正常推镜（全片唯一慢速段）。

---

## Shot 05 — Signature（6-8s，英雄镜头 2）

必须体现角色独有核心卖点：

```yaml
combat: weapon-reveal
magic: ability-release
fashion: signature-pose
```

规则：不超过 1 角色 / 1 技能 / 1 特效。运镜：快速部分环绕 120-180° + 急拉微震。

---

## Shot 06 — Action（8-9.5s，多角度快切）

连续 3 角度快切（背面 → 侧面 45° → 正面贴脸），每段 0.5s，动作利落。

---

## Shot 07 — Power（9.5-11.5s，英雄镜头 3）

低机位仰拍 + 快速部分环绕 90-120° 后急停，pose 定格，气场全开。

---

## Shot 08 — Ending（11.5-15s）

所有角色固定：

```yaml
camera: hero-low-angle
action: signature-pose
transition: title-reveal
```

---

## 验收标准

- ✓ 第一秒出现角色
- ✓ 15 秒完成角色介绍
- ✓ 有能力展示
- ✓ 至少 2 个英雄镜头（Hook + 高潮或结尾）
- ✓ 多角度快切（机位角度变化 ≥ 6 次）
- ✓ 有最终记忆画面
- ✓ 角色 DNA 未变化