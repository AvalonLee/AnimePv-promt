# Shot Planner

将 Composer 的决策落为可执行的镜头表。

---

## Shot 字段

```yaml
- id:
  time:
  purpose:
  character_state:
  camera:
  action:
  expression:
  effect:
  transition:
  performance_state:
  camera_motivation:
  environment_interaction:
  effect_area:
  protected_area:
  risk_level:
```

---

## 编排规则

1. **One Shot One Purpose** — 一个镜头只完成一个主要任务
2. **双时间尺度** — 先按 `core/rhythm-engine/rhythm-planner.md` 生成 Micro-shot，
   再聚合为 Generation Clip。Action 15s 使用 16-28 个 Micro-shot（0.25-0.80s）与
   4-6 个 Generation Clip（2-4s）；禁止把 Generation Clip 数量误当成最终切镜数。
3. **多角度强制** — 连续两个镜头禁止同机位 / 同景别 / 同角度；
   每段动作高潮至少 3 个不同角度快切（正面 / 侧面 / 背面 / 45° / 俯拍 / 仰拍 / 鱼眼 / 荷兰角）
4. **镜头转动高效快速** — 优先快速甩镜、快速部分环绕（90-180°）、急推 / 急拉、
   快切多角度；慢速环绕仅用于蓄力铺垫且不超过 30-45°
5. **英雄镜头配额** — 15s 至少 2 个英雄镜头（开场 Hook / 高潮或结尾定格），
   30s 至少 3 个（开场 / 高潮 / 结尾）；英雄镜头使用低机位仰拍 + 快速部分环绕，
   优先调用 `hero-low-angle` / `hero-orbit` / `final-pose`
6. 同一 Shot 只保留一个高风险动作
7. 每个角色出现时改变镜头高度 / 方向 / 姿态 / 手势，避免站桩
8. 角色展示优先于背景与特效
9. **动作相位** — Action 主动作必须显式拆为 anticipation / impact / recovery，
   三个相位可跨 Micro-shot，但单个 Generation Clip 仍只保留一个主动作
10. **可剪辑节点** — 每个 Generation Clip 声明 3-6 个 editable_moments，供后期卡点；
    连续超过 1.2s 无新事件必须返修

---

## 风险标注

每个 Shot 必须给出 `risk_level: low / medium / high`。
若单个 Shot 为 high，进入 Auto Revision。

## 生命感补充规则（v2.5）

11. **人物先于镜头** — 每个主要角色镜头先声明具体行为、注意对象/刺激、手部任务、身体重心、表情变化，再决定机位。
12. **镜头有理由** — 推近、跟随、遮挡、低机位和快速移动必须说明拍摄目的与退出条件。
13. **环境参与表演** — 至少一种环境元素触发或反馈角色动作；优先把环境变化同时用作节拍或切点。
14. **偶然瞬间** — 15秒视频优先包含未完成动作/表情转换、外界反应、动作余韵各至少一次。
15. **镜头差异矩阵** — 相邻 Generation Clip 在行为、景别、机位、前景、光线、色彩、主效果、情绪中至少三项不同。
16. **效果作用区域** — 每片段一个主效果，可加一个轻辅助效果；必须保护核心五官、发型身份轮廓、标志配饰和武器识别结构。
