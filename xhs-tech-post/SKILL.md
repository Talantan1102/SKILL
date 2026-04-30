---
name: xhs-tech-post
description: 当用户想要起草、设计或生成关于技术工程主题的小红书（小红书 / RedNote）帖子时使用此 skill —— 涵盖 LLM 训练、推理基础设施、agent 系统、模型架构、RAG、分布式系统，或任何面向同行的技术写作。触发短语包括"帮我写一篇小红书"、"做一张小红书技术贴"、"我想把 X 发到小红书"、"RedNote 技术贴"，或者用户提供代码仓库 / 论文 / 博客 URL 并希望转化为小红书内容。该 skill 输出一篇完整的帖子 —— 封面图（3:4 HTML）+ 7–9 张内容卡片 + 帖子正文 + 话题标签 —— 采用为工程师受众调校的克制的编辑风格设计（米色背景、赭红色强调色、lucide 图标、不使用标题党语言）。即使用户只是宽泛地提到小红书、RedNote 或"技术贴 / 知识卡片"格式，也应使用此 skill。
---

# 小红书技术帖

为同行工程师生成完整的小红书帖子 —— 封面、内容卡片、帖子正文和话题标签 —— 使用一致的编辑风格视觉语言。

## 受众与意图

读者是与作者大致同等资历的同行工程师（LLM 应用、推理基础设施、ML 系统、agent 方向）。他们会从以下维度评判帖子：
- 作者是否真的实操过所描述的内容
- 信息密度和具体程度（数字、具名工具、具体决策）
- 是否诚实披露了取舍

这意味着设计与写作风格不同于主流的小红书生活方式帖子。避免标题党词汇：绝绝子、YYDS、神器、封神、震惊、永远不要 X、99% 的人不知道、emoji 堆叠的开头。这些对目标受众而言是负面信号。

但设计也不是纯粹的编辑式克制 —— v1 故意使用手绘涂鸦（波浪线、星星、手绘环、× 项目符号、贴纸倾斜）和次级琥珀色强调色来保持视觉活力。目标是：同行工程师可信度（具体、诚实、不浮夸）+ 剪贴簿式视觉能量（这样卡片组不至于像一份枯燥的内部演示）。两者都不可缺。

## skill 接受的输入

用户可以提供以下之一：

1. **主题字符串**："我想写一篇关于 GRPO reward hacking 的复盘"
   → skill 应该在生成前快速问 2–3 个澄清问题，了解具体细节（一个具体的锚点、关键洞察、取舍）。

2. **代码仓库路径或 URL**："把 sgl-project/sglang 里的 PCP 实现做成一篇贴"
   → 阅读 README 和关键目录。识别架构 / 机制。提出卡片地图；让用户确认后再生成。

3. **论文（PDF 或 arXiv URL）**："把这篇论文做成笔记"
   → 使用 pdf-reading skill 提取摘要、核心论点、标志性数字，以及至少一张图/表。映射到卡片序列。

4. **博客文章或文章 URL**：web_fetch → 提取论点 → 重组为卡片序列。

如果输入有歧义，默认进入**交互模式**：在生成任何 HTML 之前，让用户确认范围、关键洞察以及一个具体的数字/示例。

## 输出格式

完整的帖子向工作目录交付三个产物：

1. **`xhs-post-<slug>.html`** —— 所有卡片并排渲染（`display: grid` 布局），便于浏览器预览。每张卡片 `aspect-ratio: 3/4`，水印层已经烤进卡片标记。
2. **`render.py`** —— 一个基于 Playwright 的端到端构建脚本：把每张 `.card-wrap > div` 截图导出为 PNG，输出尺寸 ≥ 1242×1656 px（模板：`assets/render.py.tmpl`）。
3. **帖子正文 + 话题标签** —— 在对话中以 markdown 块输出：
   - **帖子正文**（正文）：80–150 字，对话式但技术性强，不使用标题党词汇
   - **话题标签**（话题）：3–5 个标签，按具体 → 宽泛排序

一篇完成的帖子包含：
- 1 张封面（page 01）
- 7–9 张内容卡片（pages 02–N），每张都带水印
- 1 段帖子正文 + 话题标签
- 用户运行 `render.py` 之后得到 N 张 PNG，可直接上传到小红书

## 流程

按顺序执行以下步骤。不要跳过第 1 步 —— 帖子质量更多取决于选题简报，而不是模板。

### 第 1 步 —— 构建帖子选题简报（简报关卡）

参考 `references/brief-gate.md`。在生成任何 HTML 之前，先输出一个完整的选题简报 YAML 块。6 个必填字段：

| 字段 | 内容 |
|---|---|
| `topic` | 一句话："把 43 个 tool 重构成 7 个 Skill 渐进披露" |
| `key_insight` | 一句话：把整篇帖子串起来的非显然想法 |
| `evidence` | 硬数字 / 前后对比 / 具名机制或工具 / 具体场景。**必填。**没有至少一个具体锚点的帖子会被拒绝。四种锚点类型见 `brief-gate.md`。 |
| `trade_off` | 这件事的代价是什么？**必填**，即使是轻微的。对这个受众而言，诚实是可信度的乘数。 |
| `audience_anchor` | 读者已经熟悉、可以以此为基础理解的概念是什么？用于让抽象概念落地。 |
| `chosen_hook` | 从 4 个封面 hook（A/B/C/D）中选一个 —— 选择规则见 `references/hook-patterns.md`。 |

如果 `evidence` 或 `trade_off` 缺失，遵循 `brief-gate.md` 中的拒绝协议。不要捏造。只有在选题简报完整后（或用户明确调用了 evidence override）才进入第 2 步。

### 第 2 步 —— 规划卡片序列

将选题简报映射到 7–9 张卡片。卡片类型分类法和选择规则在 `references/card-templates.md` 中。一篇实战复盘帖子的默认序列：

1. **Cover** —— 选定的 hook
2. **Concept card** —— 这是什么东西（如果不直观就配迷你示意图）
3. **Setup card** —— 上下文：之前的情况是什么，为什么重要
4. **Architecture / flow card** —— 你做的结构性改动
5. **Pitfall card** —— 取舍或反直觉之处
6. **Result card** —— 数字（对比 / 数据布局）
7. **Summary card** —— 3–5 条要点

根据主题调整。一篇纯优化帖子可能跳过架构卡，改为 2 张结果卡。一篇纯踩坑故事可能跳过架构卡，改为 2 张 pitfall 卡。不要硬套。

### 第 3 步 —— 按顺序生成卡片

对每张卡片，遵循 `references/card-templates.md` 中的模板。所有卡片都继承 `references/visual-system.md` 中的视觉契约 —— 相同的 kicker、相同的颜色、相同的角落页码、相同的页脚模式。

所有卡片通用的硬性规则（一旦违反就会损害可信度）：
- 每张卡片都有一个**具体锚点** —— 数字、具名实体、代码引用，或前后对比。绝不纯抽象。
- 每张卡片最多有**一个主要论点**。两个论点 → 拆成两张卡片。
- 取舍说明（小三角 + 斜体行）出现在确实有值得披露的代价的卡片上 —— 不是每张卡片都需要。
- hero token（品牌红高亮的词）是标题中最技术性但仍可读的词 —— 通常是专有名词（RadixAttention、Zigzag）或一个变化量（43→7）。

### 第 4 步 —— 生成帖子正文与话题标签

帖子正文（小红书撰写框中的正文）位于图片下方。长度 80–150 字。结构：
- 第 1 句：用平实的语言重述核心洞察
- 第 2–3 句：卡片装不下的一个具体细节或上下文
- 第 4 句（可选）：诚恳邀请讨论 —— "卡 N 那块的实现我还在迭代，有同行做过类似的可以评论区交流"

禁用清单（不要生成）：绝绝子、YYDS、神器、封神、震惊、你不知道的 X、99% 的人、!!!、连续多个 emoji。

话题标签：3–5 个，按具体 → 宽泛排序。例：`#SGLang #ContextParallel #LLM推理 #大模型 #AI工程师`。不要用无关的热门标签凑数。

### 第 4.5 步 —— 发布前自检

参考 `references/qa-checklist.md`。所有卡片 + 帖子正文 + 话题标签草稿完成后，向用户输出 QA 表格。自动重新生成任何 FAIL 的卡片（仅那张卡片，最多 2 次尝试）；将 coherence ✗ 项呈现给用户。只有在所有卡片 PASS 且所有 coherence 检查为 ✓（或用户明确接受）时才进入第 5 步。

### 第 5 步 —— 输出、水印、示意图标记、一键 PNG 导出

将所有卡片渲染到单个 HTML 文件：`xhs-post-<short-topic-slug>.html`。该 HTML 用 `display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 360px));` 布局把卡片包裹起来，便于浏览器预览。

**每张卡片必须包含水印层。**详见 `references/visual-system.md` "水印层" 一节 —— 一层对角平铺的 SVG 覆盖，opacity 5–6%，烤进卡片标记。没有水印的卡片不通过 QA（`watermark_present` 指标）。水印是让二次上传的截图在裁剪之后仍能识别为作者所有的唯一手段；省略水印 = 失去防盗的全部价值。

**对每一张通过 `excalidraw-diagram-generator` 生成示意图的卡片**，把内嵌的 fallback SVG 用一对标记注释包起来，让构建脚本能精准替换：

```html
<div style="margin-top: 10px; padding: 8px 10px; background: #FFFFFF;
            border: 0.5px dashed #1F1B1625; border-radius: 4px;">
  <!-- excalidraw:card-NN begin -->
  <svg viewBox="..." width="100%" style="display: block;">
    ...内嵌 fallback SVG（手写版本）...
  </svg>
  <!-- excalidraw:card-NN end -->
</div>
```

标记键约定：`card-NN`（两位数补零的卡号）。构建脚本按 `<post>-diagrams/` 下的 `.excalidraw` 文件名前两段（破折号分割）匹配标记键（`card-02-v32-bottleneck.excalidraw` → `card-02`）。

每个 `.excalidraw` 源文件存到 `<post-slug>-diagrams/card-NN-<short-name>.excalidraw`。**保留 HTML 里的 fallback 内嵌 SVG** —— 万一构建时无法访问 excalidraw 渲染器（CDN 被墙），fallback 让卡片组仍能完整出图。

然后把 `render.py` 写到 HTML 同一目录 —— 这个 Playwright 脚本**一条命令端到端构建**:(a) 用 headless excalidraw 把每张 `.excalidraw` 渲染成 SVG;(b) 在 HTML 的标记块处 inline 替换,产出 `<stem>-rendered.html`;(c) 把每张 `.card-wrap > div` 截图为 PNG,尺寸 ≥ 1260×1680 px。脚本模板 `assets/render.py.tmpl` 原样拷贝到 HTML 同目录,无需按帖子定制。

告知用户：
- "我已经把 `xhs-post-<slug>.html`、`xhs-post-<slug>-diagrams/*.excalidraw`、`render.py` 写到了工作目录。"
- "首次安装：`py -m pip install playwright`，然后 `py -m playwright install chromium`（如果 pip / playwright 网络不通，用全局 CLAUDE.md 里配的代理）。"
- "然后运行 `py render.py xhs-post-<slug>.html` —— 它会渲染 .excalidraw 为 .svg、在标记块处 inline 进 HTML（输出 `<stem>-rendered.html`）、再把每张卡片截图到 `<stem>-cards/card-NN.png`。水印已经烤进每张 PNG。"
- "降级方案（excalidraw CDN 不通或没装 Playwright）：在浏览器里打开 HTML，DevTools → 'Capture node screenshot' 按张截 `.card-wrap > div`。标记块里的 fallback 内嵌 SVG 会原样显示。"

## 硬约束

这些在整个 skill 内全局适用。它们编码了我们已商定的设计；偏离它们会导致跨帖子不一致，破坏品牌系列效应。

### 视觉常量（已锁定）

这些来自 `references/visual-system.md`。它们**不是**参数：
- 内容卡片背景：`#FFFFFF`（白色）—— 锁定
- 封面背景：`#FFFFFF` 浅色、`#1F1B16` 深色，或拆分块 —— 见下方封面原型
- 卡片边框：浅色表面 `1px solid #E8E2D6`（暖灰）；深色封面 `none`
- 着色块背景：`#FAF5E8`（米色 —— 用于卡片内的强调表面）
- 主墨色：`#1F1B16`
- 次要文本：`#5A5246`
- 三级文本 / kicker：`#8C7E68`
- 品牌主色（赭红）：`#B23A26`
- 品牌次色（琥珀，仅用于装饰）：`#D4A017`
- 卡片纵横比：`3/4`
- 仅两个字体族：正文用 `var(--font-sans)`，kicker、章节标签、示意图说明、取舍行、数据流注释用 `var(--font-serif)` 斜体
- 圆角：卡片 `8px`，内框 `4px`，SVG 矩形 `2px`

### 封面锚点（1 个必备 + 2–3 个辅助）

**这是本 skill 中最重要的规则。**一张在小红书信息流缩略图（约 200px 宽）下无法落地的封面，会让整篇帖子白费。

每张封面**必须**精确包含一个来自此列表的视觉锚点：

| # | 锚点类型 | 最低规格 | 与哪个 hook 搭配 |
|---|---|---|---|
| (a) | **数字锚点** —— 大数字 / 箭头 / 前后对比 | 数字 ≥ 80px，占据卡片面积 ≥ 25% | Hook A（始终），Hook B（当比例是核心标题时） |
| (b) | **logo 块** —— 品牌或框架名作为视觉块 | 字标 ≥ 64px，置于色块中且 ≥ 30% 卡片高度，或在深色背景上形成对比 | Hook B、Hook C |
| (c) | **示意图预览** —— 极简架构图 | ≥ 100×80px，含 ≥ 3 个标注元素 | Hook C、Hook D（当机制本身就是 hook 时） |

锚点是**当卡片以 200px 宽度显示时唯一必须保持可读的元素**。如果不可读，重新生成。

辅助装饰（2–3 个）：
- 描边卷号（右上角，深色封面上可选）
- kicker 行 + 32×1.5px 品牌红规则线（必备 —— 确立品牌系列）
- 斜条纹 / 虚线角图案（可选 —— 替代 v0 的 3 条堆叠）
- 阅读时长标记（必备 —— 帖子中唯一出现这个的位置）

3 种封面原型在 `references/card-templates.md` 中详细描述（封面变体 V1 / V2 / V3），每种都附完整 HTML。原型由选定的 hook + 帖子拥有的证据类型共同决定 —— `references/hook-patterns.md` 有选择表。

### 内容卡片相对封面的变化

内容卡片继承封面的装饰 1–3，但是：
- 装饰 4（3 条堆叠）**取消** —— 内容卡片把这块版面让给信息密度
- 装饰 5（阅读时长标记）**取消** —— 阅读时长是帖子级元数据，归属封面
- 页脚行（作者署名 + 页码指示）**完全移除** —— 小红书的 app 会在帖子旁显示作者；每张卡片重复印一次是冗余且嘈杂的
- 角落数字是**页码**（02、03……），而不是帖子号
- 取舍行（小三角 + 斜体行）成为卡片上**最后可见的元素**，用 `margin-top: auto` 推到底部

此外，内容卡片叠加 v1 的手绘 / 玩味词汇（每张卡片从此列表选 3–5 个元素）：

- 标题中强调词下方的波浪下划线
- 章节标签或贴纸旁边的琥珀色星星图形
- 标题中关键词周围的手绘椭圆（琥珀色）
- 负面调性列表（隐藏成本、踩坑、不适用）使用手绘 × 项目符号
- 示意图中某元素周围的手绘环形高亮（琥珀色）
- 一个着色元素的贴纸倾斜（`rotate(-0.6deg)` 至 `rotate(-0.7deg)`）
- 模块框上的虚线品牌红边框（架构卡片）

每种卡片类型都有自己的标准 3–5 元素组合 —— 见 `references/card-templates.md`。

### Hook 模式（4 种，无其他）

封面 hook 是 A/B/C/D 中的一种 —— 见 `references/hook-patterns.md`。没有其他 hook 类型。如果一篇帖子无法用这 4 种之一表达，那么这个主题大概不适合这个格式。

### 禁用的设计动作

不要使用：
- **内容卡片**（02+ 卡片）使用除 `#FFFFFF` 之外的任何背景色。封面可以使用 `card-templates.md` 中的深色 / 着色变体。
- 纯黑文本（使用暖调近黑色 `#1F1B16`）
- 多色 hero（仅一个强调词，使用品牌红 `#B23A26`）
- 琥珀 `#D4A017` 用于正文或结构线（琥珀仅用于装饰 —— 星星、手绘环、"关键"贴纸）
- `font-weight: 600`（从 500 直接跳到 700；600 看起来像"设计上的优柔寡断"）
- 渐变填充、投影、发光效果、模糊
- 卡片内容中的 emoji（`✅⚠️🎉🔥` 等）—— 设计已经为这些角色配备了自定义几何图标 + lucide
- 全大写中文短语
- 单张卡片正文中超过 3 个话题标签（话题标签归属帖子正文块，不在卡片上）
- 内容卡片上的作者署名（平台会显示；在卡片上印一遍是噪声）
- 单张卡片上超过 2 个贴纸倾斜元素（令人眩晕）

#### 封面专属禁忌（来自先前运行的失败模式）

- **没有其他锚点时，hero 文本 < 60px** —— 在缩略图尺度下读起来像空白卡片
- **居中纯文本布局且无锚点** —— 全白"Notion 截图"失败模式
- **3 条堆叠作为唯一视觉元素** —— 这是 v0 的主要装饰；单独使用无法成为锚点
- **副标题揭晓了悬念** —— 封面应该激发滑动，而不是总结全文
- **卷号被当作锚点** —— 角落的描边数字是装饰，不是锚点
- **封面上的多色 hero** —— 严格只用一种强调色（品牌红 OR 深色上的米色），二者不能并存

### 密度下限（每张内容卡片必须满足）

任何一项检查不通过的卡片就还不能交付：

1. **卡片正文 ≥ 6 个具体数据点**。"具体"指以下**之一**：
   - 一个数字（计数、百分比、比例、尺寸、版本、时间、阈值）
   - 一个具名工具 / 库 / 函数 / 文件 / API / 配置项（`SQLite`、`FTS5`、`cosine sim`、`top-k`、`tokenizer.json` 等）
   - 括号中的具体场景（`"喜欢 Python" 埋在 100 条 "thanks" 里`）
   - 前后对比或 vs 比较（`25K → 10K`、`vanilla vs 三层`）
2. **正文内容 200–260 中文字符当量**（不计 kicker、页码、标题、gist、取舍行）。低于 200 = 注水。高于 260 = 在 3:4 下、11px 字号、约 316px 内容宽度下，bullet 一旦换行就开始拥挤。**硬上限 280** —— 超过就拆成两张卡，绝不让取舍行被挤出底部。
3. **没有不带具体内容的项目符号**。纯断言式的项目符号（"这很糟"、"性能提升"、"更快了"）不通过。每个项目符号必须至少包含上述列表中的一个具体内容。Concept 卡的项目符号必须有**两个**具体内容（标准模式见 `card-templates.md`）。
4. **架构模块详情使用结构化双字段模式**（见 `card-templates.md`）。单一密集行不够。
5. **Pitfall "实际" 面板 ≥ 3 个具体内容**。pitfall 卡的全部意义就在于这个意外揭晓 —— 它需要具体证据。
6. **bullet 换行预算 —— 每条 bullet ≤ 2 个视觉行**（360px 卡片 / 11px 字号下）。如果某条 bullet 会换行到 3+ 行，要么去掉第二个括号内的 specific，要么拆成两条。`card-templates.md` 说"concept bullet 携带 2 个 specifics" —— 那是目标，不是把内容塞爆的许可。心算法：11px 下中文每行约 33 字符，60 字纯中文 bullet 换行成 2 行，90+ 字会换行 3 行,必须裁剪。
7. **水印层存在**。每张卡片携带 `references/visual-system.md` "水印层" 一节定义的对角 SVG 平铺。没有水印的卡片不通过 QA `watermark_present` 指标，会被重新生成。

密度下限不可妥协。如果素材不能产出足够的具体内容，那卡片类型选错了（很可能应该用另一种卡片类型，或者内容应该合并到一张更密集的卡片里）。

## 参考文件

生成帖子时，按需查阅这些文件。在会话开始时读一次 —— 它们是稳定的，你会在不同帖子间复用相同的模式。

| 文件 | 何时读 |
|---|---|
| `references/visual-system.md` | 会话开始时。所有卡片继承的视觉契约。 |
| `references/hook-patterns.md` | 选择封面 hook 时（第 1 步，`chosen_hook` 字段）。 |
| `references/card-templates.md` | 生成每张卡片时（第 3 步）。包含 concept 和 architecture 卡的完整 HTML 模板；其余卡片有原则 + 骨架。 |
| `references/post-structure.md` | 规划卡片序列时（第 2 步）。不同帖子类型的经验法则。 |
| `assets/example-post.html` | 当你想看一份完整的参考输出。用于校准密度和节奏。 |
| `assets/render.py.tmpl` | 第 5 步。原样拷贝到 HTML 同一目录命名 `render.py`。一条命令完成 .excalidraw → SVG 渲染 + 标记块 inline + 截图导出 PNG。 |
| `references/qa-checklist.md` | 第 4.5 步。定义每张卡片的 metric（`char_count` 200–260、`bullet_wrap_visual`、`wordmark_fit`、`watermark_present` 等）—— 这些 metric 是进入第 5 步的关卡。 |

## skill 委托规则

本 skill 对要不要调用其它 skill 有明确立场。

### 不要委托给 `frontend-design`

`frontend-design` skill 调校的方向是产出*独特*、*有创造性*的界面 —— 它的强项是跳出通用 AI 美学。这个目标与本 skill **直接冲突**。

本 skill 的价值在**品牌系列一致性**：用 `xhs-tech-post` 写出来的每一篇帖子,看起来都应该像同一系列的兄弟篇,这样同行工程师只看一两张卡就能识别出来源。视觉系统(色板、字号阶梯、手绘词汇、卡片框架、kicker / 页码 / 页脚模式、水印)在 `references/visual-system.md` 里**已锁定**。生成过程中调用 `frontend-design` 会注入"创造性指令",覆盖这些锁定值,让每篇帖子风格各异 —— 这正是本 skill 存在要避免的失败模式。

**因此:不要从本 skill 内部调用 `frontend-design`,也不要通过 `frontend-design` 调本 skill。**卡片 HTML 直接从 `references/card-templates.md` 模板生成。如果视觉系统本身需要演化,直接编辑 `visual-system.md` 和模板 —— 那是单独的、深思熟虑的改动,不是按帖子做的创意 pass。

### 把示意图委托给 `excalidraw-diagram-generator`

对于 `concept` 和 `architecture` 卡片里的**迷你示意图** —— 那些展示某个机制如何拼装的图(例如 Hybrid Attention 的 CSA/HCA 切分、3 层记忆架构、请求流泳道) —— 正确的工具是官方 `excalidraw-diagram-generator` skill,**不是**手写 inline SVG primitive。

理由：
- excalidraw 的 hand-drawn `roughness` 渲染感与 v1 手绘词汇(波浪线、星星、手绘椭圆、× bullet)契合度远高于线条干净的 inline SVG。手写 SVG 看起来像蓝图;excalidraw 输出看起来像笔记本草图 —— 这正是卡片组想要的感觉。
- 用户能拿到一份可编辑的 `.excalidraw` JSON,后续不用碰 HTML 就能迭代图。
- 元素级的颜色 / 字体 / strokeStyle 可以干净映射到品牌色板 —— 详见 `references/visual-system.md` "示意图 — excalidraw conventions" 一节里锁定的映射表。

**工作流**(在生成示意图非平凡的卡片时执行)：

1. **生成** —— 调用 `excalidraw-diagram-generator`,在描述里要求它使用品牌色板(赭红 `#B23A26`、近黑 `#1F1B16`、米色 `#FAF5E8`、装饰琥珀 `#D4A017`)、`fontFamily: 5`、`roughness: 1`。输出到 `xhs-post-<slug>-diagrams/card-NN.excalidraw`。
2. **转换** —— 由 `assets/render.py.tmpl` 中实现的 Playwright 自动化负责:headless 加载 excalidraw 库,渲染每张 .excalidraw 为 SVG,inline 替换到 HTML 标记块,然后截图。**不需要用户手动走 excalidraw.com 导出**。
3. **降级** —— 对极简示意图(2-3 个框 + 1 条箭头)、或环境无法访问 excalidraw CDN 时,降级到 `visual-system.md` 中列出的 inline SVG primitive。降级是允许的,但要明确标注为降级路径,不要假装降级版本是首选输出。

**元素预算**:每张图按 `excalidraw-diagram-generator` 验证清单保持 ≤ 20 个元素。如果一张卡需要更多,说明卡片承载得太多 —— 拆成两张卡。

**值得用 excalidraw 的示意图**：
- 解释多组件机制的 concept 卡(≥ 3 个标注框 + 关系)
- 展示模块交互的 architecture 卡
- 任何示意图本身需要承载意义、超出仅作排版装饰的卡片

**不值得用 excalidraw 的**：
- 一个着色框带 2 个标签 —— inline SVG 或者直接一个 styled `<div>` 更快
- 标注矩形的 2 行网格 —— 同上
- 视觉系统本身的"手绘词汇"元素(波浪线 / 星星 / 椭圆 / × / 手绘环) —— 那些是卡片框架的一部分,不是示意图

## 关于迭代的说明

此 skill 是 **v1**。五种卡片类型已有完全锁定的 HTML 模板：`cover`、`concept`、`architecture`、`compare`、`pitfall`、`summary`。两种仍只有原则：`flow` 和 `code` —— 它们的视觉语言尚未通过真实演示运行验证。当生成的帖子需要尚未锁定的卡片类型时，遵循 `card-templates.md` 中的原则和视觉常量 —— 生成的卡片可能需要用户反馈才能为下一次迭代锁定模板。
