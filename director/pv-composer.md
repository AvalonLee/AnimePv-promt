# AstraForge Composer

核心导演模块，负责生成 Shot / Camera / Action / Expression / Transition。

---

## 导演链

```
角色固定特征 → 创作意图 → 内容类型 → 风格组合
→ 风格检查 → 导演编排 → 节奏规划 → 分镜规划 → 平台编译
```

任何 Shot 生成前必须读取 `character_dna`。

---

## Component 自动选择算法

```
组件得分 = 角色适配 + 创作意图适配 + 画面效果 - 生成风险
```

示例（银发女剑士）：

| 组件 | 角色适配 | 意图适配 | 画面效果 | 风险 | 总分 | 结果 |
|---|---:|---:|---:|---:|---:|---|
| weapon-reveal | 10 | 10 | 10 | -2 | **28** | 选择 |
| 普通挥剑 | 7 | 5 | 6 | -5 | 13 | 舍弃 |

---

## Quality Feedback Loop

```
Composer → Shot Plan → Quality Check → Risk Analyzer → Revision → Final Shot Plan
```

### 自动修正示例

输入：黑暗魔女能力爆发展示

初版：

```yaml
action: huge magic explosion
camera: 360 rotation
effect: level 4
```

检测：action=high / camera=high / effect=critical

自动修正：

```yaml
action: controlled magic
camera: hero low angle
effect: purple energy particles (level 2)
```

风险：HIGH → LOW

---

## 最终输出模板

1. 角色方向 — 角色定位、视觉重点与创作意图
2. 风格方向 — 基础风格、增强层与特殊表现
3. 节奏方案 — 能量曲线、节拍表、快切小镜头与独立生成片段
4. 分镜方案 — 镜头、时间、运镜、动作与作用
5. 平台提示词包 — 每个独立生成片段按目标平台编译
6. 质量报告 — 一致性、观看节奏、风险与修改建议
