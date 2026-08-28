# Installation Guide

**AstraForge Studio · 星铸工坊 v1.2.0**

---

## Requirements

推荐环境：

- Git
- Python 3.10+
- YAML parser
- AI 视频生成环境（如 MiniMax H3 等）

---

## Clone Repository

```bash
git clone https://github.com/AvalonLee/AstraForge-Studio.git
cd AstraForge-Studio
```

---

## 作为 AI Skill 使用

AstraForge Studio 的核心是文档与 YAML 规则集，不依赖运行时。
将仓库放入 AI Agent 的 skills 目录即可加载：

```
<agent-skills-dir>/astraforge-studio/
├── SKILL.md
└── skill/
    ├── manifest.yaml
    └── execution-flow.yaml
```

Skill 入口为根目录 `SKILL.md`。

### 加载策略

为避免上下文浪费，采用按需加载：

| 阶段 | 加载内容 |
|---|---|
| 入口 | `SKILL.md` |
| 任务判断 | `workflow/` |
| 角色分析 | `core/character-dna/` |
| 方案生成 | 匹配的 `library/` 组件 + `templates/` |
| 质量检查 | `core/quality-engine/` |

**禁止**一次性加载全部 `library/` 与 `references/`。

---

## Verify Installation

检查目录完整性：

```bash
ls SKILL.md skill/manifest.yaml docs/USER_GUIDE.md
```

运行 Benchmark 回归（如已配置工具链）：

```bash
python benchmark/run.py
```

预期输出：

```
Benchmark PASS
```

---

## 快速验证

向已加载 Skill 的 AI 发送：

```
制作一个 15 秒五星角色上线 PV。
角色：银发冰系女剑士。性格：冷静、高贵。能力：冰元素剑技。
```

预期返回 Character Bible、PV Direction、Shot List、H3 Prompt、Quality Report 五段结构化输出。
