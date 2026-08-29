# Session Protocol (SESSION_SPEC)

## 核心原则

AnimePv-promt 采用**交互式生产流程**，不假设用户意图。
每步需要用户确认后才进入下一步。

---

## Step0 — 角色需求与风格分析

每次新会话先完成角色信息充分性校验、Character DNA 提取与角色风格方向确认。
此阶段不得强制要求视频时长与视频画幅；若用户提前提供，只记录为 provisional，不能锁定为
`SESSION_SPEC`，也不能阻塞角色设定图 Prompt 输出。

## Step1 — 角色设定与风格锁定

完成角色设定卡、Character DNA Lock、Persona / Style 方向确认后，立即输出角色设定图 Prompt。
角色图 Prompt 是独立产物，不得等待视频时长、视频比例或 PV Genre 确认。

角色设定图使用独立的 `CHARACTER_IMAGE_SPEC`：

```yaml
CHARACTER_IMAGE_SPEC:
  purpose: character-sheet
  aspect_ratio: "4:5"   # 默认建议；可按用户需要调整
```

角色图 Prompt 必须明确锁定日本动画 / 日本手游与主机 JRPG 角色设计语法，
并排除欧美卡通、美国动画、欧美漫画与 3D CGI 视觉。

## Step2 — 视频 SESSION_SPEC 确认

角色设定与角色风格完成、角色图 Prompt 已输出后，再向用户确认视频时长与画幅，记为 `SESSION_SPEC`：

```yaml
SESSION_SPEC:
  duration: 15s            # 5s / 10s / 15s / 30s / custom
  aspect_ratio: "16:9"     # 16:9 / 9:16 / 1:1 / custom
```

后续 PV 方案、分镜和视频 H3 Prompt 直接引用此值，不再重复确认。

用户未指定时给出可选示例：

| 参数 | 建议 |
|---|---|
| 时长 | 5s（视觉短片）/ 15s（标准角色PV）/ 30s（剧情PV） |
| 比例 | 16:9（横版推荐）/ 9:16（竖版短视频） |

---

## 信息充分性校验

**任何时候用户输入过少，必须先完善再继续，绝不直接产出脏结果。**

| 场景 | 处理 |
|---|---|
| Step0 角色描述过简 | 补全设定维度（发型/瞳色/服装/气质），附优化方向 |
| Step1 角色风格未定 | 给出日系动画 / 日系 JRPG 方向建议，确认后立即输出角色图 Prompt |
| Step2 时长/比例未指定 | 给出可选示例，引导确认 `SESSION_SPEC` |
| Step3 画面诉求模糊 | 先给运镜、构图、光影、节奏优化方向供选择 |

---

## Generation Gate — 生成闸门

**所有图片/视频生成必须经用户显式二次确认。**
本系统全程仅产出 Prompt 与参数，不调用任何生成能力。

---

## 输出语言

- 重写/技术章节：**英文**
- 对话、歌词、可见场景文本：保留原始语言
- 与用户的交流：始终用中文

---

## 文件按需加载（避免上下文污染）

| 阶段 | 加载文件 |
|---|---|
| 入口 | SKILL.md |
| Step0-1 角色设定与风格 | core/character-dna/ + director/character-card-template.md + library/style/persona-tags.md |
| Step1 角色图 Prompt | director/character-card-template.md + core/style-anchor.md |
| Step2 SESSION_SPEC | core/session-spec.md |
| Step3 生成视频 Prompt 前 | core/prompt-structure.md（必读） |
| Step3 主题模板 | library/genre/ 对应文件 |
| Step3 分镜脚本 | director/storyboard-4shot.md |
| Step4 H3 转换 | schema/h3-base.md 或 schema/h3-ref2va.md |
| Step4 质量检查 | core/quality-engine/ |
