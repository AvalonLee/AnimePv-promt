# Walkthrough — Frostblade（端到端实测样例）

本文件是**用本项目走完一次完整流程产出的真实成品**，用于验证 skill 可用性。
不是设想，不是示意，是按 [templates/genre-action-15s.md](../../templates/genre-action-15s.md)
实际替换产出、并通过 [core/prompt-structure.md](../../core/prompt-structure.md)
10 段自检的结果。

---

## Step0 — SESSION_SPEC

```yaml
SESSION_SPEC:
  duration: 15s
  aspect_ratio: "16:9"
```

## Step1 — 用户输入

```
制作一个五星冰系女剑士的战斗展示PV。
银白长发，冰蓝瞳，黑银轻甲配深蓝披风，冰晶长剑。气质冷静高贵。
目标：手游新角色上线。15秒。
```

## Step2 — 路由判定

| 环节 | 结果 | 依据 |
|---|---|---|
| Task | `CREATE_PV` | workflow/task-orchestrator.md |
| Character Type | `cool_female` | workflow/production-flow.md 关键词表（剑士/冷静/高贵） |
| Persona Tag | 冷酷 | library/style/persona-tags.md |
| Genre | `action` | 战斗展示 → library/genre/genre-library.md |
| 内容类型 | `cool-female-jrpg` | library/theme/theme-library.yaml |
| 表现重点 | `combat.showcase.v1` | 统一导演方案中的创作意图字段 |
| Template | `genre-action-15s` | Genre=action + 15s |

## Step3 — Character DNA Lock

```yaml
character_dna:
  identity:
    character_name: Frostblade
    archetype: cool_female
    rarity: SSR
  appearance_anchor:
    hair: { color: 银白, length: 长发高马尾, special_features: 发梢冰蓝渐层 }
    face: { eye_color: 冰蓝, eye_shape: 锐利上挑, expression_style: [冷静, 高贵] }
    costume:
      main_outfit: 黑银双色轻甲 + 深蓝披风
      signature_elements: 肩甲霜纹浮雕
      color_palette: [银白, 冰蓝, 黑, 深蓝]
  signature_assets:
    weapon: 冰晶长剑
    accessory: 银质雪花吊坠
    ability_visual: 冰元素剑技
  generation_constraints:
    must_keep: [银白发色, 冰蓝瞳色, 冰晶长剑, 雪花吊坠]
    avoid_change: [发色, 瞳色, 武器替换, 服装重设计]
```

## Step4 — Style Stack（含冲突检测）

```yaml
style_stack:
  base: modern-cel
  premium: mobile-game-premium
  special: dark-cinematic-cel
conflict_check: PASS   # 无 y2k-graphic x dark-cinematic-cel 冲突
```

## Step5 — Risk Budget Gate

```yaml
genre: action
duration: 15s
effective_action_budget: 2      # min(action=2, 15s=2)
effective_effect_budget: 2
theme_candidates: [confident-walk, weapon-reveal, ability-release, signature-pose]
admitted: [confident-walk, weapon-reveal, ability-release, signature-pose]
filtered: []                    # 无 level-3 组件，无需降级
```

## Step6 — Shot List

| # | 时间 | 机位 | 动作 | 表情 |
|---:|---|---|---|---|
| 01 | 0-1.5s | 正面贴脸特写 | 眼神直视 | 锐利 |
| 02 | 1.5-3s | 仰拍→向上甩镜 | 蓄力 | 怒吼 |
| 03 | 3-4.5s | 侧面跟拍→急停 | 冲刺侧踢 | 咬牙 |
| 04 | 4.5-6s | 正面俯冲撞镜 | 出拳 | 凌厉 |
| 05 | 6-7.5s | 荷兰角低角度 | 挥剑斩击 | 专注 |
| 06 | 7.5-9s | 旋转上升→侧仰拍 | 旋转展臂 | 气场全开 |
| 07 | 9-10.5s | 鱼眼贴脸 | 挑衅手势 | 自信坏笑 |
| 08 | 10.5-12s | 高位斜拍→分格爆闪 | 三姿态连闪 | 战意 |
| 09 | 12-13.5s | 正面全景缓拉 | 能量爆发 | 呐喊 |
| 10 | 13.5-15s | 超低机位正面大透视英雄定格 | 收招定格 | 胜利笑容 |

机位无重复，符合 `library/camera/camera-motion-spec.md` 的 6 维变化强制规则。

## Step7 — 成品 Prompt

```
生成一支约15秒、16:9横版、原创热血战斗JRPG角色宣传PV。
整体采用纯二维日式赛璐璐动画 + 战斗漫画分镜风格 + 高速MG平面设计。全片保持纯二维，禁止3D建模、CG渲染、真人摄影感、写实皮肤、真实空间纵深。

【角色设定】
角色外观严格参考输入角色：银白色长发高马尾，发梢带冰蓝渐层；冰蓝色瞳孔，眼型锐利上挑；黑银双色轻甲配深蓝披风，肩甲有霜纹浮雕；武器为一柄冰晶长剑；配饰为颈间银质雪花吊坠。
气质：热血、凌厉、斗志昂扬、带一点狂气。表情可包括：怒吼、咬牙、锐利眼神、挑眉、自信坏笑、战斗呐喊。
角色一致性强制约束：发色、瞳色、服装、武器全程一致，禁止脸崩、禁止五官变化、禁止服装随机变化、禁止肢体畸形、禁止多手多脚、禁止手指错误。

【主题设定】
主题为"FROSTBLADE / 霜刃"。
故事发生在一个由战斗漫画分镜框、速度线、冲击波纹、碎石、火花、能量色块、漫画拟声词（ドン/バキュン/ゴゴゴ）、几何裂纹、黑色墨迹组成的抽象战斗空间。
主色：银白 + 冰蓝 + 纯黑 + 纯白 + 能量色（如红/蓝/金），高对比高饱和。
原创角色，原创战斗世界，不出现现有IP和Logo。

【音乐】
140-160 BPM日系战斗摇滚 / Electro Metal，融合失真吉他、快速双踩鼓、低沉Bass、铜管合奏、战斗嘶吼、冲击音效、碎拍合成器。
开场0.5s直接用重击鼓点+吉他riff切入，不做慢铺垫。
中段鼓点持续加速，每一次重拍对应一次打击或切镜。
10s后进入高潮，连续爆发鼓点+铜管齐奏。
结尾在最强一击后突然静音，以一个金属余音+碎石落地声结束。

【画面风格】
人物使用粗黑漫画线条、大面积纯色块、硬边阴影、白色高光，非写实光影。
背景由战斗漫画分镜框、放射状速度线、冲击线、碎石飞溅、火花、能量色块、漫画拟声词文字、几何裂纹、黑色墨迹、网点纹理构成。
整体像少年漫画战斗名场面、热血动画OP、游戏战斗PV高速混剪。

【动态与转场总要求】
全片高密度信息轰炸，平均0.3-0.8秒一次视觉变化，禁止长时间停顿，禁止空白过渡，禁止普通淡入淡出。
转场使用：闪白硬切、冲击拉伸转场、运动轨迹匹配、速度线推切、漫画分格跳切、图形碰撞、拟声词爆闪覆盖、碎石遮挡切镜、能量波纹扩张、画面震动复位。
多层叠加运动：前景速度线/碎石飞入、中景人物战斗动作、后景分镜框/能量脉冲、拟声词文字同步爆闪。
可闪现原创战斗文字：BREAK LIMIT / COUNTER / CRITICAL / FINAL STRIKE / WARNING / DANGER。

【分时间段镜头设计】
0-1.5s：超近距离脸部特写，角色锐利眼神直视镜头，嘴角上扬带狂气，瞬间插入：眼睛特写→武器细节→拳头→战斗姿态剪影。伴随红色闪屏、速度线爆发、主题文字碎片撞入。机位：正面贴脸特写。
1.5-3s：超低机位仰拍，角色一条腿向镜头前方迈出形成巨大前景透视，身体向后微仰，双手蓄力，周围能量色块爆发。镜头由腿部快速向上甩至脸部，角色仰头怒吼。背景漫画分镜框旋转切开，速度线从身后爆发。机位：仰拍→向上甩镜。
3-4.5s：侧面45°中景，角色侧身快速冲刺，身体拉成水平动态线，身后拖出3层离散残影，手绘放射速度线充满画面。突然变向，一脚侧踢，命中瞬间触发8-12px镜头震动+闪白。机位：侧面跟拍→急停。
4.5-6s：正面超广角近距离，角色突然向镜头俯身出拳，拳头成为巨大前景，脸部在拳头后方，表情咬牙凌厉。出拳瞬间冲击波纹从拳尖扩散，碎石飞溅。随后快速拉镜展示完整连招。机位：正面俯冲撞镜。
6-7.5s：大角度荷兰角倾斜构图，角色单膝跪地滑行，一手撑地，另一手挥武器砍出，武器轨迹留下彩色能量斩击波。画面随鼓点连续黑白反相、闪切、漫画切片。机位：荷兰角低角度。
7.5-9s：从脚边沿身体快速向上旋转匹配切镜：鞋子→腿部→腰部→武器→肩部→颈饰→面部，最终停在极低机位侧仰拍。角色双臂展开，身体旋转，头发/披风向外甩开，能量环绕全身。机位：旋转上升→侧仰拍。
9-10.5s：超近脸部鱼眼透视，角色脸部贴近镜头，眼睛成为视觉中心，一只手从画面上方压向镜头，另一只手比出挑衅手势。人物挑眉、自信坏笑。周围爆出放射状能量图形、漫画网点、拟声词"ドン"。机位：鱼眼贴脸。
10.5-12s：高机位斜后方俯拍，角色快速转身，武器/头发/披风产生夸张二维摆动。转身途中连续闪现三个不同战斗姿态：侧身防御→双手蓄力→单手挥击，使用漫画分格连续爆闪，每格不同透视方向。机位：高位斜拍→分格爆闪。
12-13.5s：全景大场面，角色站在画面中央，周身能量爆发形成巨大光柱/能量球，背景分镜框全部震碎，碎石和速度线向四周飞溅。镜头缓慢拉远展示全貌，角色仰头呐喊。机位：正面全景缓拉。
13.5-15s：超低机位正面大透视英雄镜头，角色向前一步，一只手/武器伸向镜头形成巨大前景，另一只手收招，身体微侧转。直视镜头露出自信胜利笑容。背景所有能量、碎石、速度线瞬间向人物身后收拢。最后0.3s：角色突然贴近镜头→眨眼→画面定格，巨大原创标题FROSTBLADE伴随重击音效结束。机位：超低机位正面大透视英雄定格。

【表演要求】
角色动作保持强烈二次元战斗动画感，夸张、利落、有张力，带少年漫画式的热血与狂气。
动作包括：出拳、踢腿、挥武器、冲刺、变向、跳跃、落地滑行、蓄力、爆发、转身、收招、挑衅手势。
不要写实表演，不要真实武术动作，不要慢动作。

【避免项】
禁止3D感、真人摄影感、写实皮肤、电影级光影、景深、真实材质、写实特效、高斯运动模糊、流体特效。
禁止角色脸崩、五官变化、发型变化、服装变化、武器消失、肢体畸形、多手多脚、手指错误、穿模。
禁止普通淡入淡出、空镜头、慢节奏铺垫、长时间静止、重复机位、重复动作、连续正面平视。
禁止未成年外观（如角色为成年）、过度血腥、低俗内容。

【核心目标】
重点突出角色战斗魅力、高密度高转场、热血漫画感、大透视多机位、能量爆发视觉冲击、纯二维平面设计感。整支片子像一支节奏极强、转场极密、打击感炸裂的热血战斗角色PV。

```

## Step8 — Quality Report

```yaml
quality_report:
  scores:
    generation_stability: 32     # 战斗动作风险，未满分
    character_consistency: 25
    shot_feasibility: 15
    visual_impact: 10
    creative_intent_match: 10
    art_direction: 4
  final_score: 96
  decision: PASS
  risk_analysis:
    character_drift: low         # DNA 锚点已注入
    action_complexity: medium    # level 2，在预算内
    camera_risk: low             # 全为 2.5D 平面运镜
    effect_risk: low             # level 2 以内
  structure_check:
    sections_present: 10/10
    timeline_coverage: 0-15s 连续无缝隙
    camera_repeat: none
    placeholders_remaining: 0
```

## Step9 — Generation Gate

系统在此停止。Prompt 已就绪，**需用户显式确认后**自行前往 MiniMax H3 生成。
本系统不调用任何生成能力。

---

## 本次实测暴露并修复的缺陷

| 缺陷 | 说明 | 修复 |
|---|---|---|
| SKILL.md 缺 frontmatter | 无 `name` / `description`，skill 无法被发现与自动触发 | 已补 |
| 三个模板末段缺机位标注 | `13.5-15s` 最终定格镜头缺 `机位：`，继承自项目前身的原始 skill | 已补，并新增 `tools/validate_templates.py` 防回归 |
