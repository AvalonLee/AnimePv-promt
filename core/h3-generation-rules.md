# H3 Generation Rules

## Core Principle

H3 不是动画制作软件。需要：简单动作、明确镜头、单一视觉重点。

H3 Prompt 的默认编译单位是 **Generation Clip**，不是整支 15 秒 PV。完整导演方案先由
`core/rhythm-engine/rhythm-planner.md` 拆成 2-4s 片段，再逐片段编译。

---

## Shot Complexity Rule

每个镜头最多：

```
1 个角色主体 + 1 个主要动作 + 1 个镜头运动 + 1 个主要特效
```

推荐结构：

```
Shot / Duration / Character / Action / Camera / Effect
```

每个片段额外声明 `start_pose / end_pose / editable_moments`。editable moments 是后期取帧与卡点提示，
不是要求模型在片段内自动完成多场景剪辑。

### Good Example

> 角色走向镜头，镜头缓慢推进，背景出现 UI。

### Bad Example

> 角色奔跑、拔剑、释放魔法、城市爆炸、天气变化、镜头 360 度旋转。

---

## Camera Rules

**Recommended**：push in / pull out / pan / zoom / 2.5D parallax

**High Risk**：360 orbit / complex tracking / realistic camera movement

---

## Motion Priority

| 级别 | 内容 |
|---|---|
| A 级 | look camera / smile / turn / hair movement / hand gesture |
| B 级 | weapon draw / power release |
| C 级 | group battle / destruction / physics simulation |

默认使用 A 级 + B 级组合。

---

## Animation Style Rule

默认 base style：modern-cel（Pure 2D Japanese anime animation with Japanese JRPG character-design language）

P0 支持 7 个 2D base style：
`modern-cel` / `retro-cel` / `painterly-anime` / `watercolor-ink` /
`vector-flat` / `korean-manhwa` / `western-comic`。

选定 base 后必须使用 [core/style-anchor.md](style-anchor.md) 中对应锚定与专属禁止项，
且**全片不可切换 base style**。

默认推荐：Japanese anime facial proportions / Japanese JRPG key visual / cel shading / hard shadow /
graphic motion / 2.5D movement / 12fps 有限动画

默认禁止：western cartoon / American animation / Disney-like / Pixar-like / DreamWorks-like /
western comic-book style / realistic photography / PBR material / 3D character rendering /
live action camera / 现代运动模糊

例外：base = `western-comic` 时禁止项反转（允许美漫风格，禁止日系/韩系混搭），
详见 core/style-anchor.md。

---

## Prompt Base 结构

Base 模式必须包含：

```
composition / subjects / environment / actions / camera / sound
```

---

## Negative Prompt 建议

```
realistic, 3D CGI, live action, PBR material,
western cartoon, American animation, Disney-like, Pixar-like, DreamWorks-like,
western comic-book style, superhero comic style, exaggerated western facial anatomy,
character drift, extra weapons, different hairstyle, different outfit
```

