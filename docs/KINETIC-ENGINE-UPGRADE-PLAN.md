> **归档说明**：本文档为 v1.2.2 主线时期的 v1.3.0「动能引擎」升级蓝图（合并自三份提案）。其核心设计（分段动态风险预算、PV Rhythm Score 双门槛、Sakuga 组件库、Energy Curve / Beat Grid / Micro-shot / Generation Clip）已在 v2.5.0「角色表演与生命感镜头」中实现；商业化相关暂缓项与 v2.5.0 的去商业化方向无关，仅作历史参考。

# AstraForge Studio · v1.3.0 动能引擎升级 · 合并实施方案

**计划代号**：Kinetic Engine v1.3.0 — "从 Prompt Library 升级为 Rhythm-aware Prompt Compiler"

**基线**：当前 `main`（v1.2.2，BM-01 ~ BM-13，93/100）
**本文档状态**：待评审（尚未开始改代码）

---

## 0. 方案来源与合并说明

本方案由三份独立提案合并而来，三者诊断同一病灶、方案互补：

| 来源 | 主题 | 本方案采纳程度 |
|---|---|---|
| 动能引擎升级规范（Sakuga 商业 PV 架构） | 引擎级具体改造 | **作为主干骨架** |
| 优化方案（Rhythm Engine 2.0） | 节奏架构层 | **吸收节奏分层/微镜头/双门槛/输出瘦身** |
| 全风格扩展与商业化解耦重构方案 | 跨风格战略重构 | **本次暂缓**（见 §9） |

**一句话目标**：打破"稳定性单一权重"禁锢，引入 **Micro-shot 切片 + 分段动态风险预算**，把节奏/动能真实编译进生成时间轴，同时把"给人看的导演方案"与"给模型的最小指令"彻底分离。

---

## 1. 核心目标与非目标

### 必须达成
1. 统一动作节奏定义，消除"单镜 0.3–0.8s"与"15s 8–10 镜"的矛盾（见 §4.1）。
2. 新增可计算的 **Beat Grid** 与 **Energy Curve**，把 BPM 从氛围描述变成控制信号。
3. 引入 **Micro-shot / Generation Clip 双层单位**，让节奏可被模型服从、可被后期快切。
4. 质量引擎改为**分段动态风险预算**，并新增 **PV Rhythm Score**，配合 Stability 构成**双门槛**。
5. Prompt 输出**瘦身分层**：Director Package（人看）+ Model Prompt（模型最小指令）。
6. 新增 **CI 校验脚本 + BM-14 基准用例**，让"动能"成为可回归验证的规则。

### 明确不做的（v1.3.0 范围外）
- ❌ 跨领域插件化（Cinema / 3D Ad / Documentary Domain Pack）——见暂缓事项 §9。
- ❌ Commercial vs Cinematic 双模式正式 UI / CLI。
- ❌ Editorial MG/Remotion 合成管线（仅预留数据接口，见 §4.6）。
- ❌ 真实视频成片生成（本系统仍只产出 Prompt 与参数，Generation Gate 锁定）。

---

## 2. 目标架构（融合后流水线）

```
[用户输入]
   ↓
Character DNA 锁定
   ↓
PV Director: 3-Stage Pacing（蓄力→爆发→定格 节拍拆解）
   ↓
🎵[新] Energy Curve（能量曲线，非镜头列表）
   ↓
🎵[新] Beat Grid（拍点事件表，BPM→控制信号）
   ↓
🎬 Kinetic Shot Planner: Micro-shot 0.4–1.2s 切片
   ├─ 区分 micro-shot（剪辑单位）与 generation clip（模型生成单位）
   ↓
📚 Kinetic Library: Sakuga 词库 + 极限运镜注入
   ↓
🖼 FL2VA 引擎: 首末帧 3D 位移锚定（>80% 像素变动）
   ↓
⚖️ Quality Engine: 分段动态风险预算 + PV Rhythm Score 双门槛
   ↓
📦 输出分离: Director Package (人) / Model Prompt (模型)
   ↓
🚚 [Generation Gate] 用户显式二次确认
   ↓
🧪 CI: validate_kinetic_density.py + BM-14（+ 既有 rule/benchmark 回归）
```

---

## 3. 实施阶段总览

| 阶段 | 主题 | 主要产出 | 里程碑 |
|---|---|---|---|
| Phase 0 | 节奏概念统一 | 节奏常量表（micro-shot / generation clip / 镜头数新规则） | v1.3.0-alpha |
| Phase 1 | 质量与规则层 | 分段风险预算 + Rhythm Score + 双门槛 | v1.3.0-alpha |
| Phase 2 | 动能组件层 | Sakuga 动作/极限运镜 YAML 库 | v1.3.0-beta |
| Phase 3 | 导演编排层 | 3-Stage Pacing 切片 + FL2VA 位移协议 + Pour 模板 | v1.3.0-beta |
| Phase 4 | CI 与基准 | `validate_kinetic_density.py` + BM-14 + 全量回归 | v1.3.0-rc / 发布 |

---

## 4. 各阶段改造细则

### Phase 0 · 节奏概念统一

**问题**：`library/genre` 声明 action 单镜 0.3–0.8s，`director/shot-planner.md` 却规定 15s 8–10 镜（1.5–2s/镜），模板也是十个 1.5s 段落。

**改动**：
- 在 `core/` 新增节奏常量表 `core/rhythm/pace-constants.md`，明确两个正交概念：
  - `micro-shot`：剪辑单位，0.25–1.2s（动作/魔法快切段 0.3–0.8s，文戏慢切段 1–2.5s）
  - `generation clip`：模型生成连续动作单位，2–4s
- 改写 `director/shot-planner.md` 编排规则#2：由"8–10 镜"改为以 **micro-shot 密度**为准（`cuts_per_second`），并说明一个 generation clip 内含若干可剪辑的 micro-shot 节点。
- 更新 `library/genre/genre-library.md` 与三个 genre 模板的节奏表，使单镜时长与镜头数不再自相矛盾。

**验收**：`director/shot-planner.md` 不再出现"0.3–0.8s 快切"与"1.5–2s/镜"并存表述。

---

### Phase 1 · 质量与规则层

#### 4.1 `core/quality-engine/` 分段动态风险预算

废弃全局固定 `Generation Stability 35%`，改为按镜头阶段（Shot Phase）浮动：

| 镜头阶段 | Stability | Kinetic Density | DNA Consistency | Visual Impact | 允许形变 |
|---|---|---|---|---|---|
| **Anticipation 蓄力/微动** | 40% | 10% | 35% | 15% | None（锁脸锁装） |
| **Sakuga Burst 极速爆发** | 15% | 45% | 15% | 25% | High（透视拉伸/拖影允许） |
| **Hero Settle 定格收招** | 35% | 15% | 35% | 15% | Low（仅衣摆/发丝微动） |

落地位置：修改 `core/quality-engine/risk-budget-gate.yaml` 的 `action_level_limits` 逻辑——动作等级上限由"全局 15s=2"改为**按阶段赋予等级配额**（Anticipation 低 / Sakuga Burst 允许 high / Hero Settle 中），并保留原有 `substitution_table` 作为越限兜底。

新增文件 `core/quality-engine/dynamic_negatives.yaml`（动能负向抑制词表）：

```yaml
kinetic_negative_presets:
  action_burst:
    mandatory_negatives:
      - "slow motion"
      - "lazy drifting"
      - "floating pose"
      - "static gaze"
      - "mannequin freeze"
      - "smooth pan without motion blur"
      - "gentle idle movement"
    threshold_penalty: 0.25
```

#### 4.2 新增 PV Rhythm Score + 双门槛

新增 `core/quality-engine/rhythm-rules.yaml`，评分权重：

```yaml
pv_rhythm_score:
  hook_strength: 20      # 开场 0.8s 抓人力
  event_density: 15      # 每 1.2s 内新视觉事件密度
  beat_alignment: 15     # 动效是否落到拍点
  energy_contrast: 15    # 高低能量段反差
  shot_variety: 10       # 机位/景别多样性
  character_sell: 15     # 角色识别信息呈现
  climax_strength: 10    # 高潮是否强于开场
```

**硬性门槛（不满足即扣分/拒绝）**：
- 前 0.8s ≥ 2 个视觉事件
- 连续 > 1.2s 无新事件 → 扣分
- 15s ≥ 3 次明显能量变化；高潮能量 > 开场能量
- 末 2s 必含角色识别信息
- 动作镜头必须声明 `anticipation / impact / recovery` 三段
- 禁止所有镜头同一种速度

**输出门禁改为双门槛**（修改 `core/quality-engine/quality-rules.yaml` 的 pass_conditions）：

```yaml
pass_conditions:
  generation_stability: ">= 75"
  pv_rhythm_score: ">= 80"
```

避免"稳定性 91 但完全不像动漫 PV"仍通过。

---

### Phase 2 · 动能组件层

#### 4.3 Sakuga 组件库

新增 `library/camera/kinetic_camera.yaml`：

```yaml
camera_components:
  - id: "crash_zoom_eye"
    name: "瞬时推焦眼部"
    prompt_tokens: "instant crash zoom into character's glowing eye, extreme dynamic focal shift, motion lines"
    recommended_duration: "0.4s - 0.6s"
  - id: "whip_pan_slash"
    prompt_tokens: "high-velocity whip pan camera following weapon trail, extreme directional motion blur"
    recommended_duration: "0.3s - 0.5s"
  - id: "dynamic_dutch_tracking"
    prompt_tokens: "aggressive 45-degree Dutch tilt camera, dynamic shake, fast forward dolly tracking"
    recommended_duration: "0.8s - 1.2s"
```

新增 `library/action/sakuga_action.yaml`：

```yaml
action_components:
  - id: "smear_frame_slash"
    prompt_tokens: "anime smear frames, exaggerated perspective foreshortening, kinetic blade trail, afterimage"
  - id: "impact_frame_burst"
    prompt_tokens: "high-contrast black and white impact frames, invert flash, radial speed lines burst"
  - id: "instantaneous_displacement"
    prompt_tokens: "sudden explosive burst displacement, zero acceleration startup, sonic boom air distortion"
```

> 与既有 `library/camera/camera-library.yaml`、`library/action/action-library.yaml` 并存，作为**动能专用库**供 Sakuga Burst 阶段调用；组建 id 规则需通过现有 `tools/validate_benchmarks.py` 的组件引用校验。

---

### Phase 3 · 导演编排层

#### 4.4 Kinetic Shot Planner：3-Stage Pacing 切片

改写 `director/shot-planner.md`，新增"蓄力→爆发→定格"微镜头切片排期示例（15s Action，5 镜示范）：

| 镜 | 剪辑时长 | 阶段 | 运镜 | 动作物理事件 | 目标 |
|---|---|---|---|---|---|
| 01 | 0.6s | 亮相闪现 | Crash Zoom | 拔刀 1/3，瞳孔反光缩放 | 悬念 |
| 02 | 1.4s | 蓄力微动 | Low-angle Tilt | 粒子聚集，衣角翻飞 | 能量压迫 |
| 03 | 0.4s | 极速突进 | Whip Pan | 瞬时位移，残影 | 速度爆发 |
| 04 | 0.5s | 核心命中 | Screen Shake | 斩击贯穿，黑白反色 Impact Frame | 冲击最高点 |
| 05 | 1.1s | 帅气收招 | Slow Orbit 15° | 纳刀入鞘，刀镡碰火 | 情绪定格 |

**单镜头降解为单一物理事件**（One Shot One Physical Event），取代"一镜塞多动作"。

#### 4.5 FL2VA 首末帧位移锚定

新增 `templates/fl2va-kinetic-anchor.md`，规定：
- **Start Frame**：极近景 3/4 侧脸，重心压缩下移，武器蓄力态。
- **End Frame**：极大远景/仰视全身，武器已挥出或收鞘，背景放射状斩痕/粒子碎裂。
- **插值驱动逻辑**：强制两帧 >80% 像素空间变动，逼模型生成高速运动矢量，杜绝微动摆拍。

同步修改 `templates/genre-action-15s.md` / `genre-magic-15s.md`，为快切段标注 `FL2VA kinetic anchor` 与 generation clip 切分点。

#### 4.6 输出瘦身分层 + 预留后期接口

**Director Package**（给人看，完整）：创意方向 / Energy Curve / Beat Grid / Shot List / 音乐剪辑说明 / 风险报告。
**Model Prompt**（给模型最小指令）：主体锁定 / 当前片段单一主动作 / 一个镜头运动 / 一个特效 / 起始姿态 / 结束姿态 / 速度节拍 / 负向约束。

> **暂不开工但预留**：Model Prompt 阶段对排版/文字 Token 做"纯净化"过滤，防止模型生成乱码像素；为未来 Editorial MG / `editorial_manifest.json`（Remotion/AE 后期合成）预留数据出口，v1.3.0 只输出结构，不接合成管线。

---

### Phase 4 · CI 与基准

新增 `tools/validate_kinetic_density.py`：
- 检查 `sakuga_burst` 阶段 Prompt 是否含动能关键词（smear / impact frame / crash zoom / whip pan / afterimage / speed lines / displacement / foreshortening）。
- 检查是否含被动/缓动词汇（slow motion / gentle / soft floating / static / mannequin），命中即 FAIL。

新增基准 `benchmark/test-cases/bm-14-action-sakuga-burst.yaml`（Male Samurai Sakuga Burst Combat，含 anticipation + sakuga_burst 两组镜头与对应动能 Prompt）。

**回归范围**：既有的 BM-01~13 全量跑通，保证规则重构无破坏性回退；`tools/validate_benchmarks.py`、`tools/validate_templates.py` 同步通过，`tools/check_version.py` 需将版本号对齐。

---

## 5. 文件变更清单

| 类型 | 文件 | 动作 |
|---|---|---|
| 新增 | `core/rhythm/pace-constants.md` | 节奏常量表 |
| 新增 | `core/quality-engine/dynamic_negatives.yaml` | 动能负向抑制词表 |
| 新增 | `core/quality-engine/rhythm-rules.yaml` | PV Rhythm Score 定义 |
| 新增 | `library/camera/kinetic_camera.yaml` | 极限运镜库 |
| 新增 | `library/action/sakuga_action.yaml` | Sakuga 作画特效库 |
| 新增 | `templates/fl2va-kinetic-anchor.md` | 首末帧位移协议 |
| 新增 | `tools/validate_kinetic_density.py` | 动能密度 CI 校验 |
| 新增 | `benchmark/test-cases/bm-14-action-sakuga-burst.yaml` | 动能基准用例 |
| 修改 | `core/quality-engine/risk-budget-gate.yaml` | 分段风险预算 + 分阶段动作等级配额 |
| 修改 | `core/quality-engine/quality-rules.yaml` | pass_conditions 双门槛 |
| 修改 | `director/shot-planner.md` | 3-Stage Pacing 切片 + micro-shot 规则 |
| 修改 | `library/genre/genre-library.md` | 节奏表统一 |
| 修改 | `templates/genre-action-15s.md` / `genre-magic-15s.md` | FL2VA 锚定 + generation clip 切分 |
| 修改 | `README.md` / `SKILL.md` / `CHANGELOG.md` / release manifest | 版本与能力声明更新 |
| 修改 | `.github/workflows/*` | CI 挂入 validate_kinetic_density.py |

---

## 6. 验收标准（Definition of Done）

**规则层**
- [ ] shot-planner 不再存在节奏自相矛盾。
- [ ] Rhythm Score 硬门槛 7 条全部代码化校验。
- [ ] 双门槛 `stability ≥75 && rhythm ≥80` 生效。

**组件层**
- [ ] 动能组件 id 通过既有组件引用校验。
- [ ] 组件仅被 Sakuga Burst 阶段调用，不污染蓄力/收招的稳定锁定。

**基准层**
- [ ] BM-14 通过 `validate_kinetic_density.py`。
- [ ] BM-01~13 全量回归通过（93/100 不回退）。

**产物层**
- [ ] 一条 15s action 示例能同时产出 Director Package（含 Energy Curve + Beat Grid）与精简 Model Prompt。

---

## 7. 风险与回滚

| 风险 | 等级 | 缓解 |
|---|---|---|
| 分段风险预算放开形变 → 角色漂移回潮 | 高 | Anticipation/Hero 阶段仍 35%+ 锁脸锁装；DNA 锁定优先 |
| Micro-shot 切得过碎 → 信息过载/晕眩 | 中 | 硬门槛"连续 1.2s 无事件扣分"+"禁止全身同速"双向约束；始终保留 generation clip 边界 |
| 双门槛过严 → 成片率下降 | 中 | 门槛设 `>=80` 起步，按 BM 回归结果微调，避免最初就从 100 起步 |
| Doc2 跨域重构半途混入 | 高 | 严格隔离：`domains/` 目录 v1.3.0 不创建；new feature 走独立 branch + PR 合 main |

**回滚策略**：每个阶段独立 commit，Phase 1 质量规则改动用可开关的 flag（旧静态权重路径保留为 fallback），任一阶段回归失败即回滚该阶段，不影响已通过阶段。

---

## 8. 建议实施顺序与节奏

1. **里程碑 alpha**（Phase 0 + 1）：节奏统一 + 分段风险预算 + Rhythm Score 双门槛。先让"规则不再打架、评分不再只看稳定"。
2. **里程碑 beta**（Phase 2 + 3）：Sakuga 组件库 + 3-Stage 切片 + FL2VA 协议 + 模板改造。让"动能真的有词可写、单个镜头真的只干一件事"。
3. **里程碑 rc/发布**（Phase 4）：CI 校验 + BM-14 + 全量回归 + 文档/版本同步。

> 建议每里程碑独立 PR、独立评审，符合仓库" dev-only push、main 走 PR"的分支策略。

---

## 9. 暂缓事项与未来路线（本次不实施）

Doc2 的**跨风格通用引擎重构**（微内核 + domain 插件、Cinematic/3D Ad、Commercial vs Cinematic UI、Remotion 合成流水线）与 v1.3.0 目标存在范围冲突，**本次明确暂缓**，列入后续版本：

- **v1.4.0**：将二次元逻辑收敛为 `domain-anime-pv`（为插件化铺路）；引入 `domain-cinematic-film` 光学/胶片库与 `domain-commercial-product` 3D 广告库（若确认需要跨风格）。
- **v1.5.0**：Commercial vs Cinematic 模式切换接口；接入 `editorial_manifest.json` 自动合成；跨风格 Benchmark CI。

> 理由：v1.3.0 的核心矛盾是"二次元 PV 不够燃、节奏未被编译"，应先解决单领域质量，再做多领域扩展，避免改动面过大导致回归失控。

---

## 10. 决策点（待你确认后进入执行）

本方案为 **Planning 阶段产物**，尚未开始改代码。进入执行前需确认：

1. Phase 1 双门槛取值：`stability ≥75 && rhythm ≥80` 是否采用，或按既有节奏放宽/收紧。
2. 是否按 §8 的三里程碑独立 PR 推进，还是合并主干一次性落地。
3. 约束：保持全程只产出 Prompt/参数、不调用生成能力（读回 SKILL.md 已有 Generation Gate）——本方案不违反。

**下一步**：确认后我先从 **Phase 0 + Phase 1** 动手。