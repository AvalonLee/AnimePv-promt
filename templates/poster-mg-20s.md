# 20s Poster-MG / Editorial MG Character PV

Template ID: template.poster.mg.20s.v1

## Purpose

平面海报式 / Editorial MG / 剪影符号化角色 PV 的专项分镜模板，源自三份成功案例
（太刀城市 / 命运赌场 / 兔耳魔术师）的同构方法论。核心目标：用「角色相对稳定 +
背景 Graphic 高速反向运动 + 图形匹配转场」建立角色识别度与世界观绑定，而非连续动作叙事。

## Default Style

| 属性 | 值 |
|---|---|
| 内容方向 | 按角色气质和本次创作意图确定 |
| Style | editorial-mg-poster |
| Animation | modern-cel（可锚定 P0 七个 2D base style 之一，平面图层不变） |

> Animation 从 `modern-cel` / `retro-cel` / `painterly-anime` / `watercolor-ink` /
> `vector-flat` / `korean-manhwa` / `western-comic` 中选择，锚定见 [core/style-anchor.md](../core/style-anchor.md)。
> 无论选何种 base，本模板的「平面海报式」呈现层不变：所有元素须平面化 / 剪影化 / 符号化 / 图形化。

## Structure

```
LOCAL_OPEN → SILHOUETTE_REVEAL → PROFILE_WALK → MG_MONTAGE → VILLAIN_REVEAL → TITLE
```

## Shot Plan（20s 范式，蒙太奇段高密度切镜 0.3-0.8s）

| Shot | Time | Purpose | Camera | Content |
|---|---|---|---|---|
| 01 | 0-3s | Local Open（局部开场） | low-angle detail + graphic-mask wipe | 只展示下半身 / 脚步 / 靴 / 武器局部；图形向外弹开，武器划出几何轨迹 |
| 02 | 3-6s | Silhouette Reveal（剪影↔赛璐璐） | reveal-closeup（沿武器上移分面） + silhouette-mask | 黑色剪影 → 纯白剪影 → 二维赛璐璐，背景符号动态拼合 |
| 03 | 6-9s | Profile Walk（侧面平移） | profile-pan + eye-macro | 角色侧面平移，背景反向滚动；巨大图形圆环展开斜切画面；眼睛特写框 |
| 04 | 9-11s | Montage A | graphic-panel + shape-match | 扑克 / 符号掠过 → 某张膨胀为铺满画面的抽象色块 |
| 05 | 11-13s | Montage B | detail-macro + graphic-panel | 关键姿态定格，**不连续动作**；背景符号重组 / 几何切片 |
| 06 | 13-15s | Montage C | eye-macro | 眼睛特写内部嵌套世界符号图层（扑克 / 筹码 / 兔子 / 刻度组成的二维动画） |
| 07 | 15-18s | Villain Reveal（反派终场） | extreme-closeup | 反派私人二维空间终场揭示，从容危险；红色液体杯面倒映角色剪影，从帽檐阴影抬眼微笑 |
| 08 | 18-20s | Title（标题拼合） | final-pose + title-reveal | 原创标题由主题符号（时钟 / 扑克 / 兔耳 / 魔术棒 + 几何切片）拼合，下方英文副标题 |

## Component Default

Camera: reveal-closeup / beauty-showcase / hero-low-angle / detail-macro / final-pose
（平面海报式专用：profile-pan / eye-macro / extreme-closeup 见各 Shot 的 Camera 列）
Action: head-turn / signature-pose / ability-release
Transition: graphic-mask / shape-match / black-white-invert / single-frame-red-flash /
single-frame-white-flash / mirror-shatter / ui-ring
（转场一律图形匹配，禁止普通淡入淡出 / 空白过渡 / 无理由黑场）

## Hard Constraints（本模板不可妥协）

- 全片纯二维平面动画：不要 3D / 立体建模 / 三维透视 / CG 质感 / 真实空间纵深 / 景深 /
  写实光影 / 真实材质 / 连续写实打斗 / 真实摄影棚风格 / 大面积霓虹灯 / 赛博朋克写实街景
  （除非主题明确需要赛博）。
- 角色占比约 70% 且相对稳定（关键姿态定格 + 侧面平移）；背景 Graphic 高速反向滚动。
- 蒙太奇段（9-15s）关键姿态定格、不连续动作；每次鼓点 / 魔术触发 → 反相 / 单帧闪红闪白 / 几何拆解。
- 三色高反差锁定（红 = 危险 / 白 = 规则 / 黑 = 未知），红色只用于高危 / 反杀 / 情绪触发帧。
- 每主题一套固定 2D 符号原语库，重组复用；眼睛 / 手部 / 武器局部特写内部嵌套世界符号图层。
- 收口结构：反派终场揭示 + 标题图形拼合（约 15-20s）。

## Validation

- ✓ 第一秒出现角色局部（脚 / 武器）
- ✓ 20s 内完成：揭示 + 蒙太奇 + 反派终场 + 标题拼合
- ✓ 剪影↔赛璐璐切换仅在 0-6s 开场使用
- ✓ 蒙太奇段（9-15s）关键姿态定格、不连续动作；密度 8-20 切镜（avg 0.3-0.8s）
- ✓ 每次鼓点 / 魔术触发 → 反相 / 单帧闪红闪白 / 几何拆解
- ✓ 转场一律图形匹配（无淡入淡出 / 空白过渡）
- ✓ 机位角度变化 ≥ 8 次，禁止连续同机位
- ✓ 角色占比约 70% 相对稳定，背景 Graphic 高速反向运动
- ✓ 角色 DNA 未变化
