# AstraForge Studio · 星铸工坊

![Version](https://img.shields.io/badge/version-2.5.0-blue)

面向中文用户、以最终生成效果为优先的动漫角色视频提示词导演。

## 核心流程

1. 分步完善角色设定，确定固定特征与主视觉；
2. 规划视频创意、节奏、分镜、文字和声音；
3. 选择创意方向和表现策略，建立完整统一导演方案；
4. 执行结构校验、质量评分、自动修改和复检；
5. 选择平台、生成方式和素材；
6. 输出平台专用提示词、素材登记表和操作提醒。

项目只输出方案、提示词与参数，不主动生成图片或视频。

## 可执行的平台编译

```bash
python tools/compile_platform_prompt.py examples/platform-adapters/jimeng-i2va.yaml
python tools/compile_platform_prompt.py examples/platform-adapters/h3-ref2va.yaml
```

编译器会校验平台、生成方式和素材要求，再生成即梦或 H3 对应格式，不需要人工照着文档重新拼装。

五种生成方式采用不同编译策略。可先独立检查导演方案：

```bash
python tools/validate_director_plan.py examples/platform-adapters
python tools/evaluate_director_plan.py examples/platform-adapters/jimeng-i2va.yaml
```

## 设计重点

- 角色一致性优先；
- 动作视频使用能量曲线、节拍表、快切小镜头和独立生成片段；
- 文字可选择后期添加、模型直接生成或完全无文字；
- H3 输出遵循官方 `h3-prompt-writing` 的三字段和六字段规范；
- 案例库只强制要求原始提示词，其他证据全部可选。

详细使用方法见 [SKILL.md](SKILL.md)，案例流程见 [workflow/case-ingestion.md](workflow/case-ingestion.md)。
