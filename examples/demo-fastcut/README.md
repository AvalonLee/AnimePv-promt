# Demo — Fast-Cut Shot List（快切规则测试输出）

本文件验证 [director/shot-planner.md](../../director/shot-planner.md) 更新后的
**快切优先 / 多角度 / 镜头转动高效快速 / 英雄镜头** 规则。

输入沿用 `examples/walkthrough-frostblade`：五星冰系女剑士 Frostblade，15s。
产出按 [templates/genre-action-15s.md](../../templates/genre-action-15s.md)
快切 8 镜结构与 [library/camera/camera-motion-spec.md](../../library/camera/camera-motion-spec.md)
运镜参数。

---

## Step0 — SESSION_SPEC

```yaml
SESSION_SPEC:
  duration: 15s
  aspect_ratio: "16:9"
```

## Step1 — 输入

```
五星冰系女剑士战斗展示PV。银白长发，冰蓝瞳，黑银轻甲配深蓝披风，冰晶长剑。
气质冷静高贵。目标：手游新角色上线。15秒。
```

## Step2 — 路由

| 环节 | 结果 |
|---|---|
| Task | CREATE_PV |
| Character Type | cool_female |
| Genre | action |
| 表现方案 | combat.showcase.v1 |
| 模板 | genre-action-15s（动作节奏版） |

## Step3 — Risk Budget Gate（新转场预算）

```yaml
effective_action_budget: 2
effective_effect_budget: 2
max_camera_transition: 9     # 旧版 4 → 新版 15s 上限 9
shot_count_target: 8-10      # 快切默认
hero_shot_min: 2             # 15s 英雄镜头下限
```

---

## Step4 — Shot List（快切 8 镜 · 多角度 · 快速转动 · 英雄镜头 ×3）

| # | 时间 | 景别 / 机位 | 运镜（速度参数） | 动作 / 表情 | 转场 | 英雄镜头 |
|---:|---|---|---|---|---|---|
| 01 | 0-1.5s | 贴脸特写 / 低机位仰拍 | 快速上摇甩镜（0.3s 完成 90°） | 眼神直视镜头，披风甩动 | 闪白硬切 + 主题文字碎片 | ★ Hook |
| 02 | 1.5-3s | 正面 45° → 侧面 90° → 背面 | 三角度快切（0.5s/段） | 蓄力姿态，长发/披风翻卷 | 运动轨迹匹配 | |
| 03 | 3-4.5s | macro 特写 | 快速部分环绕 90-120°（0.5-1s）后急停 | 冰晶长剑 + 雪花吊坠细节 | 快速甩镜切出 | |
| 04 | 4.5-6s | 中景 | 30° 小角度环绕 + 0.4/s 推镜（全片唯一慢速段） | 闭眼蓄力，冰蓝能量聚集 | 人物动作轨迹匹配 | |
| 05 | 6-8s | 中景 → 全景 | 快速部分环绕 120-180°（0.5-1s）+ 急拉 + 8px 微震 0.3s | 冰元素剑技爆发，冲击波扩散 | 高光闪白硬切 | ★ 高潮 |
| 06 | 8-9.5s | 背面 → 侧面 45° → 正面贴脸 | 三角度快切（0.5s/段） | 连招变向，残影 + 速度线 | 冲击拉伸 + 快速甩镜 | |
| 07 | 9.5-11.5s | 低机位仰拍全景 | 快速部分环绕 90-120°（0.5-1s）后急停 | 收招 pose 定格，气场全开 | 图形碰撞 / 分格跳切 | ★ 力量定格 |
| 08 | 11.5-15s | 正面全景 | 固定机位定格（结尾标题卡） | 最终 pose + 标题 FROSTBLADE | title-reveal | |

**规则自检**

- ✅ 快切：单镜 1.5-2s（结尾标题卡 3.5s），8 镜 / 7 次切换 ≤ 上限 9
- ✅ 多角度：机位 8 个无重复，高潮段 3 角度快切（#02 / #06）
- ✅ 镜头转动高效快速：甩镜 #01、部分环绕 #03 / #05 / #07，无完整 360°
- ✅ 英雄镜头 3 个（Hook / 高潮 / 力量定格）≥ 15s 下限 2
- ✅ 慢速运镜仅 1 处（#04 蓄力）

---

## Step5 — 示例 H3 Prompt（Shot 05 高潮英雄镜头）

```yaml
shot: 05
duration: 2s
composition: 中景推向全景，角色居中
subjects: 银白长发冰系女剑士，冰晶长剑，黑银轻甲深蓝披风
environment: 抽象冰霜战斗空间，裂纹 + 速度线 + 冰晶碎片
actions: 释放冰元素剑技，剑气冲击波扩散，发丝披风向后甩动
camera: 快速部分环绕 120-180°（1s 内），爆发瞬间急拉 + 短时微震 8px
effect: 块状分层手绘冰晶光效，非流体
```

---

## Step6 — Quality Report（新规则口径）

```yaml
quality_report:
  scores:
    generation_stability: 32
    character_consistency: 25
    shot_feasibility: 15
    visual_impact: 10
    creative_intent_match: 10
    art_direction: 4
  final_score: 96
  decision: PASS
  risk_analysis:
    camera_risk: low        # 部分环绕/甩镜/急推列为稳定项，无完整 360°
    action_complexity: medium  # level 2，预算内
  structure_check:
    shot_count: 8           # 快切达标
    hero_shots: 3           # ≥ 2
    camera_repeat: none
    slow_motion_count: 1    # 仅蓄力段
```

## 风格 Demo 索引

| 风格 | 文件 | 核心差异 |
|---|---|---|
| 打斗（默认） | 本 README | 0.3-0.8s 高密度快切，3 英雄镜头 |
| 日常文戏 | [daily.md](daily.md) | 0.8-1.5s 轻快切，9 镜 |
| 魔法幻想 | [magic.md](magic.md) | 快慢结合：蓄力 1 处慢速 + 爆发快切 |
| 双人 | [duo.md](duo.md) | 分格降险，锚位恒定，同框 action_level 1 |
