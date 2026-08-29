# AnimePv-promt Benchmark Suite

每次重大更新都必须通过回归验证：

```
Skill Update → Benchmark → Quality Check → Regression Test → Release
```

---

## 用例文件

每个用例以机器可校验的 YAML 形式存放于 `benchmark/test-cases/`：

```
benchmark/test-cases/
├── bm-01-sweet-y2k.yaml
├── bm-02-cool-warrior.yaml
├── bm-03-dark-witch.yaml
├── bm-04-male-knight-action.yaml       ← 首个男性角色 + Genre=action
├── bm-05-academy-daily.yaml            ← Genre=daily
├── bm-06-magic-girl-transform.yaml     ← Genre=magic + 风险预算压测
├── bm-07-duo-rival.yaml                ← 首个多角色（duo）
├── bm-08-anniversary-trio.yaml         ← 首个活动 PV（trio + 周年）
├── bm-09-male-suit.yaml                ← 男性西装 内容类型
└── bm-10-male-samurai.yaml             ← 男性武士 内容类型
```

字段约定：

| 字段 | 用途 |
|---|---|
| `input` | 原始请求 + SESSION_SPEC |
| `expected_routing` | 断言 Router 判定结果（task/genre/theme/variation/style_stack） |
| `genre_params_asserted` | 断言 Genre 可量化参数被正确应用 |
| `expected_components` | 断言组件选择 |
| `risk_budget` | 断言风险预算上限 |
| `scores` | 六维评分与判定 |
| `issues_found` | 该用例暴露的问题及修复位置 |
| `cast` | 多角色阵容（成员/权重/关系/锚位） |
| `contrast_check` | 阵容成员对比度校验 |
| `cast_risk_assertions` | 同框动作等级放大与身份串味风险 |
| `event_assertions` | 活动 PV 的 结尾信息 与情绪曲线 |

校验：`python tools/validate_benchmarks.py`

---

## 测试链路

每个用例需完整走通：

```
Task Orchestrator → Character Analyzer → Reference Retrieval
→ 内容类型选择器 → Component Selector → Shot Planner
→ H3 Risk Check → Quality Check
```

每一步单独打分，汇总为 100 分制。

---

## 当前用例

| # | 用例 | 维度 | Genre | 角色方向 | 状态 | 分数 | 暴露的问题 |
|---:|---|---|---|---|---|---:|---|
| 01 | Sweet Y2K Girl | 内容类型 | daily | 甜系 / 时尚 | ✅ PASS | 98 | 动作冲突 -> sweet_character_motion_limit |
| 02 | Cool Warrior | 内容类型 | action | 冷艳 / 战斗 | ✅ PASS | 96 | 稳定性权重下调 |
| 03 | Dark Witch | 内容类型 | magic | 幻想 / 黑暗魔女 | ✅ PASS | 94 | 特效过载 -> auto_revision |
| 04 | Male Knight Combat | **Genre+性别** | action | 男角色 / 战斗 | ✅ PASS | 91 | Expression 性别硬编码 -> 已修复 |
| 05 | Academy Tsundere Daily | **Genre** | daily | 学院 / 日常 | ✅ PASS | 98 | 技术验证：角色稳定+背景高速运动 |
| 06 | Magic Girl Transform | **Genre** | magic | 魔法 / 变身 | ✅ PASS | 92 | Transform 超限 -> Risk Budget Gate 已修复 |
| 07 | Duo Rival Showcase | **Cast** | action | 双人 / 宿敌 | ✅ PASS | 90 | 同框动作等级放大 |
| 08 | Anniversary Trio | **Event** | daily | 三人 / 周年 | ✅ GOOD | 84 | 3 人同框逼近上限 |
| 09 | Male Suit Elegance | 内容类型 | daily | 男装 / 成熟 | ✅ PASS | 97 | 男性角色类型 覆盖 |
| 10 | Male Samurai Combat | 内容类型 | action | 武士 / 热血 | ✅ PASS | 93 | 男性角色类型 覆盖 |

> 加入生成稳定性权重后，战斗与魔法角色分数下调 —— 视觉强但生成风险更高。

---

## 覆盖情况

| 方向 | 覆盖用例 | 状态 |
|---|---|---|
| **Genre 维度** | | |
| 打斗 Action | BM-02, BM-04, BM-10 | ✅ |
| 日常文戏 Daily | BM-01, BM-05, BM-09 | ✅ |
| 魔法幻想 Magic | BM-03, BM-06 | ✅ |
| **内容类型 维度** | | |
| 甜系 | BM-01 | ✅ |
| 冷艳 | BM-02 | ✅ |
| 幻想 | BM-03 | ✅ |
| 学院 | BM-05 | ✅ |
| 男装 | BM-09 | ✅ |
| 武士 | BM-10 | ✅ |
| 骑士 | BM-04 | ✅ |
| **性别维度** | | |
| 女性 | BM-01, BM-02, BM-03, BM-05, BM-06 | ✅ |
| 男性 | BM-04, BM-09, BM-10 | ✅ |
| **阵容维度** | | |
| 单角色 | BM-01..06 | ✅ |
| 双人 duo | BM-07 | ✅ |
| 三人 trio | BM-08 | ✅ |
| 四人 squad | — | ⬜ v1.2（仅 30s） |
| **活动维度** | | |
| 周年 anniversary | BM-08 | ✅ |
| 联动 collaboration | — | ⬜ v1.2 |
| 季节 seasonal | — | ⬜ v1.2 |

当前评分：**93 / 100**（10 例覆盖 3 Genre × 2 性别 × 3 阵容 × 1 活动类型，
含男性西装 / 武士 / 骑士 内容类型）

---

## Benchmark 发现并固化的规则

### Issue-01 — 甜系角色动作冲突

甜妹类角色容易叠加 wink + 手伸镜头 + hair flip + 转身，导致手部异常。

```yaml
sweet_character_motion_limit:
  per_shot:
    max: 1 charm_action + 1 expression_change
```

---

### Issue-02 — Y2K 视觉过载

```yaml
y2k_balance_rule:
  character_priority: 70%
  graphic_element: 30%
```

---

---

### Issue-03 — Expression 库 prompt_block 硬编码女性（已修复，固定于 BM-04）

8/9 个表情组件的 prompt_block 写死 "anime female character"。
修复：新增 `gender_neutral_prompt_block` 字段 + 三个男性向表情组件。
Composer 须依 `character_dna` 中的性别信息择一注入。

---

### Issue-04 — 缺少男性向表情组件（已修复，固定于 BM-04）

已新增 `composed-gaze` / `battle-resolve` / `detached-stare` 三个组件。

---

### Issue-05 — 内容方案推荐动作超出 Genre 动作等级上限（P0，已修复，固定于 BM-06）

`theme.magic-girl` 推荐 `transformation`（action_level 3），但 genre=magic 的 max_action_level 为 2。
修复：新增 `core/quality-engine/risk-budget-gate.yaml`，内容方案推荐仅为候选，
必须经 Genre/时长上限过滤后才可进入 Shot Plan。

---

### Issue-06 — transformation 与 Character DNA Lock 语义冲突（P1，已修复，固定于 BM-06）

DNA Lock 将 costume_change 列为 critical 禁止项，变身动作本质是换装。
修复：`forbidden-changes.yaml` 增加 `transformation_exception`，
变身前后的核心 DNA（脸/发色/眼色/标志物）必须一致，且必须在同一 Shot 内完成。

---

---

### Issue-07 — 组件短名无法从 id 反推（已修复）

`camera.hero.low_angle.v1` 在全项目 14+ 处被引用为 `hero-low-angle`，
但从 id 机械反推得到 `hero-low_angle`，导致引用校验全面误报。
同类问题：`camera.hand.camera.v1` → 实际引用 `hand-to-camera`；
`expression.shy.v1` → 实际引用 `shy-expression`。

修复：为全部 52 个组件增加显式 `slug` 字段作为唯一规范短名，
`validate_yaml.py` 强制其存在且全局唯一，引用校验一律基于 slug。

---

### Issue-08 — Genre 动作等级上限与自身模板矛盾（已修复）

引入 Genre 层时把 `daily` 的 `max_action_level` 定为 1，但
`templates/genre-daily-15s.md` 自身含「漫步」「转身」，即 `confident-walk`（level 2）。
同时 `magic` 上限为 2，使 `transformation`（level 3）的准入条件
（30s + SSR + magic）永远无法满足 —— 规则写了但不可达。

修复：
- `daily` 上限修正为 2
- 引入 `genre_ceiling_uplift`：genre 上限为**基线**，
  `magic + 30s + SSR` 与 `action + 30s` 可提升至 3
- 三处定义（risk-budget-gate / genre-library / execution-flow）同步对齐

---

### Issue-09 — 被引用但未定义的组件（已修复）

`environment-reveal`（story-director、variation-library、examples 引用）与
`ability-preparation`（dark-witch theme、examples 引用）从未在库中定义。

修复：补充两个组件定义。`ability-preparation` 作为 `ability-release` 的
低风险前置动作（action_level 1），使 Genre=magic 的「快慢结合」
可以在不提高动作等级的前提下建立节奏对比。

---

---

## 评分构成

| 维度 | 权重 |
|---|---:|
| Generation Stability | 35% |
| Character DNA Consistency | 25% |
| Shot Feasibility | 15% |
| Visual Impact | 10% |
| Effect-first Value | 10% |
| Art Direction | 5% |

判定：`>=90 PASS` / `75-89 GOOD` / `60-74 REVISION` / `<60 REBUILD`
