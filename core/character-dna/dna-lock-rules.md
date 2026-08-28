# Character DNA Priority Rules

## 核心原则

> 角色不是一个 Prompt 描述，而是一套不可破坏的视觉资产。

---

## Priority Order

```
Face > Hair > Costume > Signature Item > Color > Personality > Action
```

---

## Lock Level System

| Level | 说明 | 范围 |
|---|---|---|
| Level 0 | 绝对禁止变化 | 发色、眼睛颜色、核心服装、标志配饰、年龄感 |
| Level 1 | 允许动态变化 | 发丝摆动、表情、姿势、光影 |
| Level 2 | 自由变化 | 背景、特效、镜头、UI 元素 |

---

## 不允许自动修改

### Face
禁止改变脸型、眼睛颜色、年龄感。

### Hair
禁止自动换发色、自动改变长度、自动增加复杂造型。

### Costume
禁止无理由换装、删除核心设计、改变主色。

### Signature Asset
禁止武器消失、标志物替换。

---

## Multi-shot Consistency Rule

连续镜头中必须保持 Character DNA 一致。
每次变化只能来自：Camera / Pose / Expression / Lighting。

---

## Character Selling Priority

角色视频 展示顺序：

```
Face → Eyes → Hair → Signature Item → Outfit → Ability
```

不要先展示背景。

---

## Failure Detection

以下情况判定角色漂移：

- ❌ 发型改变
- ❌ 服装重新设计
- ❌ 眼睛颜色变化
- ❌ 年龄感变化
- ❌ 气质变化

发现后重新调用 Character DNA。

---

## Composer 接入

任何 Shot 生成前必须读取 `character_dna`。

例：生成 `weapon-reveal`，角色为银发女剑士 →
✅ 允许原剑 / ❌ 禁止自动换枪。
