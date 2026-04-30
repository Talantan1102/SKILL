# 卡片模板 (v1)

七种卡片类型,全部锁定。模板基于 v1 视觉系统(白色背景、1px 边框、无页脚、手绘元素、琥珀色作次级强调色)。

## 卡片类型分类(taxonomy)

| 类型 | 用途 | 在一篇典型帖子中的出现频率 |
|---|---|---|
| **Cover (封面)** | 首卡,钩子 | 每帖 1 次(必有) |
| **Concept (概念)** | 定义一个非显然的想法,框定一个问题 | 0–2 次 |
| **Architecture (架构)** | 结构性总览(并列分面 / 模块) | 0–1 次 |
| **Flow (流程)** | 顺序流水线 | 0–1 次 |
| **Compare (对比)** | 并列或前后结构对比 | 0–2 次 |
| **Code (代码)** | 带注释的关键片段 | 0–2 次 |
| **Pitfall (陷阱)** | 反直觉的陷阱或"我以为 X"瞬间 | 1–3 次(战记类帖子) |
| **Summary (收束)** | 含要点 + 适用/不适用 的收束卡 | 每帖 1 次(必有) |

一篇典型的 7 卡帖子:封面 + 概念 + 对比 + 架构 + 概念-或-陷阱 + 陷阱 + 收束。

---

## 1. Cover(封面)

钩子——也是决定小红书 feed 中是否有人继续读下去的唯一一张卡。三种锁定的原型(V1 / V2 / V3);根据所选钩子 + brief 中证据的种类挑选其一。挑选表见 `references/hook-patterns.md` 的 "Anchor selection table"。

**强制规则:** 每张封面必须包含一个视觉锚点——一个大数字 (V1)、一个 logo 块 (V2),或一个迷你示意图 (V3)。白底 + 小字 + 角落装饰已不再是合法封面;那是 v0 的失败模式,在 200px 缩略图下会消失。

### V1 — Number Hero(数字英雄,浅底)

用于钩子 A(数字反差)和钩子 B(当结构变化带计数时,例如 `43 → 7`)。

**结构:**
```
┌─────────────────────────────────────┐
│ [kicker · italic serif]    [01 #]   │  ← outlined corner number (optional)
│ ───                                  │
│                                      │
│                                      │
│       88                             │  ← BIG number, 88-96px
│       →   27%                        │  ← arrow + after, brand red
│                                      │
│       sub-headline (structural)      │  ← 14px context, no spoiler
│                                      │
│ ◤                                    │  ← diagonal stripe corner (optional)
│ ●author                  约 N min   │
└─────────────────────────────────────┘
```

**模板:**

```html
<div style="position: relative; aspect-ratio: 3/4; background: #FFFFFF;
            padding: 24px 22px 18px 22px; display: flex; flex-direction: column;
            justify-content: space-between; border: 1px solid #E8E2D6;
            border-radius: 8px; color: #1F1B16; box-sizing: border-box;
            overflow: hidden;">
  <div style="position: absolute; top: 8px; right: 14px; font-size: 70px;
              font-weight: 700; color: transparent;
              -webkit-text-stroke: 1px #B23A26; line-height: 1;
              letter-spacing: -0.05em; opacity: 0.4;
              font-family: var(--font-serif);">{PAGE_NUM}</div>
  <div style="position: absolute; bottom: 0; left: 0; width: 0; height: 0;
              border-style: solid; border-width: 0 0 36px 36px;
              border-color: transparent transparent #B23A26 transparent;"></div>
  <div style="position: relative; z-index: 2;">
    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 11px; letter-spacing: 0.05em;
                color: #8C7E68;">{KICKER}</div>
    <div style="width: 32px; height: 1.5px; background: #B23A26;
                margin-top: 6px;"></div>
  </div>
  <div>
    <div style="font-size: 88px; font-weight: 700; line-height: 0.92;
                letter-spacing: -0.03em;">
      {BEFORE} <span style="color: #B23A26;">→</span> {AFTER}
    </div>
    <div style="font-size: 14px; color: #5A5246; margin-top: 18px;
                line-height: 1.55; max-width: 260px;">{SUBTITLE — structural context, no spoiler}</div>
  </div>
  <div style="display: flex; align-items: center; justify-content: space-between;
              gap: 8px; font-size: 11px; color: #8C7E68; padding-top: 10px;
              border-top: 0.5px solid #1F1B1622;">
    <div style="display: flex; align-items: center; gap: 8px;">
      <span style="width: 6px; height: 6px; background: #B23A26;
                   border-radius: 50%;"></span>
      <span>{AUTHOR} · {CATEGORY}</span>
    </div>
    <span>读完约 {N} 分钟</span>
  </div>
</div>
```

### V2 — Logo Block(Logo 块,深色海报)

用于无数字的钩子 B、钩子 C(技术名词)、钩子 D(我以为)。品牌 / 框架 / 模型名在深色海报背景上承担视觉重量。这是最强的"拇指停留"原型——在 feed 缩放下它看起来就像一张专辑封面。

**结构:**
```
┌─────────────────────────────────────┐  ← dark bg #1F1B16, no border
│ ▰                            VOL·01 │  ← stripe + small VOL marker
│                                      │
│ [kicker dim cream] ───              │
│                                      │
│       DeepSeek                       │  ← wordmark line 1, cream 84px
│       V4                             │  ← wordmark line 2, brand red 84px
│                                      │
│       subtitle line                  │  ← cream-dim, 14px
│       ● tag1  ● tag2  ● tag3         │  ← inline data tags, brand-red dots
│                                      │
│ ●author                  约 N min   │  ← cream-dim footer
└─────────────────────────────────────┘
```

**模板:**

```html
<div style="position: relative; aspect-ratio: 3/4; background: #1F1B16;
            padding: 24px 22px 18px 22px; display: flex; flex-direction: column;
            justify-content: space-between; border: none; border-radius: 8px;
            color: #F5EDDC; box-sizing: border-box; overflow: hidden;">
  <div style="position: absolute; top: 0; right: 0; width: 90px;
              height: 14px; background: #B23A26;
              transform: rotate(45deg) translate(20px, -32px);
              transform-origin: 100% 0%;"></div>
  <div style="position: absolute; top: 14px; right: 18px;
              font-family: var(--font-serif); font-style: italic;
              font-size: 11px; color: #8C7E68; letter-spacing: 0.12em;">VOL · {PAGE_NUM}</div>
  <div style="position: relative; z-index: 2;">
    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 11px; letter-spacing: 0.05em;
                color: #8C7E68;">{KICKER}</div>
    <div style="width: 32px; height: 1.5px; background: #B23A26;
                margin-top: 6px;"></div>
  </div>
  <div>
    <div style="font-size: 84px; font-weight: 700; line-height: 0.92;
                letter-spacing: -0.025em; color: #F5EDDC;">
      {WORDMARK_LINE_1}
    </div>
    <div style="font-size: 84px; font-weight: 700; line-height: 0.92;
                letter-spacing: -0.025em; color: #B23A26;
                margin-top: 4px;">
      {WORDMARK_LINE_2 — version / edition / suffix}
    </div>
    <div style="font-size: 14px; color: #B5A98E; margin-top: 16px;
                line-height: 1.55; max-width: 260px;">{SUBTITLE}</div>
    <div style="display: flex; gap: 14px; margin-top: 12px;
                font-family: var(--font-serif); font-style: italic;
                font-size: 11px; color: #B5A98E;">
      <span><span style="color: #B23A26;">●</span>&nbsp;{TAG_1}</span>
      <span><span style="color: #B23A26;">●</span>&nbsp;{TAG_2}</span>
      <span><span style="color: #B23A26;">●</span>&nbsp;{TAG_3}</span>
    </div>
  </div>
  <div style="display: flex; align-items: center; justify-content: space-between;
              gap: 8px; font-size: 11px; color: #8C7E68;
              padding-top: 12px; border-top: 0.5px solid #5A524633;">
    <div style="display: flex; align-items: center; gap: 8px;">
      <span style="width: 6px; height: 6px; background: #B23A26;
                   border-radius: 50%;"></span>
      <span>{AUTHOR} · {CATEGORY}</span>
    </div>
    <span>读完约 {N} 分钟</span>
  </div>
</div>
```

**V2 规则:**
- Wordmark 拆成 2 行:品牌/框架名(cream)在第 1 行,版本/edition(品牌红)在第 2 行。任意一行都可以是品牌红的那行——通常是更短、更有辨识度的那个 token。
- **Wordmark 长度上限:** 任意 wordmark 行在 84px 下若超过 **12 视觉字符**(中文计 1,ASCII 计 1)将会撑爆 360px 卡片。三个备选方案,按优先级排序:(1) 缩写(`RadixAttention` → `RadixAttn` 或 `RA`);(2) 降到 64px 保留全名;(3) 拆成更多行。不要降到 60px 以下——那会破坏锚点规则。
- 使用 0–3 个内联数据 tag。Tag 可以是 (a) **硬数字**——若帖子有这些数字且封面要做数字预告,(b) **结构事实**(具名组件、分层概念、框架家族),或 (c) **元数据**(版本、license、发布日期)。一致地选——不要在同一行混用元数据和数字。
- 对角条纹是可选的但建议保留——它把这张封面与一个普通的"暗色模式" Notion 页面区分开。
- 在深色背景上,页脚文本必须是 `#8C7E68`(三级灰),而不是 cream——保持 hero 作为主焦点的可读性。

### V3 — Schematic Peek(示意图窥视,浅底,以示意图为锚)

用于钩子 C / D 的场景:**没有广为人知的品牌或框架名**可以借势,**且**该机制的示意图比任何 wordmark 都更易被记住。例子:context-parallel 的 zigzag 切分模式、2D pipeline parallel 的网格、像 `Mamba` selective scan 这样的数据流形状。迷你示意图是锚点;hero 文字缩小给它让位。

**V3 是少见的兜底,而非钩子 C 的默认。** 如果帖子讲的是一个具名系统(RadixAttention、SGLang、vLLM、FlashAttention 等),V2 胜出,因为品牌 wordmark 在缩略图尺度下比示意图的图形匹配能给出更强的前注意识别。只在以下情况用 V3:(a) 没有可放在封面上的可识别品牌;或 (b) 示意图本身在工程师受众中具有标志性、可识别(很少见)。

**结构:**
```
┌─────────────────────────────────────┐
│ [kicker]              [01 #]        │
│ ───                                  │
│                                      │
│ 32px hero line 1                     │
│ 32px hero with [accent token]        │
│                                      │
│ ┌───────────────────────────────┐   │
│ │  [mini schematic ≥ 100×80]    │   │  ← cream-tinted backdrop
│ │  3+ labeled elements          │   │
│ │  arrows + amber loop          │   │
│ └───────────────────────────────┘   │
│                                      │
│ ●author                  约 N min   │
└─────────────────────────────────────┘
```

使用 `visual-system.md` 中"Schematic SVG visual language"的示意图原语。Hero 文字最大 30-36px——视觉重量由示意图承担,而非文字。V3 的副标题是可选的(示意图本身就是它的副标题)。

**模板骨架**(完整 SVG 内容因帖而异,见 hooks-patterns + 示意图原语):

```html
<div style="position: relative; aspect-ratio: 3/4; background: #FFFFFF;
            padding: 22px 22px 18px 22px; display: flex; flex-direction: column;
            justify-content: space-between; border: 1px solid #E8E2D6;
            border-radius: 8px; color: #1F1B16; box-sizing: border-box;
            overflow: hidden;">
  <div style="position: absolute; top: 8px; right: 14px; font-size: 70px;
              font-weight: 700; color: transparent;
              -webkit-text-stroke: 1px #B23A26; line-height: 1;
              letter-spacing: -0.05em; opacity: 0.4;
              font-family: var(--font-serif);">{PAGE_NUM}</div>
  <div style="position: relative; z-index: 2;">
    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 11px; letter-spacing: 0.05em;
                color: #8C7E68;">{KICKER}</div>
    <div style="width: 32px; height: 1.5px; background: #B23A26;
                margin-top: 6px;"></div>
  </div>
  <div>
    <div style="font-size: 32px; font-weight: 700; line-height: 1.15;
                letter-spacing: -0.01em;">
      {HERO_LINE_1}<br/>
      <span style="color: #B23A26;">{ACCENT_TOKEN}</span> {HERO_LINE_2}
    </div>
    <div style="margin-top: 16px; padding: 12px 14px; background: #FAF5E8;
                border-radius: 4px; border: 0.5px solid #1F1B1622;">
      <svg viewBox="0 0 280 130" width="100%" style="display: block;">
        <!-- 示意图内容:3-5 个带标签的方框、箭头、琥珀色环 -->
        <!-- 见 visual-system.md 中的 schematic SVG visual language -->
      </svg>
    </div>
  </div>
  <div style="display: flex; align-items: center; justify-content: space-between;
              gap: 8px; font-size: 11px; color: #8C7E68; padding-top: 10px;
              border-top: 0.5px solid #1F1B1622;">
    <div style="display: flex; align-items: center; gap: 8px;">
      <span style="width: 6px; height: 6px; background: #B23A26;
                   border-radius: 50%;"></span>
      <span>{AUTHOR} · {CATEGORY}</span>
    </div>
    <span>读完约 {N} 分钟</span>
  </div>
</div>
```

### V1 vs V2 vs V3 的选择

```
有硬 before-after 数字 / 可做大字 hero?  ──→ V1 Number Hero
        │ no
        ↓
有具名 brand / 框架 / 模型 / 版本?         ──→ V2 Logo Block
        │ no — 是一个抽象机制 (无品牌)
        ↓
                                        ──→ V3 Schematic Peek
```

**默认走 V2。** 带品牌的题材永远走 V2,即便示意图很有意思——在 200px 缩略图尺度下,wordmark 识别压过示意图的图形匹配。V3 只用于无品牌的概念(例如 "zigzag split"、"selective scan dataflow"),这些场景没有可识别的名字可以放上封面。

V1 与 V2 之间犹豫时:如果标题数字是**单一数字对**(比如 `43 → 7`、`27% / 10%`),走 V1。如果标题是**系统/版本**(比如 `DeepSeek V4`、`SGLang 0.5`),走 V2——即便帖子里也有数字(那些数字应该出现在 tag 或内容卡里,而不是封面 hero)。

---

## 2. Concept card(概念卡)

定义一个概念。包含一个着色的"现状"便签 + 迷你示意图 + 一段"N 个 X"的项目列表。

### 结构

```
[kicker + rule]                  [page #]
[Title with squiggle + amber star]
[Gist line in red]
─────────────────────
~ 现状 (tilted -0.7deg, cream bg)
  body explaining the situation
─────────────────────
[Mini-schematic with amber loop highlight]
─────────────────────
→ N 个 X (red label + amber star)
  × hand-drawn × bullet 1 (with parenthetical specifics)
  × bullet 2
  × ...
─────────────────────
△ 代价 · text
```

### 使用的手绘元素 (4 种)

1. 标题中强调 token 下方的波浪线
2. 强调 token 旁边的琥珀色星星
3. 示意图中关键元素周围的琥珀色手绘环
4. "N 个 X" 列表中作为项目符号的手绘 × 标记
5. "现状" 着色框上的便签倾斜(若想拉满密度,这算第 5 种)

### 模板

```html
<div style="position: relative; aspect-ratio: 3/4; background: #FFFFFF;
            padding: 22px 22px 18px 22px; display: flex; flex-direction: column;
            border: 1px solid #E8E2D6; border-radius: 8px; color: #1F1B16;
            box-sizing: border-box; overflow: hidden;">

  <div style="position: absolute; top: 8px; right: 14px; font-size: 70px;
              font-weight: 700; color: transparent;
              -webkit-text-stroke: 1px #B23A26; line-height: 1;
              letter-spacing: -0.05em; opacity: 0.4;
              font-family: var(--font-serif);">{PAGE_NUM}</div>

  <div style="position: relative; z-index: 2;">
    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 11px; letter-spacing: 0.05em;
                color: #8C7E68;">{KICKER}</div>
    <div style="width: 32px; height: 1.5px; background: #B23A26;
                margin-top: 6px;"></div>
  </div>

  <div style="margin-top: 12px;">
    <div style="font-size: 21px; font-weight: 700; line-height: 1.2;
                letter-spacing: -0.01em;">{TITLE_LINE_1}</div>
    <div style="font-size: 21px; font-weight: 700; line-height: 1.2;
                position: relative; display: inline-block; margin-top: 2px;">
      <span style="color: #B23A26;">{ACCENT_TOKEN}</span>
      <svg width="65" height="8" viewBox="0 0 65 8"
           style="position: absolute; bottom: -4px; left: -2px;">
        <path d="M 1 5 Q 10 1 20 5 T 40 5 T 64 5"
              fill="none" stroke="#B23A26" stroke-width="1.6"
              stroke-linecap="round"/>
      </svg>
      <svg width="14" height="14" viewBox="0 0 14 14"
           style="position: absolute; top: -8px; right: -16px;">
        <path d="M 7 1 L 8 6 L 13 6 L 9 9 L 11 13 L 7 10 L 3 13 L 5 9 L 1 6 L 6 6 Z"
              fill="#D4A017" stroke="#D4A017" stroke-width="0.5"/>
      </svg>
    </div>
    <div style="font-size: 12px; color: #B23A26; font-weight: 500;
                margin-top: 6px; line-height: 1.5;">{GIST}</div>
  </div>

  <div style="margin-top: 10px; background: #FAF5E8; padding: 8px 11px;
              transform: rotate(-0.7deg); border-radius: 4px;">
    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 10px; color: #8C7E68; letter-spacing: 0.05em;
                margin-bottom: 3px;">~ {INTRO_LABEL}</div>
    <div style="font-size: 11px; line-height: 1.55; color: #1F1B16;">
      {INTRO_BODY — 描述现状的 2-3 行}
    </div>
  </div>

  <div style="margin-top: 8px;">
    {SCHEMATIC_SVG — 见 visual-system.md 中的示意图模式}
  </div>

  <div style="margin-top: 6px;">
    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 10px; color: #B23A26; letter-spacing: 0.05em;
                margin-bottom: 5px; display: flex; align-items: center; gap: 4px;">
      <svg width="9" height="9" viewBox="0 0 9 9">
        <path d="M 4.5 0.5 L 5.4 3.6 L 8.5 3.6 L 6 5.5 L 7 8.5 L 4.5 6.6 L 2 8.5 L 3 5.5 L 0.5 3.6 L 3.6 3.6 Z"
              fill="#D4A017"/>
      </svg>
      <span>{N} 个 {LIST_LABEL}</span>
    </div>
    <ul style="list-style: none; padding: 0; margin: 0; font-size: 10.5px;
               line-height: 1.55; color: #1F1B16;">
      <li style="padding-left: 14px; position: relative; margin-bottom: 2px;">
        <svg width="9" height="9" viewBox="0 0 9 9"
             style="position: absolute; left: 0; top: 4px;">
          <path d="M 1 1 L 8 8 M 8 1 L 1 8"
                stroke="#B23A26" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
        {BULLET_1 含可选 <b>强调</b> + 括号内具体细节}
      </li>
      <!-- 重复用于第 2..N 项(最多 3 到 5 项) -->
    </ul>
  </div>

  <div style="margin-top: auto; display: flex; align-items: center;
              gap: 6px; padding-top: 8px;">
    {TRADE_OFF_SVG_AND_LINE — 见 visual-system.md}
  </div>
</div>
```

### 带括号具体细节的 bullet(必需)

概念卡的 bullet 必须遵循这个模式:
```
{症状或论断} · <b>{关键术语}</b>({具体 1},{具体 2 或澄清})
```

**括号里写两个具体细节,而不是一个。** 一个具体可以是数字、具名工具、具体场景或前后对比。两个具体应该是不同*类别*——例如(具体场景,数值后果)——以叠加可信度。

例子:
- `cosine sim 一刀切 · 时序丢光(早晨 vs 上周一视同仁,召回 ranking 完全失效)`
- `top-k 易塞满 16K context(k=20×800tok 就吃光,剩余 system+task 不够装)`
- `偏好被闲聊淹没("喜欢 Python" 埋在 100 条 "thanks" 里,召回率 < 5%)`
- `长尾任务从未召回(embedding sim 偏向高频 query,新意图首次失败概率 ~ 70%)`
- `偏好 update 越积越多(旧条目不删,3 个月后 query 召回 5+ 条互相矛盾)`

括号是让 bullet 对同行读者*可信*的关键——它传递的是亲历经验。**单一 specific 的 bullet 能过 v0,但过不了 v1。** 每条 bullet 都该给读者两个相信作者的理由。

一张概念卡有 4–6 条这样的 bullet。少于 4 条 = 卡看起来很单薄。多于 6 条 = 视觉拥挤。

---

## 3. Architecture card(架构卡)

展示 N(3–6)个并列模块 + 它们之间的协作。模块方框带虚线品牌红边框、cream 背景、lucide 图标。

### 结构

```
[kicker + rule]                  [page #]
[Title — with hand-drawn ellipse around key word]
[Gist line in red]
[Intro line — 1 sentence framing]
─────────────────────
[Module box 1: icon + name + dense 2-line desc]
[Module box 2]
[Module box 3]
...
─────────────────────
~ 数据流  {how modules cooperate at runtime}
─────────────────────
[★ 关键 — tilted amber sticker callout]
─────────────────────
△ 代价 · text
```

### 布局密度规则

- **3 个模块** → 1 列(垂直堆叠),每个模块约 70–78px 高(带 2 字段细节)
- **4–6 个模块** → 2×2 或 2×3 网格;在网格模式下,如果 2 字段会溢出,可降级为 1 字段细节(每个模块单行密集描述)
- **7 个及以上** → 拆成两张卡或简化;不要硬塞

### 模块细节:结构化 2 字段模式(垂直堆叠架构卡必需)

每个模块的次级块是**两行短的带标签内容**,而不是一行密集描述。两个字段抓住*模块是什么*与*它实际怎么工作*。标签是 italic-serif 红色,细节是普通灰色。

按模块类型挑选标签对:

| 模块类型 | 字段 1 | 字段 2 | 例子 |
|---|---|---|---|
| 存储层 | `存储` | `召回` | `存储 SQLite KV,每条 50–200 字` / `召回 FTS5 全文 + LLM top-5 二次过滤` |
| 进程 / 运行时层 | `触发` | `行为` | `触发 任务结束自动 nudge` / `行为 LLM 蒸馏 facts → 写 KV` |
| 数据层 | `范围` | `持久化` | `范围 当前 step plan + tool 输出` / `持久化 完成 step 即清空,无独立 DB` |
| 集成 | `输入` | `输出` | `输入 5KB 多轮原文` / `输出 200B 结构化 facts (~25:1 压缩)` |
| 通用兜底 | `怎么用` | `不怎么用` | `怎么用 long-context 推理` / `不怎么用 检索式 query` |

每个字段细节必须包含**至少 1 个具体**(数字 / 具名工具 / 文件 / 场景)。一个不带任何 specific 的 2 字段块过不了密度下限。

### 使用的手绘元素 (4 种)

1. 标题中关键词周围的手绘椭圆(琥珀色)
2. 模块方框上的虚线红边
3. 卡片底部的倾斜"关键"贴纸(琥珀色)
4. 从"关键"贴纸角落探出的星星贴纸

### 模板(3 模块垂直变体)

```html
<div style="position: relative; aspect-ratio: 3/4; background: #FFFFFF;
            padding: 22px 22px 18px 22px; display: flex; flex-direction: column;
            border: 1px solid #E8E2D6; border-radius: 8px; color: #1F1B16;
            box-sizing: border-box; overflow: hidden;">

  <div style="position: absolute; top: 8px; right: 14px; font-size: 70px;
              font-weight: 700; color: transparent;
              -webkit-text-stroke: 1px #B23A26; line-height: 1;
              letter-spacing: -0.05em; opacity: 0.4;
              font-family: var(--font-serif);">{PAGE_NUM}</div>

  <div style="position: relative; z-index: 2;">
    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 11px; letter-spacing: 0.05em;
                color: #8C7E68;">{KICKER}</div>
    <div style="width: 32px; height: 1.5px; background: #B23A26;
                margin-top: 6px;"></div>
  </div>

  <div style="margin-top: 12px; position: relative;">
    <div style="font-size: 22px; font-weight: 700; line-height: 1.2;
                letter-spacing: -0.01em;">
      {TITLE_PREFIX}
      <span style="color: #B23A26; position: relative;">
        {ACCENT_TOKEN}
        <svg width="42" height="22" viewBox="0 0 42 22"
             style="position: absolute; top: -3px; left: -4px; z-index: -1;">
          <path d="M 5 11 Q 2 4 21 3 Q 39 4 38 11 Q 37 19 21 19 Q 4 19 5 11 Z"
                fill="none" stroke="#D4A017" stroke-width="1.4"
                stroke-linecap="round"/>
        </svg>
      </span>
      {TITLE_SUFFIX}
    </div>
    <div style="font-size: 12px; color: #B23A26; font-weight: 500;
                margin-top: 5px; line-height: 1.5;">{GIST}</div>
  </div>

  <div style="margin-top: 8px; font-size: 11px; line-height: 1.5;
              color: #1F1B16;">{INTRO_LINE}</div>

  <div style="display: flex; flex-direction: column; gap: 6px; margin-top: 9px;">
    <!-- 为每个模块重复此 module-box 块 -->
    <div style="display: flex; gap: 9px; padding: 8px 10px;
                border: 0.8px dashed #B23A26; border-radius: 4px;
                background: #FAF5E8; align-items: flex-start;">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
           stroke="#B23A26" stroke-width="1.6"
           stroke-linecap="round" stroke-linejoin="round"
           style="flex-shrink: 0; margin-top: 1px;">
        {LUCIDE_ICON_PATHS}
      </svg>
      <div style="flex: 1; min-width: 0;">
        <div style="font-size: 11px; font-weight: 700;
                    line-height: 1.2;">
          {MODULE_NAME} · <span style="color: #B23A26;">{MODULE_ROLE}</span>
        </div>
        <div style="font-size: 10px; color: #5A5246; margin-top: 2px;
                    line-height: 1.4;">
          <span style="font-family: var(--font-serif); font-style: italic;
                       color: #B23A26;">{FIELD_1_LABEL}</span>
          {FIELD_1_DETAIL — 含具体细节}<br/>
          <span style="font-family: var(--font-serif); font-style: italic;
                       color: #B23A26;">{FIELD_2_LABEL}</span>
          {FIELD_2_DETAIL — 含具体细节}
        </div>
      </div>
    </div>
  </div>

  <div style="margin-top: 8px; font-family: var(--font-serif); font-style: italic;
              font-size: 10px; color: #8C7E68; line-height: 1.5;">
    <span style="color: #B23A26; letter-spacing: 0.05em;">~ 数据流</span>
    &nbsp; {模块在运行时如何协作}
  </div>

  <div style="margin-top: 8px; padding: 7px 11px 7px 12px;
              background: rgba(212,160,23,0.13);
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
                 margin-left: 6px;">{TAKEAWAY — 8-16 字}</span>
  </div>

  <div style="margin-top: auto; display: flex; align-items: center;
              gap: 6px; padding-top: 8px;">
    {TRADE_OFF_LINE}
  </div>
</div>
```

### Lucide 图标路径参考

(与 v0 相同未变)

| 概念 | Lucide 名 | Path |
|---|---|---|
| 分层 / 上下文 | `layers` | `<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>` |
| 工作流 / 路由 | `workflow` | `<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>` |
| 盾牌 / 守卫 | `shield` | `<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>` |
| 数据库 / 状态 | `database` | `<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>` |
| 恢复 / 循环 | `rotate-ccw` | `<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>` |
| 可观测 / 眼睛 | `eye` | `<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>` |
| 时钟 / 时序 | `clock` | `<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>` |
| 历史 / 时间线 | `history` | `<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>` |
| GPU / 硬件 | `cpu` | `<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>` |

其他图标搜索 lucide.dev。保持 `stroke-width="1.6"`。

---

## 4. Compare card(对比卡)

并列对比或"朴素 vs 我们"的对比。视觉上的反差**就是**这种设计——左侧中性/灰,右侧品牌红强调。

### 结构

```
[kicker + rule]                       [page #]
[Title with vs in red]
[Gist line]
─────────────────────
┌──────────────┬──────────────┐
│ × naïve      │ ★ ours       │
│ (italic gray)│ (italic red) │
│              │              │
│ - bullet 1   │ - bullet 1   │
│ - bullet 2   │ - bullet 2   │
│ - bullet 3   │ - bullet 3   │
│ - bullet 4   │ - bullet 4   │
└──────────────┴──────────────┘
△ 代价 · text
```

左列:灰色 bullet(`#8C7E68`),用中性措辞描述痛点。
右列:红色 bullet(`#B23A26`),关键术语加粗加红。

### 这种卡的密度下限

每条 bullet——两列都一样——必须包含**≥ 1 个具体**(数字、具名工具、具体机制)。两列都要遵守这条规则,因为只有当两边都具体时,对比才能成立。一张模糊对模糊的对比卡什么也教不了。

- ✗ `全部混在一起检索` / `三层独立检索`(都很模糊)
- ✓ `cosine sim 全部混着检(不带时间衰减)` / `三层各自检索(FTS5 + cosine + KV 三种召回)`

右列 bullet 应将**关键术语**(技法引入的实质名词)加粗 + 染红,bullet 其余部分描述它。视觉上这让略读者只吸收加粗的红字也能理解整篇。

bullet 数量:**每列 4-5 条**。3 条看起来单薄,6+ 视觉拥挤。

### 手绘元素 (3 种)

1. 标题中的 `vs` 用品牌红呈现
2. "naïve" 标头旁的手绘 × 标记
3. "ours" 标头旁的琥珀色星星

### 模板

```html
<div style="position: relative; aspect-ratio: 3/4; background: #FFFFFF;
            padding: 22px 22px 18px 22px; display: flex; flex-direction: column;
            border: 1px solid #E8E2D6; border-radius: 8px; color: #1F1B16;
            box-sizing: border-box; overflow: hidden;">

  <div style="position: absolute; top: 8px; right: 14px; font-size: 70px;
              font-weight: 700; color: transparent;
              -webkit-text-stroke: 1px #B23A26; line-height: 1;
              letter-spacing: -0.05em; opacity: 0.4;
              font-family: var(--font-serif);">{PAGE_NUM}</div>

  <div style="position: relative; z-index: 2;">
    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 11px; letter-spacing: 0.05em;
                color: #8C7E68;">{KICKER}</div>
    <div style="width: 32px; height: 1.5px; background: #B23A26;
                margin-top: 6px;"></div>
  </div>

  <div style="margin-top: 14px;">
    <div style="font-size: 21px; font-weight: 700; line-height: 1.2;
                letter-spacing: -0.01em;">
      {LEFT_LABEL} <span style="color: #B23A26;">vs</span> {RIGHT_LABEL}
    </div>
    <div style="font-size: 12px; color: #B23A26; font-weight: 500;
                margin-top: 6px; line-height: 1.5;">{GIST}</div>
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
              margin-top: 14px;">
    <div>
      <div style="display: flex; align-items: center; gap: 4px;
                  margin-bottom: 8px;">
        <svg width="9" height="9" viewBox="0 0 9 9">
          <path d="M 1 1 L 8 8 M 8 1 L 1 8"
                stroke="#8C7E68" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
        <span style="font-family: var(--font-serif); font-style: italic;
                     font-size: 11px; color: #8C7E68; letter-spacing: 0.05em;">
          {LEFT_HEADER}
        </span>
      </div>
      <ul style="list-style: none; padding: 0; margin: 0;
                 font-size: 11px; line-height: 1.6; color: #1F1B16;">
        <li style="padding-left: 10px; position: relative; margin-bottom: 6px;">
          <span style="position: absolute; left: 0; top: 7px;
                       width: 4px; height: 4px; background: #8C7E68;"></span>
          {LEFT_BULLET_1}
        </li>
        <!-- 重复用于左列其余 bullet -->
      </ul>
    </div>
    <div style="border-left: 0.5px solid #1F1B1625; padding-left: 12px;">
      <div style="display: flex; align-items: center; gap: 4px;
                  margin-bottom: 8px;">
        <svg width="9" height="9" viewBox="0 0 9 9">
          <path d="M 4.5 0.5 L 5.4 3.6 L 8.5 3.6 L 6 5.5 L 7 8.5 L 4.5 6.6 L 2 8.5 L 3 5.5 L 0.5 3.6 L 3.6 3.6 Z"
                fill="#D4A017"/>
        </svg>
        <span style="font-family: var(--font-serif); font-style: italic;
                     font-size: 11px; color: #B23A26; letter-spacing: 0.05em;">
          {RIGHT_HEADER}
        </span>
      </div>
      <ul style="list-style: none; padding: 0; margin: 0;
                 font-size: 11px; line-height: 1.6; color: #1F1B16;">
        <li style="padding-left: 10px; position: relative; margin-bottom: 6px;">
          <span style="position: absolute; left: 0; top: 7px;
                       width: 4px; height: 4px; background: #B23A26;"></span>
          {RIGHT_BULLET_1 含 <b style="color:#B23A26;">关键术语</b>}
        </li>
        <!-- 重复用于右列其余 bullet -->
      </ul>
    </div>
  </div>

  <div style="margin-top: auto; display: flex; align-items: center;
              gap: 6px; padding-top: 8px;">
    {TRADE_OFF_LINE}
  </div>
</div>
```

---

## 5. Pitfall card(陷阱卡)

"我以为 X,实际上 Y"的卡。两个堆叠面板,第二个用琥珀色高亮(并做贴纸式倾斜)。

### 结构

```
[kicker + rule]                       [page #]
[Title — accent token in red]
[Gist line]
─────────────────────
┌─────────────────────────┐
│ ~ 看起来 (or 以为)       │
│ what you'd expect       │  ← 1-2 lines, the naïve mental model
└─────────────────────────┘
            ↓ (red arrow)
┌─────────────────────────┐
│ ★ 实际 (or 结果)         │  ← amber-tinted, possibly tilted -0.6deg
│ what really happens —   │  ← 3-5 lines packed with specifics
│ MUST contain ≥ 3        │
│ specifics (numbers,     │
│ named tools, scenarios) │
└─────────────────────────┘
△ 代价 · text
```

### 这种卡的密度下限

"实际"面板就是陷阱卡的全部 payoff。它必须包含**≥ 3 个具体**——没有的话这张卡就只是一个观点。使用具体的形式:
- 数值阈值:`< 30 条样本里几乎随机` / `top-3 召回有 1-2 个噪声` / `约 50-100 个任务才进入可用区`
- 具名机制:`embedding ann 索引才有 cluster 结构` / `cosine sim 在小样本里坍缩`
- 时间/规模:`前 1-2 周` / `accumulate 50+`
- 失败模式:`召回率 ~ 5%` / `延迟 +200ms`

"看起来"面板可以保持简短(1-2 行,只写假设)。两个面板之间的不对称是有意为之——陷阱卡卖的就是*那个落差*。

### 标签约定

- 解析/解读类帖子(你在解读别人的项目):用 `~ 看起来 / ★ 实际`
- 战记/复盘类帖子(你在写自己的工作):用 `~ 以为 / ★ 结果`

### 手绘元素 (3 种)

1. 两面板之间的向下箭头(自定义 SVG)——品牌红
2. "实际"/"结果"面板标头上的星星贴纸
3. "实际"/"结果"面板的贴纸倾斜(-0.6deg)

### 模板

```html
<div style="position: relative; aspect-ratio: 3/4; background: #FFFFFF;
            padding: 22px 22px 18px 22px; display: flex; flex-direction: column;
            border: 1px solid #E8E2D6; border-radius: 8px; color: #1F1B16;
            box-sizing: border-box; overflow: hidden;">

  <!-- 角落数字、kicker、分割线(同 concept 模板) -->

  <div style="margin-top: 14px;">
    <div style="font-size: 21px; font-weight: 700; line-height: 1.2;
                letter-spacing: -0.01em;">
      {TITLE_PREFIX}<span style="color: #B23A26;">{ACCENT_TOKEN}</span>{TITLE_SUFFIX}
    </div>
    <div style="font-size: 12px; color: #B23A26; font-weight: 500;
                margin-top: 6px; line-height: 1.5;">{GIST}</div>
  </div>

  <div style="margin-top: 14px;">
    <div style="padding: 11px 13px; border: 0.5px solid #1F1B1625;
                border-radius: 4px; background: #FAF5E8;">
      <div style="font-family: var(--font-serif); font-style: italic;
                  font-size: 10px; letter-spacing: 0.05em; color: #8C7E68;
                  margin-bottom: 5px;">~ {EXPECTED_LABEL}</div>
      <div style="font-size: 12px; line-height: 1.55; color: #1F1B16;">
        {EXPECTED_BODY — 你会以为的样子}
      </div>
    </div>

    <div style="display: flex; justify-content: center; padding: 4px 0;">
      <svg width="16" height="16" viewBox="0 0 16 16">
        <line x1="8" y1="2" x2="8" y2="11"
              stroke="#B23A26" stroke-width="0.9"/>
        <polygon points="8,14 5,9 11,9" fill="#B23A26"/>
      </svg>
    </div>

    <div style="padding: 11px 13px; border: 1px solid #D4A017;
                border-radius: 4px; background: rgba(212,160,23,0.13);
                transform: rotate(-0.6deg); position: relative;">
      <svg width="13" height="13" viewBox="0 0 14 14"
           style="position: absolute; top: -6px; left: -5px;">
        <path d="M 7 1 L 8 5.5 L 12.5 5.5 L 9 8 L 10 12.5 L 7 10 L 4 12.5 L 5 8 L 1.5 5.5 L 6 5.5 Z"
              fill="#D4A017" stroke="#D4A017" stroke-width="0.5"/>
      </svg>
      <div style="font-family: var(--font-serif); font-style: italic;
                  font-size: 10px; letter-spacing: 0.05em; color: #8B6809;
                  font-weight: 700; margin-bottom: 5px;">{ACTUAL_LABEL}</div>
      <div style="font-size: 12px; line-height: 1.55; color: #1F1B16;">
        {ACTUAL_BODY — 实际发生的样子,带具体细节}
      </div>
    </div>
  </div>

  <div style="margin-top: auto; display: flex; align-items: center;
              gap: 6px; padding-top: 10px;">
    {TRADE_OFF_LINE}
  </div>
</div>
```

---

## 6. Summary card(收束卡)

收束卡。适用 / 不适用 列表配带要点的项目。

### 结构

```
[kicker + rule]                       [page #]
[Title — "什么时候该抄" or similar]
[Gist line]
─────────────────────
★ 适用 (red label + amber star)
  ▪ takeaway 1 (with reason in parens)
  ▪ takeaway 2 (with reason in parens)
  ▪ takeaway 3 (with reason in parens)
─────────────────────
× 不适用 (gray label + gray ×)
  ▪ takeaway 1 (with reason in parens)
  ▪ takeaway 2 (with reason in parens)
─────────────────────
△ 代价 · text (optional, often omitted on summary)
```

### 这种卡的密度下限

每条 bullet 必须在括号中带**一个理由或具体细节**,而不是只写一个分类。读者正在决定要不要采纳这种做法——他们需要看到每条"适用"或"不适用"*为什么*适用于自己。

- ✗ `长期对话连续性是核心需求`(过于泛)
- ✓ `长期对话连续性是核心需求(个人助手、24h+ 长任务 agent,需要 50+ 轮记忆)`
- ✗ `单次完成型任务`(过于泛)
- ✓ `单次完成型任务(一次 LLM 调用就完成的,short-term 一层就够)`

每个列表(适用/不适用)通常 3 项。少于 3 项这一栏看起来单薄。当帖子较短时,2+2 是可接受的。

### 手绘元素 (2 种)

1. "适用" 标头旁的琥珀色星星
2. "不适用" 标头旁的手绘 ×

### 模板

```html
<div style="position: relative; aspect-ratio: 3/4; background: #FFFFFF;
            padding: 22px 22px 18px 22px; display: flex; flex-direction: column;
            border: 1px solid #E8E2D6; border-radius: 8px; color: #1F1B16;
            box-sizing: border-box; overflow: hidden;">

  <!-- 角落数字、kicker、分割线、标题、gist(同 concept) -->

  <div style="margin-top: 14px;">
    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 11px; letter-spacing: 0.05em; color: #B23A26;
                margin-bottom: 8px; display: flex; align-items: center; gap: 4px;">
      <svg width="9" height="9" viewBox="0 0 9 9">
        <path d="M 4.5 0.5 L 5.4 3.6 L 8.5 3.6 L 6 5.5 L 7 8.5 L 4.5 6.6 L 2 8.5 L 3 5.5 L 0.5 3.6 L 3.6 3.6 Z"
              fill="#D4A017"/>
      </svg>
      <span>{适用_HEADER}</span>
    </div>
    <ul style="list-style: none; padding: 0; margin: 0 0 14px 0;
               font-size: 11.5px; line-height: 1.65; color: #1F1B16;">
      <li style="padding-left: 12px; position: relative;">
        <span style="position: absolute; left: 0; top: 7px;
                     width: 5px; height: 5px; background: #B23A26;"></span>
        {APPLY_BULLET_1 — 简短要点}
      </li>
      <!-- 重复 -->
    </ul>

    <div style="font-family: var(--font-serif); font-style: italic;
                font-size: 11px; letter-spacing: 0.05em; color: #8C7E68;
                margin-bottom: 8px; display: flex; align-items: center; gap: 4px;">
      <svg width="9" height="9" viewBox="0 0 9 9">
        <path d="M 1 1 L 8 8 M 8 1 L 1 8"
              stroke="#8C7E68" stroke-width="1.4" stroke-linecap="round"/>
      </svg>
      <span>{不适用_HEADER}</span>
    </div>
    <ul style="list-style: none; padding: 0; margin: 0;
               font-size: 11.5px; line-height: 1.65; color: #1F1B16;">
      <li style="padding-left: 12px; position: relative;">
        <span style="position: absolute; left: 0; top: 7px;
                     width: 5px; height: 5px; background: #8C7E68;"></span>
        {NOT_APPLY_BULLET_1}
      </li>
      <!-- 重复 -->
    </ul>
  </div>

  <!-- 收束卡上省略 trade-off(它已在"不适用"中隐含) -->
</div>
```

---

## 7. Flow card(流程卡,仅原则,模板尚未锁定)

顺序流水线。3–5 个阶段,中间带箭头。

**结构原语**:
- 阶段方框的垂直堆叠
- 每个阶段方框:类似架构卡的模块方框(图标 + 名称 + 密集描述),但有箭头向下指向下一阶段
- 可选:转换处的箭头标签("then"、"if X"、检查点标记)

**待真实 demo 跑过后再锁定** — 设计挑战在于让垂直箭头看起来有 editorial 味(而不是流程图味)。

---

## 8. Code card(代码卡,仅原则,模板尚未锁定)

带注释的关键片段。

**约束**:
- 使用 `font-family: var(--font-mono); font-size: 11px;`
- 背景:`#1F1B1605`(极淡的墨色染色,**不是**深色代码块)
- 最多高亮 1–3 行,`background: #B23A2615`
- 注释箭头 + 标签可指向某一行(用品牌红 0.8px)
- 片段长度:≤12 行。更长的代码:摘录或概述。

**待真实 demo 跑过后再锁定。**

---

## 密度规则(适用于所有卡片类型)

- **字数目标**:卡片正文(不含 kicker、页码、标题、gist、代价行)**220–300 个汉字等价**。正式清单见 SKILL.md 的 "Density floor"。
- **具体细节下限**:卡片正文 ≥ **6 个 specific 数据点**(数字、具名工具、具体场景、前后对比)。每条 bullet 必须带 ≥ 1 个 specific;概念卡的 bullet 必须带 ≥ 2 个 specific。
- **bullet 数量**:**4–6**。少于 4 条,列表读起来像"凑数"。多于 6 条,卡看起来过载。
- **每张卡的小节数**:最多 3 个不同小节(intro / 示意图 / 列表)再加代价行。再多碎片化会让扫读变难。
- **架构模块细节**:结构化 2 字段模式(见上文 "模块细节:结构化 2 字段模式")。单行模块细节是 v0;v1.1 要求垂直堆叠架构卡使用 2 字段。
- **陷阱卡的"实际"面板**:≥ 3 个 specific。揭示需要具体证据,而不只是反向论断。
- **贴纸倾斜**:每张卡最多 2 个倾斜元素。再多设计就会让人晕。
- **手绘元素**:每张卡 3–5 个,从 visual-system.md 的词汇表中挑。不要 7 个全用上。

### 如何在不破坏布局的情况下提升密度

当卡片正文 specific 太少时:
1. 给已有 bullet 加一个括号 `(具体 1, 具体 2)`——不改变视觉结构,只增加文本长度
2. 把单行模块细节改成 2 字段细节(架构卡)——每个模块多约 12px
3. 如果概念卡缺铺垫语境,加一个"现状"着色框
4. 如果架构卡缺运行时流程描述,加"数据流"行

当卡片正文超过 300 字上限时:
1. 先精简括号(保留 1 个 specific,丢掉第二个澄清)
2. 删掉架构卡上可选的 intro 行
3. 如果"数据流"已经传达了要点,删掉"关键"标注
4. 把 bullet 数量减 1 (5 → 4)
5. 最后才考虑:拆成两张卡(对 3:4 来说一张确实太密)
