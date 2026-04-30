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

## 示意图 — 首选路径:`excalidraw-diagram-generator`

对于 `concept` 和 `architecture` 卡片里非平凡的迷你示意图,**默认路径是把示意图生成委托给官方 `excalidraw-diagram-generator` skill**。它的手绘 `roughness` 渲染感与 v1 词汇(波浪线 / 星星 / × / 手绘椭圆)契合度远高于线条干净的 inline SVG。详细工作流见 `SKILL.md` 的 "把示意图委托给 excalidraw-diagram-generator" 一节。

### 给 excalidraw 元素的品牌色板映射

调用 `excalidraw-diagram-generator` 生成示意图时,**在描述里强制传以下颜色** —— 该 skill 尊重元素级 `strokeColor` / `backgroundColor` override:

| Excalidraw 角色 | 十六进制 | 用途 |
|---|---|---|
| 主线 | `#B23A26` (赭红) | 强调 / "我们的方案" / 强调框、箭头颜色、hero 块 |
| 副线 | `#1F1B16` (近黑) | 中性结构框、常规标签 |
| 浅填 | `#FAF5E8` (米色) | 盒底色 —— 与 inline SVG 米色填充统一 |
| 装饰高光 | `#D4A017` (琥珀) | 仅一个关键元素 —— 类比手绘琥珀环 |
| 实心填充(如 query token) | `backgroundColor: #B23A26` + `fillStyle: solid` | 示意图围绕的"hero"元素 |

其他锁定参数:

- `fontFamily: 5`(Excalifont —— excalidraw skill 强制要求所有文本使用)
- `roughness: 1`(默认手绘抖动;不要升到 2 —— 在缩略图尺度下会过于嘈杂)
- `strokeStyle: dashed` 表达"压缩 / 近似 / 有损"关系(如 CSA/HCA 窗口)
- `strokeStyle: solid` 表达"精确 / 完整"关系(如 local full-attention)
- `strokeWidth: 1` 形状,`2` 主连接箭头
- `endArrowhead: "arrow"`,`startArrowhead: null` —— 单向;绝不双向
- `roundness: null` 中性框用锐角(更学术);`roundness: {type: 3}` 仅给 hero 实心赭红块(锚点元素)

### 该问 diagram-generator 的内容

一个好的示意图 prompt 会指明:
1. **布局** —— 元素的中心 / 上 / 左 / 右位置(有像素坐标就给)
2. **元素类型** —— 矩形、椭圆(token 点)、小块化矩形
3. **关系** —— 哪些箭头从哪到哪,可选标签
4. **颜色角色** —— 哪些元素用赭红 vs 近黑,哪些用米色填充
5. **元素预算** —— 保持 ≤ 20 个元素;超出说明示意图对一张卡来说过密

### 输出处理

`excalidraw-diagram-generator` 写出 `.excalidraw` JSON 文件。把它存到 `<post-stem>-diagrams/card-NN-<short-name>.excalidraw`。`assets/render.py.tmpl` 中实现的构建管线自动:

1. 用 Playwright headless 加载 excalidraw 库(unpkg 的 UMD bundle)
2. 对每个 `.excalidraw` 文件调用 `ExcalidrawLib.exportToSvg({elements, appState, files})`
3. 把结果落到 `<post-stem>-diagrams/card-NN-<short-name>.svg` 便于检查
4. 在 HTML 对应标记块处 inline 替换(`<!-- excalidraw:card-NN begin --> ... <!-- excalidraw:card-NN end -->`)
5. 把合并结果写入 `<post-stem>-rendered.html`,从这个文件截图

标记键派生规则:`.excalidraw` 文件名 stem 的前两段(破折号分割)(`card-02-v32-bottleneck.excalidraw` → `card-02`)。HTML 必须有一对 `<!-- excalidraw:card-02 begin -->` ... `<!-- excalidraw:card-02 end -->` 把**内嵌 fallback SVG** 包起来,构建脚本才能精准替换。**保留 fallback** —— 当 CDN 不可达时,原始 inline SVG 原样出图。

**用户的一条命令工作流**:`py render.py xhs-post-<slug>.html` —— 一键完成转换 + inline + 截图。无需手动到 excalidraw.com 导出。

## 示意图 SVG 视觉语言(降级,不使用 excalidraw 时)

对于极简示意图(2-3 个框 + 1 条箭头)、或环境无法访问 `.excalidraw` 渲染器时,降级到手写 inline SVG。这是明确的**降级路径**,不是首选。

当卡片嵌入手写示意图:

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

v1 内容卡片的正文必须包含 **200–260 中文字符等价词**的实质内容,不计入引子、页码、标题、gist 和权衡行。低于 200 读起来像凑数。高于 260 在 3:4 比例下、11px 字号、约 316px 内容宽度下,bullet 一旦换行就开始拥挤;**硬上限 280**,超过就拆成两张卡。

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

## 水印层(防盗,烤进每张卡片)

每张卡片 —— 封面和内容卡 —— 都携带一层**对角平铺 SVG 水印**,作为卡片 div 的最后一个 DOM 子节点。水印是让二次上传到其他平台的截图在裁剪后仍能被识别为作者所有的关键。没有水印的卡片不通过 QA(`qa-checklist.md` 中的 `watermark_present` 指标)。

### 规格

| 属性 | 值 |
|---|---|
| 层样式 | `position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 50` —— 由卡片的 `overflow: hidden` 限定 |
| 平铺尺寸(pattern) | 200 × 100 px,`patternUnits="userSpaceOnUse"` |
| 旋转 | `patternTransform="rotate(-28)"` |
| 文本内容 | `@<author-handle>`(默认 `@谭磊 · TanLei`) |
| 字体 | `EB Garamond, Georgia, serif`,斜体,13px |
| 浅色表面(内容卡、V1/V3 封面) | `fill="#1F1B16"` `fill-opacity="0.05"` |
| 深色表面(V2 封面) | `fill="#F5EDDC"` `fill-opacity="0.06"` |
| Pattern `id` | 每张卡唯一:`wm-01`、`wm-02`...... 一个 HTML 里多个 `<defs>` 不能撞 |

### 模板(作为每张卡片最后一个子节点放进去)

```html
<svg xmlns="http://www.w3.org/2000/svg"
     style="position: absolute; inset: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 50;"
     aria-hidden="true" preserveAspectRatio="none">
  <defs>
    <pattern id="wm-{PAGE_NUM}" x="0" y="0" width="200" height="100"
             patternUnits="userSpaceOnUse" patternTransform="rotate(-28)">
      <text x="0" y="50" font-family="EB Garamond, Georgia, serif"
            font-style="italic" font-size="13"
            fill="{WM_COLOR}" fill-opacity="{WM_OPACITY}">{WM_TEXT}</text>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#wm-{PAGE_NUM})"/>
</svg>
```

### 设计理由

- **5–6% opacity** 让正文完全可读,但合成后的水印无法在不重新渲染卡片的前提下被去除(重新渲染会破坏其余细节)。盗图的人截图再上传,水印跟着走。
- **对角全卡平铺**意味着*裁剪也跑不掉水印* —— 任何可见像素块里都含作者 handle 的片段。
- **`pointer-events: none`** 让这层不可交互:文字选择、悬停、复制依然作用在底层真实内容上。
- **z-index: 50** 居于内容之上、页码 ghost 描边之下(后者本身用透明描边,装饰性)。在 5% opacity 下,水印不会与标题或 hero 在视觉上抢占。
- **作为最后一个 DOM 子节点**意味着水印不需要在其他元素上做 z-index 体操就能渲染在最上层。

### 禁用变体

- **不要只在角落放水印**。单角水印很容易被裁掉 —— 等于失去全部价值。
- **不要"© 版权所有"法律体**。读者是同行工程师;法律辞令读起来像偏执,反而降低可信度。
- **内容卡不要超过 8% opacity 的水印**。超过 8% 会干扰标题和 bullet 对比度,小字号尤其明显。
- **水印文本不要超过 16 个视觉字符**。更长的字符串在 -28° 旋转下平铺起来很差,会开始视觉冲突。
- **`assets/example-post.html` 参考输出不要带水印** —— 那个例子是模板,不是要发布的帖子,水印放进去会泄露到所有克隆这个例子的副本。
