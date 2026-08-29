<div align="center">

# AnimePv-promt

### 动漫角色视频提示词导演 · 可安装的 AI Agent Skill

**把角色创意变成可执行的动漫 PV 方案：角色设定 → 资产设定 → 分镜与提示词产出**

*From character ideas to executable anime PV prompts.*

![Version](https://img.shields.io/badge/version-2.5.0-blue)
![Codename](https://img.shields.io/badge/codename-%E8%A7%92%E8%89%B2%E8%A1%A8%E6%BC%94%E4%B8%8E%E7%94%9F%E5%91%BD%E6%84%9F%E9%95%9C%E5%A4%B4-8957e5)
![AI Skill](https://img.shields.io/badge/AI-Agent%20Skill-purple)
![Domain](https://img.shields.io/badge/domain-Anime%20PV-red)
![Status](https://img.shields.io/badge/status-production-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

[📖 Skill 入口](SKILL.md) ·
[🚀 安装](#安装) ·
[🧭 使用指南](docs/USER_GUIDE.md) ·
[🧪 Benchmark](benchmark/)

</div>

---

## 项目简介

**AnimePv-promt** 是一套可直接安装到 AI Agent 的专项 Skill，面向中文用户的动漫角色视频创作。它把角色侧的输入：

| 输入 | |
|---|---|
| 角色创意 | 人物背景 |
| 已有角色提示词 | 外观设计 |
| 角色参考图片 | 技能设定 |

转化为可直接投入制作的输出：

| 输出 | |
|---|---|
| 角色设定卡 | 分镜脚本 |
| 资产设定方案 | 节奏与镜头规划 |
| 平台专用提示词 | 质量评估报告 |
| 素材登记表 | 操作提醒 |

系统只产出**方案、提示词与参数**，不主动生成图片或视频；实际调用生成能力前必须获得用户明确确认。

## 三大核心能力

### ① 角色设定（Character Design）

- **分步完善角色**：从初步创意、已有提示词或角色图片三种入口逐轮补全身份气质、外观服装、武器能力、画风与构图；
- **Character DNA Lock**：锁定脸部、发色、瞳色、核心服装、标志资产，明确「不可变化特征」与「允许变化特征」，杜绝多次生成间的角色漂移；
- **概念分解图矩阵**：11 套角色类型（含男性西装 / 武士 / 骑士，女性甜系 / 赛博 / 暗黑魔女，中性非二元）的服装分层、表情集、材质特写、生活切片六维拆解；
- **主视觉增强**：只优化已有角色图的构图、光线、层次，禁止改动角色身份与核心五官。

### ② 资产设定（Asset Design）

- **风格基线**：默认面向中文用户的日式动漫角色审美，7 套 2D 基础风格（现代赛璐璐 / 复古赛璐璐 / 厚涂动画 / 水彩国风 / 矢量潮流 / 韩漫 / 美漫）可叠加；
- **组件库**：Camera / Action / Expression / Transition / 创意方向 / 生命感镜头 / 动能库（高速爆发、残影、冲击帧），全部机器可校验；
- **创意方向与表现策略**：动作爆发、情绪特写、神秘揭示、关系张力、图形化角色印象五大方向，按角色固定特征与目标画面效果选择；
- **多角色阵容**：duo / trio / squad 的画面权重、对比校验、同框风险建模与身份串味防护。

### ③ PV 动画分镜产出（Storyboard & Prompt Output）

- **节奏引擎 v2**：能量曲线、节拍表、快切小镜头（0.3–0.8s）与独立生成片段（2–4s），每个片段一个主动作、一个主要运镜、一个主特效；
- **人物表演设计**：镜头必须有拍摄理由；「原本状态 → 外界刺激 → 即时反应 → 收束」四段表演，环境可触发或反馈角色动作，拒绝无目的环绕与摆拍；
- **10 段 Prompt 结构规范** + H3 官方格式转换（三字段 / 六字段）；
- **严格质量闭环**：结构校验 → 质量评分 → 自动修改 → 复检，质量不通过时禁止平台编译。

## 分步工作流

Skill 采用三阶段交互，每阶段输出后等待确认：

```
第一阶段  完善角色与主视觉
   └─ 材料入口 → 角色设定卡 → 固定/可变特征 → 主视觉提示词
第二阶段  确定创意方向并规划视频、文字与声音
   └─ 创意方向 → 能量曲线 → 节拍事件 → 快切小镜头 → 文字与声音策略
第三阶段  质量闭环、平台、生成方式与素材
   └─ 结构校验 + 质量评分 → 平台选择 → 素材登记 → 平台专用提示词
```

## 支持平台与生成方式

| 平台 | 生成方式 |
|---|---|
| 即梦 | 文生视频 / 首帧 / 尾帧 / 首尾帧 / 多参考 |
| MiniMax H3（官方） | 同上五种，遵循官方 `h3-prompt-writing` 规范 |
| MiniMax H3（自行部署） | 同上五种，支持提示词正文 / 素材标签 / 检查点 / 推理参数分层 |

平台专用提示词由编译器直接产出，无需人工拼装：

```bash
python tools/compile_platform_prompt.py examples/platform-adapters/jimeng-i2va.yaml
python tools/compile_platform_prompt.py examples/platform-adapters/h3-ref2va.yaml
```

## 安装

```bash
git clone https://github.com/AvalonLee/AnimePv-promt.git
cd AnimePv-promt
```

将仓库根目录的 [SKILL.md](SKILL.md) 作为 Skill 入口注册到你的 AI Agent（入口与按需加载策略声明见 [skill/manifest.yaml](skill/manifest.yaml)）。Skill 按需读取 `core/`、`director/`、`library/`、`references/` 下的规则与词库，无需额外构建步骤。

详细部署说明见 [docs/INSTALLATION.md](docs/INSTALLATION.md)。

## 质量与回归体系

- 13 个机器可校验基准用例（action / daily / magic × 单人 / 双人 / 三人 × 男性 / 女性 / 中性），由 `tools/validate_benchmarks.py` 在 CI 中强制校验组件引用、风险预算与评分自洽；
- 质量评分以「生成稳定性 + 角色一致性」为双门槛，节奏效果分独立评估；
- CI 包含 YAML 组件校验、命名迁移、版本一致性、模板 / 基准 / 案例 / 平台适配器 / 导演方案 / 执行内核 / 质量闭环 / 效果优先迁移共 12 项检查（见 [.github/workflows/validate.yml](.github/workflows/validate.yml)）；
- 证据分级案例库：只强制原始提示词，其余证据可选，`prompt_only` 提取的规律自动标记「待验证」。

## 项目结构

```
AnimePv-promt/
├── SKILL.md                 AI Agent Skill 入口
├── skill/                   Skill 部署清单
├── core/                    核心规则（角色 DNA / 风格引擎 / 质量引擎 / 节奏引擎 / 表现策略）
├── workflow/                任务调度与执行主链
├── director/                导演系统（表演 / 分镜 / 主视觉增强 / 概念分解图 / 群像）
├── library/                 视觉组件库 + 创意方向 + 生命感镜头 + 动能库
├── templates/               15s 分镜模板
├── references/              平台规范 / 审美基线 / 实证案例
├── case-library/            证据分级案例库
├── benchmark/               回归基准（13 用例 + 导演方案边界样例）
├── schema/                  数据协议（导演方案 / 节奏 / 音频卡点 / 编辑清单）
├── examples/                示例输出 + 平台适配器样例
├── platform-adapters/       可执行平台适配器
├── tools/                   校验 / 编译 / 评估脚本
├── release/                 发布信息
└── docs/                    项目文档
```

## 文档

| 文档 | 说明 |
|---|---|
| [SKILL.md](SKILL.md) | Skill 入口（Agent 加载此文件） |
| [User Guide](docs/USER_GUIDE.md) | 使用指南 |
| [Installation](docs/INSTALLATION.md) | 安装部署 |
| [Architecture](docs/ARCHITECTURE.md) | 系统架构 |
| [Developer Guide](docs/DEVELOPER_GUIDE.md) | 开发规范 |
| [Branch Policy](docs/BRANCH_POLICY.md) | 分支与推送规范 |
| [Changelog](CHANGELOG.md) | 版本记录 |

## 适用人群

| 人群 | 场景 |
|---|---|
| **AI 创作者** | 动漫角色视频制作、提示词工程、角色设计 |
| **动画 / PV 团队** | 分镜预演、节奏编排、风格探索 |
| **独立开发者** | 个人作品展示、角色概念可视化 |

## License

MIT License

<div align="center">

**AnimePv-promt**

动漫角色视频提示词导演 · AI Agent Skill

*From character ideas to executable anime PV prompts.*

</div>
