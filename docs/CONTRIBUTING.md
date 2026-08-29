# Contributing Guide

欢迎参与 AnimePv-promt 开发。

---

## 贡献方向

- Camera Components
- Action Components
- 内容类型 Templates
- Style Definitions
- Benchmark Cases
- Documentation
- Workflow Optimization

---

## Component Requirements

每个组件必须包含：

```yaml
component:
  id:
  metadata:
  usage:
  parameters:
  prompt:
  quality:
```

并且必须提供：

- YAML 定义
- Example 示例
- Test Case 测试用例

---

## Pull Request Rules

提交前请确认：

1. 已补充文档
2. 已添加 Benchmark 用例
3. 已验证质量评分
4. 已在 PR 描述中说明设计原因

---

## 分支约定

> ⚠️ **红线：禁止直接推送到 `main`。** 推送目标一律为 `dev`，经 PR 合入 `main`。
> 详见 [BRANCH_POLICY.md](BRANCH_POLICY.md)。

| 分支 | 用途 | 可否直接推送 |
|---|---|---|
| `main` | 稳定版本 | ❌ 仅通过 PR |
| `dev` | 集成开发分支 | ✅ |
| `feature/*` | 功能分支 | ✅ |
| `hotfix/*` | 紧急修复 | ✅ |

---

## 组件设计准则

1. **不直接修改核心规则** — 优先以新增模块的方式扩展能力
2. **所有组件必须可评分** — 提供 `stability_score` 与 `impact_score`
3. **风险必须显式声明** — `risk: low / medium / high`
4. **Character DNA 不可破坏** — 任何组件都不得引入换装、换发色等行为
