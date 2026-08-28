# Style Priority Rules

当多个 Style 竞争时，优先级为：

```
角色固定特征 > 创作意图 > Base Style > 画面增强层 > 个性风格层
```

---

## 系统不做平均融合

例：角色为甜酷少女，输入 `Y2K + Dark + Cyber`。

系统不会平均融合，而是：

```yaml
primary: y2k-graphic
secondary: modern-cel
remove: dark-cinematic-cel
```

---

## Style Validation Gate

Composer 调用前必须通过验证：

```
Character Direction → Style Stack → Conflict Detection → Resolve → Composer
```

---

## Style Stack 结构

```yaml
style_stack:
  base_style:      # 负责动画表现
  premium_layer:   # 负责画面精致度
  special_layer:   # 负责角色个性
```

## Base Style 选择规则

P0 支持 7 个 2D base style（`modern-cel` / `retro-cel` / `painterly-anime` /
`watercolor-ink` / `vector-flat` / `korean-manhwa` / `western-comic`），
选择依据是**角色美术语言**，而不是主题偏好：

```
日系动画脸 → modern-cel / retro-cel / painterly-anime / watercolor-ink
韩系条漫脸 → korean-manhwa
欧美漫画脸 → western-comic
潮流海报感 → vector-flat
```

未指定时默认 `modern-cel`。base 一经选定全片锁定；
Premium / Special 层只能微调，不得覆盖 base 的线条与渲染方式。
base 的完整锚定与专属禁止项见 core/style-anchor.md。

## 自动组合规则

```yaml
style_composition:
  default_base: modern-cel
  visual_upgrade:
    clean_character_showcase: add mobile-game-premium
    dramatic_lighting:        add cinematic-lighting
    dark_atmosphere:          add dark-cinematic-cel
    graphic_fashion:          add y2k-graphic
```

---

## Style Lock

生成过程中允许 camera change / pose change，
禁止 style change（例：开始 2D cel anime，禁止中途变 realistic 3D CGI；
P0 内还禁止 2D base 中途互切：赛璐璐变厚涂 / 韩漫变美漫均不允许）。

---

## 画面风格优先级

```
Character clarity > Visual impact > Background complexity
```

