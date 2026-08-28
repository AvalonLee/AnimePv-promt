# Configuration Guide

**AstraForge Studio · 星铸工坊 v1.2.0**

AstraForge 使用基于 YAML 的配置。

---

## Core Configuration

```
config/
├── project.yaml
├── style.yaml
├── quality.yaml
└── benchmark.yaml
```

---

## Project Config

```yaml
project:
  name: AstraForge Studio
  name_zh: 星铸工坊
  version: 1.2.0
```

---

## Quality Config

评分权重可调整，但建议保持稳定性优先：

```yaml
quality:
  generation_stability: 35
  character_consistency: 25
  shot_feasibility: 15
  visual_impact: 10
  creative_intent_match: 10
  art_direction: 5
```

判定阈值：

```yaml
decision:
  ">=90": PASS
  "75-89": GOOD (minor optimization)
  "60-74": REVISION
  "<60": REBUILD
```

---

## Risk Limits

```yaml
limits:
  max_action_level:
    5s: 1
    15s: 2
    30s: 3
  max_effect_level:
    15s_character_pv: 2
    legendary: 3
  max_camera_transition:
    5s: 4
    10s: 6
    15s: 9
    30s: 15
```

---

## Style Config

默认 Style Stack：

```yaml
# base 可选 7 套 2D 画风：modern-cel / retro-cel / painterly-anime /
# watercolor-ink / vector-flat / korean-manhwa / western-comic
style_stack:
  base: modern-cel
  premium: mobile-game-premium
  special: null
```

画面升级规则：

```yaml
visual_upgrade:
  character_release: mobile-game-premium
  legendary_character: cinematic-lighting
  dark_character: dark-cinematic-cel
  fashion_character: y2k-graphic
```

---

## Custom Style

用户可添加自定义风格：

```
library/style/custom-style.yaml
```

添加后需在 `core/style-engine/style-conflict-rules.yaml` 中登记兼容性，
否则 Style Validation Gate 会拒绝该组合；新增 base style 还需补全
`core/style-anchor.md` 的锚定与专属禁止项。

---

## Fallback Defaults

```yaml
defaults:
  style: modern-cel
  duration: 15s
  pv_mode: 15s_release
  variation: release.standard.v1
```


