# 角色设定卡与出图 Prompt 模板

## 1. 角色设定卡（Step0-1 输出）

```
【角色设定卡】
- 角色类型：女性 / 男性 / 其他
- 姓名/代称：
- 年龄/体态：
- 发型：
- 发色：
- 瞳色/眼神：
- 服装：
- 配饰：
- 气质/性格锚定：
- 画风元素（Base Style 锚点，默认 modern-cel）：日本动画 / 日本 JRPG 角色设计语法、扁平色块、明确日式手绘描边、硬边高光；
  其他 2D base style 见 core/style-anchor.md
- 角色设定图比例：<角色设定图比例，默认建议 4:5>
- 视频时长与画幅：待 Step2 单独确认，不写入角色 DNA
```

## 2. 角色设定图 Prompt（角色风格确认后立即输出）

````
提示词（文生图）：
<角色设定卡要点>，<Base Style 英文锚定，默认 modern-cel；见 core/style-anchor.md>，
Japanese anime character design, Japanese mobile / console JRPG character concept art,
Japanese TV anime facial proportions, pure 2D hand-drawn cel animation, clean Japanese anime lineart,
flat color blocks, hard-edged cel shadows, expressive anime eyes, Japanese game character sheet,
<姿态/构图描述>，画面比例 <角色设定图比例>，高质量，日系动画与日系 JRPG 视觉语言（默认；非日系 base 按锚定替换）。

必须追加的风格锁定：

```text
默认优先呈现日本动画与日本 JRPG 角色设计语法：日系脸部比例、日系眼睛与五官、日式手游角色立绘、
日式主机 JRPG 概念设定稿、手绘赛璐璐线稿、二维动画关键帧质感。
默认禁止欧美卡通比例、美国动画造型、迪士尼风、Pixar 风、DreamWorks 风、欧美漫画风、超级英雄漫画风、
粗重矢量卡通线、橡皮管动画、3D CGI、三维建模、写实摄影感。
若 base = western-comic，则允许美漫脸部比例与夸张动态，改禁日系赛璐璐混搭；
完整禁止项按 core/style-anchor.md 对应 base style 执行。
```

建议参数：
- 模型：seedream5.0Lite（豆包）
- 角色设定图比例：<角色设定图比例，默认 4:5>
- 视频比例：待 Step2 `SESSION_SPEC` 确认
- 数量：建议 2-4 张供挑选
````

> 出图动作需用户二次确认后，由用户自行前往豆包生成。

## 3. 通用基础固定参数（所有主题 Prompt 的开头锚定）

```
画面风格：<默认 modern-cel：日本动画与日本 JRPG 角色设计语法，90年代日系赛璐璐动画，纯手绘黑硬轮廓线，
大面积平涂上色，几何块状硬边阴影，无渐变溢色、无写实PBR材质、无高斯运动模糊；
12fps有限动画，关键帧定格设计，轻微35mm胶片颗粒、微量手绘线条抖动，复古TV动画质感；
其他 2D base style 替换为 core/style-anchor.md 对应中文锚定>
画幅分辨率：<角色设定图比例> / 4K超清
核心规则：所有动态依靠手绘速度线、残影、形体形变表现，拒绝现代写实动态模糊；
镜头以2.5D平面运镜为主，无3D环绕、无大幅度空间位移

默认日系视觉强化：Japanese anime key visual, Japanese JRPG character art, Japanese mobile game illustration,
anime facial anatomy, anime eyes, clean delicate Japanese lineart, cel-shaded flat colors.
默认禁止：NO western cartoon, NO American animation, NO Disney-like style, NO Pixar-like style, NO DreamWorks-like style,
NO western comic-book style, NO superhero comic style, NO exaggerated western facial anatomy,
NO thick vector cartoon outlines, NO rubber-hose animation, NO 3D CGI, NO rendered 3D model.
非日系 base 按 core/style-anchor.md 替换视觉强化与禁止项（如 western-comic 反向）。
```


