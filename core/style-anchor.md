# 2D 风格锚定语模板库

P0 支持 7 个 2D base style。每个 base style 是一套完整的
「画风锚定 + 专属禁止项」，选定后必须贯穿全部镜头与角色图 Prompt。

## 风格锁定铁律

1. **Base Style 一经选定，全片不可切换**。2D 赛璐璐中途变厚涂 / 美漫 = 直接失败。
2. 默认 base = `modern-cel`，并读取 `references/默认动漫审美.md` 作为面向中文用户的日式动漫角色审美补充；用户指定其他 2D base style 时，以用户选择和本文件对应锚定为准。
3. 所有 base 都是**纯 2D 动画**；禁止 3D 渲染、三维模型、真人摄影、PBR 材质、实拍运镜。
4. Special / Premium 层可叠加，但不得改变 base 的线条与渲染方式。

## 锚定选择表

| Base Style | 中文名 | 画风锚点 | 线条 | 光影 | 动态 |
|---|---|---|---|---|---|
| modern-cel | 现代赛璐璐 | 日系动画 / JRPG | 干净日式线稿 | 平涂硬边 | 12fps 有限动画 |
| retro-cel | 复古赛璐璐 | 90s 日系 TV 动画 | 手绘黑线 | 色块 + 网点 | 12fps 有限动画 |
| painterly-anime | 厚涂动画 | 半写实日系 / 国创大电影 | 软边或无描边 | 笔触渐变 | 24fps 全动态 |
| watercolor-ink | 水彩国风 | 水墨 / 淡彩 | 写意水墨线 | 透明水彩留白 | 12-24fps 有限动画 |
| vector-flat | 矢量潮流 | 扁平矢量 / 海报 | 均匀矢量线 | 平涂 + 渐变网格 | 12-24fps 矢量运动 |
| korean-manhwa | 韩漫 | 韩系条漫 / 手游 | 纤细精致线稿 | 喷枪渐变 + 高光 | 24fps 有限动态 |
| western-comic | 美漫 | 美式漫画 / 卡通 | 粗犷墨线 | 网点 + 排线 | 12-24fps 夸张动态 |

---

## 通用 2D 约束（所有 base style 共用）

```
Style anchor (apply to all shots):
 pure 2D animation,
 NO 3D CGI, NO rendered 3D model, NO PBR material,
 NO realistic photography, NO live action camera movement.

Camera limited to 2.5D planar motion
 (fixed position, slow push/pull, horizontal parallax pan,
 small-angle orbit <= 45 degrees),
 NO 3D free-form orbit, NO large spatial displacement.

Character DNA locked across all shots:
 face, hairstyle, outfit, accessories, signature items unchanged.
```

```
画面风格：纯二维动画，禁止3D渲染、三维建模、真人摄影感、写实PBR材质、实拍运镜。
镜头以2.5D平面运镜为主：固定机位、慢推慢拉、视差横移、小角度环绕≤45度，
无3D自由环绕、无大幅度空间位移。
角色DNA全程锁定：脸型、发型、服装、配饰、标志物不可变化。
```

---

## modern-cel（默认）

### 核心锚定语（英文 H3 输出）

```
Style anchor (apply to all shots):
 Japanese anime and Japanese JRPG visual language,
 Japanese TV anime character design, Japanese mobile / console JRPG key visual,
 Japanese anime facial proportions, expressive anime eyes,
 cel-shading anime, 90s Japanese retro animation,
 clean black hand-drawn outlines,
 flat color blocks,
 hard-edged geometric shadows,
 12fps limited animation,
 keyframe freeze-frame design,
 subtle 35mm film grain,
 minimal hand-drawn line jitter.

NO realistic rendering,
NO Gaussian motion blur,
NO fluid simulation effects,
NO western cartoon style,
NO American animation style,
NO Disney-like style,
NO Pixar-like style,
NO DreamWorks-like style,
NO western comic-book style,
NO superhero comic style,
NO exaggerated western facial anatomy,
NO thick vector cartoon outlines,
NO rubber-hose animation,
NO 3D CGI,
NO rendered 3D character model.

All motion expressed via hand-drawn speed lines,
discrete afterimages,
and squash-and-stretch deformation.
```

### 中文锚定

```
画面风格：面向中文二次元用户审美的现代日式动漫角色设计，日本动画与日本 JRPG 视觉语言，日式手游/主机 JRPG 角色设计，
日系脸部比例与动漫眼睛，90年代日系赛璐璐动画，纯手绘黑硬轮廓线，
大面积平涂上色，几何块状硬边阴影，
无渐变溢色、无写实PBR材质、无高斯运动模糊；
12fps有限动画，关键帧定格设计，
轻微35mm胶片颗粒、微量手绘线条抖动，
复古TV动画质感
```

### 专属禁止项

```
NO western cartoon, NO American animation,
NO Disney-like style, NO Pixar-like style, NO DreamWorks-like style,
NO western comic-book style, NO superhero comic style,
NO exaggerated western facial anatomy,
NO thick vector cartoon outlines, NO rubber-hose animation,
NO 3D CGI, NO rendered 3D character model,
NO realistic rendering, NO motion blur, NO fluid effects.
```

```
禁止欧美卡通风、美国动画风、迪士尼风、Pixar 风、DreamWorks 风、欧美漫画风、超级英雄漫画风、
夸张欧美脸部比例、粗重矢量卡通线、橡皮管动画、3D CGI、三维建模、真人摄影感、写实皮肤、
电影级光影、景深、真实材质、写实特效、高斯运动模糊、流体特效。
```

---

## retro-cel

### 核心锚定语（英文 H3 输出）

```
Style anchor (apply to all shots):
 90s Japanese retro anime cel animation,
 Japanese JRPG character concept art language,
 film grain texture,
 halftone shading,
 limited palette,
 12fps limited animation,
 hand-drawn speed lines and discrete afterimages,
 keyframe freeze-frame design.

NO western cartoon style,
NO American animation style,
NO modern motion blur,
NO digital gloss,
NO 3D CGI.
```

### 中文锚定

```
画面风格：90年代日系复古赛璐璐动画，日式主机JRPG概念设定语言，
胶片颗粒质感，网点阴影，克制色板，12fps有限动画，
手绘速度线与离散残影，关键帧定格设计。
```

### 专属禁止项

```
NO western cartoon, NO American animation,
NO modern motion blur, NO digital gloss, NO 3D CGI.
```

```
禁止欧美卡通风、美国动画风、现代运动模糊、数码光泽、3D CGI。
```

---

## painterly-anime（厚涂动画）

### 核心锚定语（英文 H3 输出）

```
Style anchor (apply to all shots):
 semi-realistic 2D painted anime style,
 painterly brushwork with soft color transitions,
 layered lighting with soft shadows and subtle rim light,
 thin soft linework or line-less rendering,
 premium Chinese / Japanese animated film quality,
 fluid 24fps 2D animation,
 slight motion smear kept hand-painted.

NO cel-shading flat color blocks,
NO hard-edged geometric shadows,
NO thick clean ink outlines,
NO realistic photography,
NO PBR material,
NO 3D CGI,
NO live action camera movement.
```

### 中文锚定

```
画面风格：半写实厚涂二维动画，柔和笔触过渡，层次光影与边缘光，
细软描边或无线稿，国创/日系动画大电影质感，24fps全动态，
轻微手绘动态拖尾，禁止写实摄影感。
```

### 专属禁止项

```
NO cel shading, NO flat color blocks,
NO hard-edged shadows, NO thick clean ink outlines,
NO realistic photography, NO PBR material,
NO 3D CGI, NO live action camera.
```

```
禁止赛璐璐平涂色块、硬边几何阴影、粗黑干净线稿、
真人摄影感、写实PBR材质、3D CGI、实拍运镜。
```

---

## watercolor-ink（水彩国风）

### 核心锚定语（英文 H3 输出）

```
Style anchor (apply to all shots):
 Chinese ink-and-watercolor 2D animation,
 translucent watercolor washes,
 expressive ink-brush linework,
 paper grain texture,
 negative-space composition,
 restrained ethereal color palette,
 12fps limited animation with hand-drawn flow.

NO hard cel shading,
NO flat color blocks,
NO thick clean anime outlines,
NO heavy impasto texture,
NO realistic rendering,
NO western cartoon style,
NO 3D CGI.
```

### 中文锚定

```
画面风格：水墨淡彩二维动画，透明水彩晕染，写意毛笔线条，
纸纹颗粒，留白构图，克制清雅的色板，12fps有限动画手绘流动。
```

### 专属禁止项

```
NO hard cel shading, NO flat color blocks,
NO thick clean anime outlines, NO heavy impasto,
NO realistic rendering, NO western cartoon, NO 3D CGI.
```

```
禁止硬边赛璐璐阴影、平涂色块、粗重干净动画描边、厚重油彩、
写实渲染、欧美卡通风、3D CGI。
```

---

## vector-flat（矢量潮流）

### 核心锚定语（英文 H3 输出）

```
Style anchor (apply to all shots):
 clean vector 2D animation,
 flat graphic color fields,
 smooth uniform outlines,
 limited bold palette,
 poster-grade composition,
 kinetic typography and graphic UI accents,
 12-24fps vector motion design.

NO painterly brush texture,
NO watercolor wash,
NO airbrush gradient shading,
NO photo texture,
NO realistic rendering,
NO 3D CGI,
NO thick cel-style anime lineart.
```

### 中文锚定

```
画面风格：干净矢量二维动画，扁平图形色块，平滑均匀描边，
克制的醒目色板，海报级构图，动态排版与图形UI点缀，
12-24fps矢量运动设计。
```

### 专属禁止项

```
NO painterly brush texture, NO watercolor wash,
NO airbrush gradient, NO photo texture,
NO realistic rendering, NO 3D CGI,
NO thick cel-style anime lineart.
```

```
禁止笔触纹理、水彩晕染、喷枪渐变、照片纹理、
写实渲染、3D CGI、粗重赛璐璐动画描边。
```

---

## korean-manhwa（韩漫）

### 核心锚定语（英文 H3 输出）

```
Style anchor (apply to all shots):
 Korean manhwa / webtoon-inspired 2D animation,
 fine delicate lineart,
 airbrush gradient shading with glossy highlights,
 elegant elongated proportions,
 clean luminous faces,
 soft romantic lighting,
 24fps limited animation with subtle motion.

NO hard cel shading,
NO flat color blocks,
NO thick outlines,
NO painterly heavy texture,
NO western exaggerated cartoon anatomy,
NO realistic photography,
NO 3D CGI.
```

### 中文锚定

```
画面风格：韩漫/条漫感二维动画，纤细精致线稿，喷枪渐变光影与光泽高光，
修长优雅身形比例，干净明亮的五官，柔和浪漫布光，24fps有限动态。
```

### 专属禁止项

```
NO hard cel shading, NO flat color blocks,
NO thick outlines, NO painterly heavy texture,
NO western exaggerated cartoon anatomy,
NO realistic photography, NO 3D CGI.
```

```
禁止硬边赛璐璐阴影、平涂色块、粗重描边、厚重笔触、
欧美夸张卡通造型、真人摄影感、3D CGI。
```

---

## western-comic（美漫）

> 唯一允许欧美脸部比例与夸张动态的 base style。使用该风格时，
> 所有「禁止欧美卡通」的默认规则反转，改为禁止日系/韩系混搭。

### 核心锚定语（英文 H3 输出）

```
Style anchor (apply to all shots):
 western comic-book 2D animation,
 bold expressive ink linework,
 halftone dots and dramatic hatching,
 dynamic exaggerated anatomy and foreshortening,
 comic panel language with action lines and onomatopoeia,
 12-24fps snappy animated motion.

NO Japanese anime facial proportions,
NO cel-shading flat anime colors,
NO korean manhwa airbrush gradients,
NO painterly realistic rendering,
NO realistic photography,
NO 3D CGI.
```

### 中文锚定

```
画面风格：美式漫画风二维动画，粗犷表现力墨线，网点与排线阴影，
夸张动态人体与透视，漫画分格语言、动作线与拟声字，
12-24fps利落动态。
```

### 专属禁止项

```
NO Japanese anime facial proportions,
NO cel-shading flat anime colors,
NO korean manhwa airbrush gradients,
NO painterly realistic rendering,
NO realistic photography, NO 3D CGI.
```

```
禁止日系脸部比例、赛璐璐平涂动画配色、韩漫喷枪渐变、
厚涂写实渲染、真人摄影感、3D CGI。
```

---

## Motion Comic（动态漫画处理层）

动态漫画是**呈现方式**而非画风，可作为 Special Layer 叠加在任意 2D base style 上：

```
Motion comic presentation layer:
 comic panel layouts with dynamic panel cuts,
 illustrated stills brought alive by camera push / pull and parallax,
 onomatopoeia and action lines animated in 2D,
 limited frame animation for poses and expressions.
```

```
动态漫画处理层：漫画分镜面板与动态切格，
插画静止画面通过推拉与视差动起来，
拟声字与动作线二维动画化，
pose与表情使用有限帧动画。
```


