# 开发指南

## 修改原则

1. 面向用户的文字使用直白中文。
2. 内部字段保持稳定，平台专属语法只存在于适配器和编译器。
3. 新流程必须落到可运行校验，不能只写文档。
4. 不引入营销目标、转化指标或广告专用流程。

## 新增平台适配器

1. 在 `platform-adapters/` 添加配置，声明平台、模式、输出字段和素材引用规则。
2. 在 `tools/compile_platform_prompt.py` 增加转换逻辑。
3. 在 `examples/platform-adapters/` 添加最小示例。
4. 在 `tools/validate_platform_adapters.py` 增加结构与真实编译校验。
5. 更新用户指南，并运行全量测试。

## 统一导演方案

输入应符合 `schema/director-plan.schema.yaml`。平台适配器只负责转换表达形式，不应重新决定角色设定、故事、分镜或节奏。

## 回归命令

```bash
python tools/check_effect_first_migration.py
python tools/validate_director_plan.py examples/platform-adapters
python tools/validate_execution_kernel.py
python tools/validate_quality_loop.py
python tools/evaluate_director_plan.py examples/platform-adapters/jimeng-i2va.yaml
python tools/validate_platform_adapters.py
python tools/validate_yaml.py
python tools/validate_templates.py
python tools/validate_benchmarks.py
python tools/validate_cases.py
python tools/check_version.py
python tools/check_links.py
```

提交前还应运行技能包结构校验和 `git diff --check`。
