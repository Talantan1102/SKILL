# 视觉规范 (v1)

每张卡片都继承的视觉契约。这里定义的是常量,而非参数 —— 品牌系列一致性来自于贴文之间严格统一的刚性规范。

## 配色

```
Card background:   #FFFFFF  /* 白色 —— 主画布,内容卡片 02+ 锁定不可改 */
Card border:       #E8E2D6  /* 暖灰,1px —— 用于在页面上勾勒卡片边缘 */

Tinted block bg:   #FAF5E8  /* 米色 —— 曾是 v0 的主背景,现降级为强调色 */
Primary ink:       #1F1B16  /* 暖调近黑色 —— 用于主视觉/标题文字 */
Secondary text:    #5A5246  /* 暖灰 —— 正文、说明文字 */
Tertiary text:     #8C7E68  /* 用于引子、页脚、弱化 UI */

Brand primary:     #B23A26  /* 赭红 —— 关键术语、装饰、主要强调色 */
Brand deep:        #8C2A1B  /* 更深的赭红 —— 在 V2 暗色模式下用作封面块背景 */
Brand secondary:   #D4A017  /* 深琥珀色 —— 装饰性星形、手绘环线、"关键" 贴纸 */
Amber-on-tint text:#8B6809  /* 用于琥珀色背景上文字的更深琥珀色(用于对比度) */

Border / divider:  #1F1B1622 /* 主墨色 13% 透明度 —— 发丝细线 */
Inner box border:  #1F1B1625 /* 主墨色 15% 透明度 —— 微弱的盒子轮廓 */
Dashed brand:      #B23A26 with stroke-dasharray —— 模块盒、草图轮廓 */

/* 仅用于封面的扩展(不要用在内容卡片上) */
Cover dark bg:     #1F1B16  /* 海报模式背景,满版出血 */
Cover cream-on-dark:#F5EDDC  /* 背景为深色时的主视觉文字颜色 */
Cover dim-on-dark: #8C7E68  /* 深色背景上的次级文字 —— 与浅色模式下的三级文字相同 */
```

颜色使用规则:
- **赭红 (Terracotta)** 是主品牌色:引子分隔线、标题中的关键术语、负面 bullet 的 ×号、权衡三角形、示意图箭头、虚线模块边框。
- **琥珀色 (Amber)** 仅用于装饰:手绘星形、强调词周围的手绘椭圆、"关键" 浮窗贴纸的背景/边框。绝不用于正文或结构性线条。
- **米色 (Cream)** 用于白色卡片内的浅色块:"现状" 盒子、模块盒背景、示意图终端容器。
- 绝不在彩色背景上使用纯黑 `#000000` 或纯白文字。

## 字体规范

只用两套字族:
- **无衬线 Sans**(默认):正文、主视觉、标题、数字、模块名
- **衬线斜体 Serif italic**(`var(--font-serif)` + `font-style: italic`):引子、示意图说明、章节标签("→ XXX" / "~ XXX")、权衡行、数据流注解、"关键" 浮窗标签

只用两个字重:
- **400**(常规):正文、描述、说明
- **700**(粗体):主视觉、标题、模块名、统计数字、bullet 强调

完全跳过 600。跳过一个字重比逐级递增能营造更清晰的层级。

### 字号系统

```
Cover hero (number / arrow):  72-96px / 700 / line-height 0.92 / letter-spacing -0.03em
Cover hero (logo / wordmark): 64-90px / 700 / line-height 0.95 / letter-spacing -0.02em
Cover hero (text-on-schematic): 30-36px / 700 / line-height 1.1 (仅当示意图作为锚点时使用)
Card title:              21-23px / 700 / line-height 1.2 / letter-spacing -0.01em
Gist line:               12px / 500 / 品牌红色
Body / intro paragraph:  11-12px / 400 / line-height 1.55
Bullet list:             10.5-11px / 400 / line-height 1.55-1.6
Module name (in box):    11px / 700
Module description:      10px / 400 / line-height 1.4
Schematic label (inside):10-11px / 400 / 衬线斜体 / 填充主墨色
Schematic caption (below):9-10px / 400 / 衬线斜体 / 填充次级文字色
Section label:           10px / 400 / 衬线斜体 / tracking 0.05em / 品牌红 或 琥珀色
Kicker:                  11px / 400 / 衬线斜体 / tracking 0.05em
Stat label:              10px / 400 / 衬线斜体 / tracking 0.05em
Stat number:             17-18px / 700
Trade-off line:          11px / 400 / 衬线斜体 / 次级文字色
Data-flow note:          10px / 400 / 衬线斜体 / 次级文字色(带红色标记前缀)
Corner page number:      70-78px / 700 / 衬线 / 描边(text-stroke)/ opacity 0.4-0.5
```

## 卡片框架(封面与所有内容卡片共用)

```
aspect-ratio:    3 / 4
background:      #FFFFFF
border:          1px solid #E8E2D6
border-radius:   8px
padding:         22px 22px 18px 22px
position:        relative
overflow:        hidden
display:         flex
flex-direction:  column
```

始终使用 `box-sizing: border-box;`。在权衡行上使用 `margin-top: auto;` 把它推到卡片底部。

## 封面锚点系统 (v2)

**凌驾于一切之上的唯一规则:**封面必须在小红书信息流中以 200px 宽度显示时仍能阅读。如果视觉主元素在那个尺度下消失,封面就失败了。测试方法:打开 HTML,浏览器缩放至 25% —— 你能否仅凭封面就判断出贴文讲什么?

### 必选:1 个视觉锚点(三选一)

**锚点 (a) —— 数字锚点**

一个大数字、箭头、或前后对比对。当贴文有可量化的硬指标结果时使用。

- 数字:80-96px,字重 700,line-height 0.92
- 箭头 `→` 用品牌红渲染,与数字同一尺寸级别
- 占据卡片面积 ≥ 25%
- 通常占据封面整个垂直中心

**锚点 (b) —— Logo 块**

一个品牌 / 框架 / 模型名作为大字标(wordmark),通常放在彩色块内或作为深色/海报封面的中心主体。当贴文围绕一个具名系统(DeepSeek V4、SGLang、GRPO 等)、或没有单一主视觉数字时使用。

- 字标文字:64-90px,字重 700
- 颜色:深色 `#1F1B16` 背景上的米色 `#F5EDDC`,或米色块上的主墨色,或混合(一个词用主墨色,版本/版次用品牌红)
- 块填充或满版出血背景覆盖卡片高度 ≥ 30%
- 允许加一道斜条纹 / 角块作为次级强调

**锚点 (c) —— 示意图露脸**

一张极简的架构图 / 数据流图,带手绘感。当贴文的钩子就是机制本身(钩子 C 和 D)、且没有单一主导数字时使用。

- 最小尺寸:100×80px(占据卡片右侧或中央条带)
- ≥ 3 个带标签的元素(盒子、箭头或层叠形状)
- 描边 1px 品牌红,说明用衬线斜体,连接线为虚线
- 主视觉文字缩小到 30-36px,为示意图腾出空间

### 必选辅助元素(每张封面都要)

- **引子行** + 其下方 32×1.5px 的品牌红分隔线(左上角)
- **阅读时间戳**置于底部(`读完约 X 分钟`,按内容总字数 ÷ 300 + 0.3 分钟/张卡片估算;对于仅渲染封面或草稿场景,先按计划卡片数给一个占位估值,等内容卡片做出来后再修订)

### 可选辅助元素(选 1–2 个,不要更多)

- **描边卷号**(右上角)—— font-size 70-78px,text-stroke 1px,浅色背景下 opacity 0.4,深色背景下 opacity 0.25。**可选**,不能当作锚点。
- **斜条纹**(角部)—— 品牌红,6-8px 宽,30°-45° 倾角,从一条边切入封面。替代 v0 的 3 条横杠堆叠。
- **作者签名 pill** —— 左下角,仅封面使用。`谭磊 · 类目` 用三级文字色,前缀加品牌红圆点。
- **版次 / 系列标记** —— 比如 `Vol.01` 或 `note 02 / 04`,衬线斜体,三级文字色。

### 封面禁用项

- 把 v0 的 3 条横杠下降堆叠当作主视觉 —— 单独使用并不能锚定画面
- 居中、纯文字、无锚点 —— "Notion 截图" 失败模式
- 主视觉文字小于 60px 且没有其他锚点元素
- 把卷号当锚点(它是装饰)
- 多色主视觉(只允许一种强调色 —— 品牌红或深底米字,不要两者并存)

**内容卡片不放作者签名。**小红书 app 已经在贴文旁边显示作者 ID;每张卡片都打一遍是冗余。封面可以用上面那个可选 pill 显示。

## 内容卡片装饰

内容卡片去掉:
- 装饰 4(3 条横杠堆叠)—— 仅封面专用花活
- 装饰 5(阅读时间)—— 由权衡行替代

内容卡片增加 v1 的手绘 / 俏皮元素词汇表(每张卡片用 3–5 个):

### 元素词汇表(克制使用,每张卡片最多 5 个)

| 元素 | 何时使用 | 实现 |
|---|---|---|
| **波浪下划线** | 在标题中某个关键短语下方(通常是强调色术语) | `<svg viewBox="0 0 65 8"><path d="M 1 5 Q 10 1 20 5 T 40 5 T 64 5" stroke="#B23A26" stroke-width="1.6" fill="none"/></svg>`,绝对定位在文字下方 |
| **琥珀色星星** | 章节标签旁,或作为浮窗上的贴纸 | 五边形星形 SVG path,填充 `#D4A017`,9–14px |
| **手绘椭圆** | 圈住标题中某个关键词 | `<svg viewBox="0 0 42 22"><path d="M 5 11 Q 2 4 21 3 Q 39 4 38 11 Q 37 19 21 19 Q 4 19 5 11 Z" stroke="#D4A017" stroke-width="1.4" fill="none"/></svg>`,绝对定位在文字后方,`z-index: -1` |
| **手绘 × 号 bullet** | 负面调性列表的项目符号("hidden costs"、"踩坑"、"不适用") | `<svg viewBox="0 0 9 9"><path d="M 1 1 L 8 8 M 8 1 L 1 8" stroke="#B23A26" stroke-width="1.4"/></svg>`,9px |
| **手绘环线高亮** | 圈住示意图中的关键元素("vector store" 标注) | 不规则的闭合贝塞尔曲线,`stroke="#D4A017"`,1.2px |
| **贴纸倾斜** | 仅对一个元素使用 —— 通常是带底色的浮窗框 | `transform: rotate(-0.6deg)` 到 `rotate(-0.7deg)` |
| **虚线边框** | 模块盒(架构卡片) | `border: 0.8px dashed #B23A26` |

不要把 7 种全堆在一张卡上。挑 **3–5** 个契合内容形态的:
- 概念卡 + bullet 列表:波浪下划线 + 星星 + ×号 bullet + 倾斜浮窗框(4 个)
- 架构卡:关键词上的手绘椭圆 + 虚线模块边框 + 贴纸浮窗(3 个元素;模块算作一种重复元素)
- 对比卡:左侧 ×号 bullet + 右侧表头波浪下划线(2 个元素;克制用在这里恰到好处,对比本身就是视觉)

## 章节标签约定

章节标签出现在卡片内部,用于切分内容。两种风格,按调性挑选:

- **`→ XXX`** —— 中性 / 结构性章节("→ 现状"、"→ 4 个隐藏成本"、"→ 关键"、"→ 数据流")
- **`~ XXX`** —— 较柔和 / 随意的章节("~ 现状"、"~ 顺手记一下"),用于便利贴风格的盒子

两者都是衬线斜体 10px,letter-spacing 0.05em,颜色根据强调程度选 `#B23A26`(红)或 `#8C7E68`(灰)。

当章节标签搭配星形图标(`<svg>` 9px 琥珀色)时,把星星放在标签文字的左侧。

## "数据流注解"(用于架构卡片)

v1 引入的新结构性元素:在模块盒**下方**的一行衬线斜体注解,前缀为红色 `~ 数据流` 标签,概括这些模块在运行时如何协作。

```html
<div style="margin-top: 8px; font-family: var(--font-serif); font-style: italic;
            font-size: 10px; color: #8C7E68; line-height: 1.5;">
  <span style="color: #B23A26; letter-spacing: 0.05em;">~ 数据流</span>
  &nbsp;
  {一行话描述模块运行时如何相互喂数据}
</div>
```

这把一张静态结构图转化为动态心智模型 —— 读者看到的不仅是"零件是什么",还有"它们实际上怎么协同工作"。架构卡片必备;若概念涉及多个协作子部分,概念卡片可选。

## "关键" 浮窗(贴纸样式)

当一张卡片需要在正文末尾落定一句要点时,用倾斜的琥珀色贴纸:

```html
<div style="padding: 7px 11px 7px 12px; background: rgba(212,160,23,0.13);
            border: 1px solid #D4A017; border-radius: 4px;
            transform: rotate(-0.6deg); position: relative;">
  <svg width="14" height="14" viewBox="0 0 14 14"
       style="position: absolute; top: -7px; left: -6px;">
    <path d="M 7 1 L 8 5.5 L 12.5 5.5 L 9 8 L 10 12.5 L 7 10 L 4 12.5 L 5 8 L 1.5 5.5 L 6 5.5 Z"
          fill="#D4A017" stroke="#D4A017" stroke-width="0.5"/>
  </svg>
  <span style="font-family: var(--font-serif); font-style: italic;
               font-size: 10px; color: #8B6809; letter-spacing: 0.05em;
               font-weight: 700;">关键</span>
  <span style="font-size: 11px; color: #1F1B16; font-weight: 500;
               margin-left: 6px;">{要点,8-16 字}</span>
</div>
```

克制使用:每张卡片最多一个 "关键" 贴纸。建议用于架构卡片和总结卡片。

## 示意图 SVG 视觉语言

当卡片嵌入示意图(概念卡片的迷你图等):

- viewBox 通常 `0 0 280 X`
- 描边宽度:形状 0.5–0.8px,箭头 0.6–0.8px。发丝细。
- **连接线用虚线**(`stroke-dasharray="2 2"`)表达"数据流"或"摄入"语义 —— 比蓝图更像笔记本。
- 盒子:`fill="none"`(空心)或 `fill="#FAF5E8"`(米色填充)
- 箭头:品牌红 0.8px 描边 + 6px 多边形箭头。绝不在 SVG 内部使用 unicode `→`。
- 标签:衬线斜体,9–11px,说明用 `fill="#5A5246"`,盒内标签用 `#1F1B16`
- 加上**一个**手绘环线高亮(琥珀色,不规则贝塞尔路径)指引视线到关键元素

## 权衡行(可信度乘数,沿用 v0)

与 v0 相同:

```html
<div style="margin-top: auto; display: flex; align-items: center; gap: 6px; padding-top: 8px;">
  <svg width="11" height="11" viewBox="0 0 11 11" style="flex-shrink: 0;">
    <polygon points="5.5,1.2 9.8,9.8 1.2,9.8" fill="none"
             stroke="#B23A26" stroke-width="0.9"/>
    <line x1="5.5" y1="4.5" x2="5.5" y2="7.2"
          stroke="#B23A26" stroke-width="0.9" stroke-linecap="round"/>
    <circle cx="5.5" cy="8.5" r="0.55" fill="#B23A26"/>
  </svg>
  <span style="font-size: 11px; color: #5A5246;
               font-family: var(--font-serif); font-style: italic;">
    代价 · {权衡文字,8-16 字}
  </span>
</div>
```

在 v1 布局中,这是**卡片上最后一个可见元素**(页脚已被移除)。用 `margin-top: auto;` 把它推到底部。

如果一张卡片没有真实的权衡,就省略。强行硬编的权衡会读起来像假谦虚。

## 图标用法(lucide 库)

与 v0 相同 —— lucide outline 图标,品牌红,描边 1.6px,尺寸 12/14/15/16px。手绘图标保留给品牌专用符号(警示三角、琥珀色星星贴纸)和示意图基础图元。

## 信息密度目标

v1 内容卡片的正文必须包含 **220–300 中文字符等价词**的实质内容,不计入引子、页码、标题、gist 和权衡行。低于 220 读起来像凑数。高于 300 在 3:4 比例下会塞得过满。

密度不仅是字数 —— 而是**具体性**。每张卡片必须包含 ≥ 6 个具体数据点(数字、具名工具、具体场景、前后对比)。一张 280 字但 0 个具体点的卡片不及格;一张 240 字但有 8 个具体点的卡片合格。详见 SKILL.md 的"密度底线"正式清单。

各卡片类型的具体内容元素:
- **概念卡**:标题 + gist + 浅底色 intro 框(2-3 行)+ 示意图 + N 项 bullet 列表(4-6 项,每项**括号内带 2 个具体点**)+ 权衡
- **架构卡**:标题 + gist +(可选)intro 行 + 3-6 个模块盒(每个**结构化的 2 字段细节**)+ 数据流注解 +(可选)关键浮窗 + 权衡。如果模块用了密集的 2 字段模式,intro 行和关键浮窗就变成可选 —— 模块本身已经承载了实质内容。
- **对比卡**:标题 + gist + 2 列(每列 4-5 项,每项**至少 1 个具体点**)+ 权衡
- **踩坑卡**:标题 + gist + 看起来/实际(或 以为/结果)对照面板 —— 实际面板必须**至少 3 个具体点** + 权衡
- **总结卡**:标题 + gist + 适用/不适用 列表(每项括号内带原因)+ 权衡
- **代码卡**:标题 + gist + 代码块 + 2-3 个**带具体点的**注解 bullet + 权衡

## 间距节奏

垂直节奏使用以下数值,按优先级排序:
- 4px、6px、8px、10px、12px、14px、16px、18px、22px

避免奇数值(如 11px、19px)。避免任意像素值(如 17px)。
