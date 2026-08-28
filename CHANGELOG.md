# Changelog

All notable changes to AstraForge Studio（星铸工坊）are documented in this file.

---

## v2.5.0 — 角色表演与生命感镜头

- 新增人物表演设计层：当前行为、外界刺激、即时反应、继续/收束。
- 新增生命感镜头卡、镜头动机与环境互动规则，减少角色摆拍感。
- 新增偶然瞬间与动作/情绪余韵要求。
- 新增镜头差异矩阵：相邻生成片段至少三个视觉/表演维度不同。
- 特效预算升级为“一个主效果 + 一个轻辅助效果”，并保护角色身份区域。
- 新增主视觉效果增强任务，在不改角色身份的前提下优化构图、光线和层次。
- 默认审美调整为面向中文用户的日式动漫角色基线；用户明确指定其他风格时可覆盖。
- 保留 v2.2.0 的三阶段确认、五种生成方式、即梦/H3 平台适配和案例摄取流程。

## v2.2.0 — 效果优先执行内核恢复

- 建立唯一执行主链，统一技能入口、生产流程、任务调度和模块映射。
- 重建不含商业约束的创意方向库与表现策略引擎。
- 统一导演方案重新承载多角色、能量曲线、节拍事件、快切小镜头、独立生成片段、文字图形和音频卡点。
- 新增可执行质量评分、安全自动修改和复检，质量不通过时禁止平台编译。
- 新增执行内核与质量闭环回归检查。

## v2.1.0 — 五种生成方式与严格校验

- 文生、首帧、尾帧、首尾帧和多参考改为五套独立编译策略。
- 新增严格导演方案校验，覆盖时间线、总时长、文字互斥、素材锚点、编号和继承范围。
- 编译器在校验失败时停止输出，不再生成表面完整但不可执行的提示词。
- 新增五个有效编译样例和四个故意错误的拒绝样例，并接入持续集成。

## v1.3.0 — Rhythm Intelligence

### Added

- Rhythm Engine v2：Energy Curve、Beat Grid、Beat Event、Micro-shot、Generation Clip。
- Action 15s 双时间尺度：16-28 个微镜头聚合为 4-6 个 2-4s 生成片段。
- PV Rhythm Score 与生成质量双门槛，补齐 Hook、事件密度、节拍对齐、能量反差与高潮强度。
- 证据驱动案例工作流：`draft → reviewed → proven/rejected`。
- `tools/ingest_case.py`：案例规范化、时间指标计算、证据指纹、重复检测与索引更新。
- `tools/validate_cases.py`：状态、评分、时间轴和 proven 准入校验，并接入 CI。

### Changed

- 重构 Action 15s 模板为五个独立 Generation Clip；每段只保留一个主动作，并提供 Beat Grid 与可剪辑节点。
- Shot Planner 不再把 8-10 个大段等同于 Action 快切。
- Composer 输出升级为 Director Package + 分片 Model Prompt Package。
- 成功案例不再仅靠 Prompt 文本晋升为 proven，必须包含实际输出与指令服从证据。

## v1.2.2 — Poster-MG Methodology

将三份成功案例 PV（太刀城市 / 命运赌场 / 兔耳魔术师）的创作要点系统提炼为
「平面海报式 / Editorial MG / 剪影符号化」方法论，融入案例库与 skill 能力层。

### Added

- **平面海报式实证案例** `references/cases/proven-editorial-mg-poster.yaml`
  - 综合三份成功案例，沉淀可复用方法论：视觉基底（纯二维/平面化/剪影化/符号化）、
    三色高反差 + 色彩语义系统（红=危险/白=规则/黑=未知）、世界符号库（每主题一套固定 2D 原语）、
    剪影↔赛璐璐瞬时切换、图形匹配转场方法论、20s 分镜节奏结构、反派终场揭示模板、
    动态负向约束清单范式、音乐/音效一等输入、同构不同皮变体（太刀/赌场/兔耳）
- **规则层扩展** `references/extracted-rules.md` 由 11 类扩展至 16 类
  - 十二、平面海报式 / Editorial MG 视觉规则
  - 十三、剪影 ↔ 赛璐璐 瞬时切换手法
  - 十四、反派终场揭示结构（Villain Reveal at End）
  - 十五、符号化图形系统（每主题一套固定 2D 原语）
  - 十六、动态负向限制清单范式（颗粒化枚举禁止项）
  - 顶部来源署名补充三份成功案例 PV
- **SKILL.md 接入**
  - 知识系统生产资产表新增案例入口 + 规则层 16 类说明
  - 最佳使用方式新增「方法 4：平面海报式 / Editorial MG PV」
- **skill 能力声明** `skill/manifest.yaml`
  - 新增能力 `editorial_mg_poster_style`
  - 新增 `visual_approaches`（cel_animation / editorial_mg_poster 双构图模式）
  - 版本升级至 1.2.2（Poster-MG Methodology）；SKILL.md / README 版本与徽章同步

### Changed

- `skill/execution-flow.yaml` 的 `genre_params` 新增 `poster_mg` 段，量化平面海报式镜头节奏：
  蒙太奇窗口（9-15s）、蒙太奇密度（6s 窗口 8-20 切镜 / avg 0.3-0.8s / 关键姿态定格不连续动作）、
  反相触发频率（每次鼓点 ≈ 每 0.4-0.5s 一次，类型 black-white-invert / single-frame-red-flash /
  single-frame-white-flash / geometric-deconstruct）、剪影↔赛璐璐切换窗口（0-6s）、角色占比（~70% 静止）、
  图形匹配转场硬约束、bpm 120-140
- `SKILL.md` 知识系统资产表 + Genre→模板表新增 `templates/poster-mg-20s.md` 入口

### Resolved (from prior Known Limitations)

- ✅ 专项「海报式→分镜」自动导演模板 `templates/poster-mg-20s.md` 已补齐（局部开场→剪影↔赛璐璐揭示→
  侧面平移→MG 蒙太奇 9-15s→反派终场→标题拼合，含平面海报式硬约束与 Validation）
- ✅ MG 蒙太奇密度 / 反相触发频率已量化进 `execution-flow.yaml` 的 `genre_params`（见 `poster_mg` 段）

---

## v1.2.1 — Male Concept Breakdown

将「男生角色设计提示词」的有效要点系统融入项目，新增角色概念分解图资产并固化男性主题分解矩阵。

### Added

- **角色概念分解图资产** `director/character-concept-sheet.md`
  - 六维拆解框架：服装分层 / 私密内着拆解 / 表情集 / 材质特写 / 物品质感特写 / 生活切片（关联物品）
  - 构图布局（中心立绘 + 环绕拆解 + 手绘引导线）、视觉规范（白底设计稿变体仍服从 Base Style 锁定）、执行逻辑（4 步对接 Step0→Step1）、可直接套用的文生图 Prompt 模板
  - 与 `character-card-template.md` 互补，共享角色设定卡与 Base Style 锁定，不替换角色圣经
- **男性主题分解矩阵** — `library/theme/theme-library.yaml` 的 `male-suit-release` / `male-samurai-release` / `male-knight-release` 各新增 `concept_sheet` 字段（服装分层 / 私密内着 / 表情集 / 材质特写 / 生活切片三桶），确保风格统一有数据支撑
- **基准用例 BM-11** `benchmark/test-cases/bm-11-male-concept-sheet.yaml` — 校验概念分解图资产与男性西装 Theme 协同（dimension=concept-sheet 新资产回归）

### Added (Female Extension)

- **概念分解图女性向扩展** `director/character-concept-sheet.md`
  - 性别化背景色：男性向纯白 / 浅灰稿纸；女性向米黄 / 羊皮纸 / 浅灰纹理背景（仅呈现层，不触发画风切换）
  - 生活切片三桶命名跨性别统一为「随身包袋与内容物 / 个护与配饰 / 个性化物件」，补充女性向示例（手账本 / 常备药品 / 收藏品 / 化妆镜 / 香水 / 发饰）
  - 材质特写新增「做旧痕迹」（磨损边 / 褪色 / 起球）以增强女性向生活厚度，并约定高奢 / 禁欲系角色应克制
  - 私密内着术语对齐（打底衫 / 袜类），表情集补充女性情绪（甜笑 / 自信挑眉 / 走神 / 狡黠）
- **女性主题分解矩阵** — `library/theme/theme-library.yaml` 的 `cool-female-jrpg` / `sweet-y2k-girl` / `academy-character` / `magic-girl` / `cyberpunk-girl` / `dark-witch-release` 各新增 `concept_sheet` 字段，与男性矩阵对称
- **基准用例 BM-12** `benchmark/test-cases/bm-12-female-concept-sheet.yaml` — 校验概念分解图资产与女性甜系 Y2K Theme 协同（dimension=concept-sheet，与 BM-11 对称）

### Added (Neutral Extension)

- **概念分解图中性向扩展** `director/character-concept-sheet.md`
  - 引言、生活切片三桶脚注、一致性约束补充中性 / 非二元指向（`character-release` / `gacha-legendary` 两个性别中立主题）
  - 背景规则扩展：中性 / 非二元角色可在「纯白稿纸」与「羊皮纸纹理」间按气质二选一，均仅限呈现层
  - 生活切片第三桶补充中性向示例（跨性别通用：徽章 / 盲盒 / 手账 / 明信片）
- **中性主题分解矩阵** — `library/theme/theme-library.yaml` 的 `character-release` / `gacha-legendary` 各新增 `concept_sheet` 字段（跨性别通用示例，与男 / 女矩阵对称）
- **基准用例 BM-13** `benchmark/test-cases/bm-13-neutral-concept-sheet.yaml` — 校验概念分解图资产与性别中立基础发布 Theme 协同（dimension=concept-sheet，与 BM-11 / BM-12 对称）

### Changed

- `SKILL.md` Step1 流程补充「角色概念分解图」产出说明，生产资产表新增该文档条目
- `README.md` Benchmark 表新增 BM-11 / BM-12，`Current Release` 记录 v1.2.1 女性扩展

### Known Limitations

- 概念分解图目前为 Step1 设定稿资产，尚未提供专项「分解图→分镜」自动导演链路

---

## v1.2.0 — 2D Style Expansion

视觉风格扩展：从单一赛璐璐扩展为 7 套 2D base style，同时补齐男性角色主题与角色图 Prompt Gate。

### Added

- **2D 多画风体系**
  - 7 个 base style：`modern-cel` / `retro-cel` / `painterly-anime` / `watercolor-ink` / `vector-flat` / `korean-manhwa` / `western-comic`
  - `core/style-anchor.md` 重写为 2D 风格锚定语模板库，每个 base 含中英锚定与专属禁止项
  - `library/style/style-library.yaml` 新增 5 个 base 组件与 `motion-comic` 呈现层
  - `core/style-engine/style-conflict-rules.yaml` 新增 conflict.004-007，防 2D base 中途互切与跨形态混搭
  - `core/style-engine/style-priority-rules.md` 增加 Base Style 选择规则（按角色美术语言）
  - H3 schema 与 `core/h3-generation-rules.md` 由「赛璐璐硬编码」改为「所选 base 锚定贯穿」
  - PV 模板与角色卡模板参数化：默认 `modern-cel`，可替换为其他 2D base
- **男性角色主题**
  - `library/theme/theme-library.yaml` 新增 `male-suit-release` / `male-samurai-release` / `male-knight-release`
  - 角色路由新增 `male_cool` / `male_hotblooded` / `male_mature`
  - 表情组件 `composed-gaze` / `battle-resolve` / `detached-stare`
  - Benchmark BM-09（Male Suit Elegance 97）、BM-10（Male Samurai Combat 93），BM-04 升级为骑士主题
- **角色图 Prompt Gate**
  - 交互协议 Step0-2 重构：先确认角色与风格、输出角色设定图 Prompt，再锚定 `SESSION_SPEC`
  - `director/character-card-template.md` 支持按 base style 参数化

### Changed

- 默认 `modern-cel` 不变，未指定其他 base 时行为向后兼容
- `core/prompt-structure.md` 与模板的默认禁止项补充欧美卡通反向排除（base = western-comic 时反转）
- `docs/ARCHITECTURE.md`、`docs/USER_GUIDE.md`、`docs/CONFIGURATION.md` 同步多画风说明

### Known Limitations

- 尚未提供 2D 多画风专项 Benchmark 用例
- 3D 形态（三渲二 / 写实 CG / 实拍 VFX）仅列入 roadmap，未进入 P0
- 2D 内 planned 美术细节（fantasy-luxury / sci-fi-anime / urban-neon / historical-anime 等）待后续版本

---

## v1.1.0 — Character Universe Expansion

角色宇宙扩展。核心是把系统从「单角色 PV 导演」扩展为「角色宇宙导演」，
同时补齐可生产性（frontmatter / 模板缺陷 / 校验体系）。

### Added

- **中文品牌名**：星铸工坊。定位语「AI 二次元游戏角色 PV 智能导演系统」
- **Cast Engine（多角色 PV）** — `core/multi-character/`
  - duo / trio / squad 阵容，画面权重 `sum==70` 且 `lead >= second × 1.5`
  - identity_bleed 风险建模、contrast 准入闸门、同框动作等级放大
  - 稳定性按阵容规模封顶 `{1:35, 2:32, 3:28, 4:24}`
  - `templates/cast-duo-15s.md` 双人完整 Prompt 模板
  - 6 个同框镜头组件，均带 `negative_addon` 禁止特征互换
- **Event Engine（活动 PV）**
  - 周年 / 联动 / 季节三类 Theme，CTA 强制且须含活动时间
  - `director/event-director.md`
  - `costume_variant_exception` 受控放行限定造型
- **可生产性修复**
  - `SKILL.md` 补 frontmatter（此前缺失导致 skill 无法被发现与触发）
  - 三个 genre 模板末段补齐机位标注（继承自前身 skill 的缺陷）
  - `examples/walkthrough-frostblade/` 端到端实测样例
- **校验体系**
  - `tools/validate_templates.py`、`tools/validate_benchmarks.py`、`tools/check_links.py`
  - 全部接入 CI，共 5 个校验器
- **工程规范**
  - `docs/BRANCH_POLICY.md`：禁止直接推送 main，经 dev + PR
  - `.githooks/pre-push` 本地守卫 + GitHub Branch Protection 双层强制

### Changed

- `group battle` 由笼统 `level_4 forbidden` 细分：无序混战仍禁止，结构化多角色可控
- Genre 动作等级上限修正（`daily` 1→2）并引入 `genre_ceiling_uplift`
- 全部 61 个组件增加显式 `slug` 字段
- Benchmark 覆盖度 85 → 93（8 例，含首个男性角色 / 多角色 / 活动 PV）

### Known Limitations

- squad（4 人）规则已定义但无用例
- 联动 / 季节 Theme 已定义但无用例
- 男性角色仅有表情组件，尚无专属 Theme

---

## v1.0.0 — Foundation Release

**Initial Production Release**

首个正式公开版本。项目前身为内部迭代的 `AnimePV-H3`（迭代至 v2.6），
v1.0.0 起以 AstraForge Studio 名义重新起版，定位为 Production Foundation Release。

### Added

- **Character DNA System** — 角色视觉资产锁定，跨镜头一致性保护，H3 Prompt 自动注入身份锚点
- **Theme Engine** — 商业方向驱动的 PV 主题选择
- **Variation Engine** — 同角色多商业版本（Release / Gacha / Combat / Story / Skin）
- **Style Stack** — Base + Premium + Special 三层视觉语言，含冲突检测与自动收敛
- **Composer** — 5s / 15s / 30s 自动导演，组件评分匹配算法
- **Quality Engine** — 稳定性优先的自动评分、H3 风险分析、自动返修闭环
- **Benchmark Framework** — 回归测试体系（Sweet Y2K / Cool Warrior / Dark Witch）
- **Visual Component Library** — Camera / Action / Expression / Transition / Theme / Style
- **Production Schema** — Character Bible / Shot List / H3 Prompt / Quality Report / Revision Log
- **文档体系** — README / SKILL / User Guide / Architecture / Developer Guide / Installation / Configuration / Contributing

### Changed

- 项目全面从 `AnimePV-H3` 更名迁移为 `AstraForge Studio`
- `composer/` → `director/`，`output-schema/` → `schema/`
- 质量评分权重由「视觉冲击优先」调整为「生成稳定性优先」

### Added (Prompt 生产资产回填)

从 `animepv-h3` 原始 skill 与三份已验证成片案例中提炼补齐，
让项目从「架构规范」变为「可直接产出 Prompt 的生产系统」：

- **Prompt Engineering 层**
  - `core/prompt-structure.md` — 10 段结构规范 + 输出前自检清单（生成前必读）
  - `core/style-anchor.md` — 赛璐璐风格锚定语（中英双版）
  - `core/session-spec.md` — SESSION_SPEC 锚定、信息充分性校验、Generation Gate
- **H3 输出格式规范**
  - `schema/h3-base.md` — T2VA / I2VA / FL2VA / L2VA 三字段格式
  - `schema/h3-ref2va.md` — Ref2VA 六字段格式
  - 镜头六要素：composition / subjects / environment / actions / camera / sound
- **Genre 内容类型层**（与 Theme 正交）
  - `library/genre/genre-library.md` — 打斗 / 日常文戏 / 魔法幻想，含可量化帧率、运镜、震动、BPM 参数
  - `library/style/persona-tags.md` — 6 种 Persona 风格标签与叠加规则
  - `library/camera/camera-motion-spec.md` — 运镜速度、机位变化 6 维强制规则、转场清单
- **完整可用 Prompt 模板**
  - `templates/genre-action-15s.md` — 打斗 15s（含 10 段完整 Prompt + 5s/10s 适配 + 精简版）
  - `templates/genre-daily-15s.md` — 日常文戏 15s
  - `templates/genre-magic-15s.md` — 魔法幻想 15s
- **导演资产**
  - `director/storyboard-4shot.md` — 4 镜头连贯分镜脚本
  - `director/character-card-template.md` — 角色设定卡 + 出图 Prompt
- **实证案例库**
  - `references/cases/proven-pink-signal.yaml` — 御姐甜妹 PINK SIGNAL（H3 实测直出）
  - `references/cases/proven-academy-file.yaml` — 学院傲娇 ACADEMY FILE（H3 实测直出）
  - `references/cases/proven-cel-baseline.yaml` — 赛璐璐三套可量化参数基线
  - `references/extracted-rules.md` — 从实证案例提取的 11 类规则

### Known Limitations (v1.0.0 当时)

- Benchmark 覆盖偏女性角色，缺少多角色 / 群像 / 活动 PV 用例
- Theme 库仍在扩展中


# v2.0.0 — 效果优先交互流程

- 完全移除商业定位、广告、抽卡、活动宣传和商业评分模块。
- 建立角色主视觉、视频文字声音、平台生成方式三阶段确认。
- 平台收敛为即梦、MiniMax H3 官方和 MiniMax H3 自行部署。
- 支持文生、首帧、尾帧、首尾帧和多参考五种生成方式。
- H3 遵循官方三字段、六字段与素材引用规范。
- 案例摄取改为原始提示词唯一必填，成片和其他信息全部可选。
# v2.0.1 — 执行统一与平台编译

- 完成全仓效果优先迁移，清除旧营销字段、模块引用和评分键。
- 重写执行流程为三阶段、三次确认，并加入文字策略互斥与素材一致性检查。
- 新增统一导演方案、三套平台适配器和可执行提示词编译脚本。
- 新增即梦首帧、H3 多参考编译样例及迁移防回流检查。
