# Branch Policy

## 红线约束

> **禁止直接推送到 `main`。所有推送必须先进入 `dev`，再通过 Pull Request 合入 `main`。**

此约束同时适用于人工操作与自动化代理（包括 AI 助手）。

---

## 分支职责

| 分支 | 用途 | 可否直接推送 |
|---|---|---|
| `main` | 稳定发布版本 | ❌ **禁止**，仅通过 PR |
| `dev` | 集成开发分支，日常推送目标 | ✅ 允许 |
| `feature/*` | 功能分支 | ✅ 允许 |
| `hotfix/*` | 紧急修复 | ✅ 允许（仍需 PR 合入 main） |

---

## 标准流程

```
本地提交
   ↓
git push origin HEAD:dev
   ↓
GitHub 上开 PR：dev -> main
   ↓
CI 校验通过（12 项校验器）
   ↓
Review 后合并
```

---

## 两层强制机制

### 第 1 层：本地 pre-push hook（已随仓库提交）

`.githooks/pre-push` 会拦截任何以 `main` / `master` 为目标的推送。

**启用**（克隆后需执行一次）：

```bash
git config core.hooksPath .githooks
```

验证是否生效：

```bash
git push --dry-run origin HEAD:main   # 应被拒绝，退出码 1
git push --dry-run origin HEAD:dev    # 应通过
```

> ⚠️ **本地 hook 可被 `--no-verify` 绕过**，因此它只是「防手滑」，
> 不是真正的安全边界。真正的强制依赖第 2 层。

### 第 2 层：GitHub Branch Protection（需在仓库设置中开启）

这是唯一无法被本地绕过的强制手段。建议配置：

```
Settings → Branches → Add branch protection rule

Branch name pattern: main
  ☑ Require a pull request before merging
  ☑ Require status checks to pass before merging
      → Validate
  ☑ Do not allow bypassing the above settings
  ☐ Allow force pushes        (保持关闭)
  ☐ Allow deletions           (保持关闭)
```

或使用 gh CLI：

```bash
gh api -X PUT repos/AvalonLee/AnimePv-promt/branches/main/protection \
  -F required_pull_request_reviews.required_approving_review_count=0 \
  -F enforce_admins=true \
  -F required_status_checks.strict=true \
  -F 'required_status_checks.contexts[]=validate' \
  -F restrictions=
```

---

## 提交前自检

推送前应本地跑通全部校验器（与 CI 一致，共 12 项）：

```bash
python tools/validate_yaml.py
python tools/check_naming.py
python tools/check_version.py
python tools/validate_templates.py
python tools/validate_benchmarks.py
python tools/validate_cases.py
python tools/check_effect_first_migration.py
python tools/validate_platform_adapters.py
python tools/validate_director_plan.py examples/platform-adapters
python tools/validate_execution_kernel.py
python tools/validate_quality_loop.py
python tools/check_links.py
```

全部需返回退出码 0（见 `.github/workflows/validate.yml`）。
