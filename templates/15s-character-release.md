# 15s 角色展示 PV 模板

Template ID: template.character.release.15s.v1

## 用途

新角色展示 / 角色 PV 的首选模板。
核心目标：建立角色记忆。

## 默认风格

| 属性 | 值 |
|---|---|
| 内容类型 | character-release |
| 风格 | mobile-game-premium |
| 动画基础 | modern-cel |

> Animation 可从 7 套 2D base style 中选择：
> `modern-cel` / `retro-cel` / `painterly-anime` / `watercolor-ink` /
> `vector-flat` / `korean-manhwa` / `western-comic`，锚定见 [core/style-anchor.md](../core/style-anchor.md)。

## 结构

```
HOOK → IDENTITY → DETAIL → PERSONALITY → SIGNATURE → ACTION → POWER → TITLE
```

## Shot Plan（快切默认，单镜 1-2s）

| Shot | Time | Purpose | Camera | Content |
|---|---|---|---|---|---|
| 01 | 0-1.5s | Hook（英雄镜头 1） | hero-low-angle + 快速上摇 | 低机位仰拍甩镜 → 贴脸特写 |
| 02 | 1.5-3s | Identity | beauty-showcase（多角度） | face → hair → outfit → signature item 快切 |
| 03 | 3-4.5s | Detail | detail-macro + 快速环绕 | 武器 / 配饰 macro 90° 环绕定格 |
| 04 | 4.5-6s | Personality | medium close + 30° 环绕 | 表情 + 动作（唯一慢速段） |
| 05 | 6-8s | Signature（英雄镜头 2） | hero-orbit + 急拉 | ability-release 或 weapon-reveal |
| 06 | 8-9.5s | Action | action-tracking（多角度） | 3 角度快切连招 / 变向 |
| 07 | 9.5-11.5s | Power（英雄镜头 3） | hero-low-angle 环绕急停 | 收招 pose 定格，气场全开 |
| 08 | 11.5-15s | Title | final-pose | character name / title / signature pose |

## 组件默认

Camera: reveal-closeup / beauty-showcase / hero-low-angle / hero-orbit / action-tracking / final-pose
Action: head-turn / signature-pose / ability-release
Transition: flash-cut / title-reveal / whip-pan

## 验证

- ✓ 第一秒出现角色
- ✓ 15 秒完成角色介绍
- ✓ 有能力展示
- ✓ 至少 2 个英雄镜头（Hook + 高潮或结尾）
- ✓ 机位角度变化 ≥ 6 次，禁止连续同机位
- ✓ 有最终记忆画面
- ✓ 角色 DNA 未变化