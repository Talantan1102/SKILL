# Card Templates (v1)

Seven card types, all locked. Templates assume the v1 visual system (white BG, 1px border, no footer, hand-drawn elements, amber as secondary accent).

## Card type taxonomy

| Type | Used for | Frequency in a typical post |
|---|---|---|
| **Cover** | First card, hook | 1× per post (always) |
| **Concept** | Defining a non-obvious idea, framing a problem | 0–2× |
| **Architecture** | Structural overview (parallel facets / modules) | 0–1× |
| **Flow** | Sequential pipeline | 0–1× |
| **Compare** | Side-by-side or before-after structural comparison | 0–2× |
| **Code** | Key snippet with annotations | 0–2× |
| **Pitfall** | Counterintuitive trap or "I assumed X" moment | 1–3× (war-story posts) |
| **Summary** | Closing card with takeaways + 适用/不适用 | 1× per post (always) |

A typical 7-card post: cover + concept + compare + architecture + concept-or-pitfall + pitfall + summary.

---

## 1. Cover

The hook — and the single card that decides whether anyone in 小红书 feed reads the rest. Three locked archetypes (V1 / V2 / V3); pick one based on the chosen hook + the kind of evidence in the brief. Selection table: see `references/hook-patterns.md` "Anchor selection table".

**Mandatory rule:** every cover must contain one visual anchor — a big number (V1), a logo block (V2), or a mini schematic (V3). White bg + small text + corner decoration is no longer a valid cover; that's the v0 failure mode and it disappears in 200px feed thumbnails.

### V1 — Number Hero (light bg)

For Hook A (数字反差) and Hook B when the structural change has a count (e.g. `43 → 7`).

**Structure:**
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

**Template:**

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

### V2 — Logo Block (dark poster)

For Hook B without numbers, Hook C (技术名词), Hook D (我以为). The brand / framework / model name carries the visual mass on a dark poster background. This is the strongest "thumb-stopping" archetype — it looks like an album cover at feed scale.

**Structure:**
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

**Template:**

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

**V2 rules:**
- Wordmark splits into 2 lines: brand/framework name (cream) on line 1, version/edition (brand red) on line 2. Either line may be the brand-red one — typically the shorter, more distinctive token.
- **Wordmark length cap:** if any wordmark line exceeds **12 visual chars** (Chinese count as 1, ASCII as 1) at 84px, the line will overflow a 360px card. Three options in order of preference: (1) abbreviate (`RadixAttention` → `RadixAttn` or `RA`); (2) drop to 64px and keep full name; (3) split across more lines. Don't shrink below 60px — that breaks the anchor rule.
- Use 0–3 inline data tags. Tags can be (a) **hard numbers** if the post has them and the cover wants a numeric preview, (b) **structural facts** (named components, layered concepts, framework families), or (c) **metadata** (version, license, release date). Pick consistently — don't mix metadata and numbers in the same row.
- Diagonal stripe is optional but recommended — it differentiates this from a generic "dark mode" Notion page.
- Footer text must be `#8C7E68` (tertiary) on dark bg, NOT cream — keeps the hero readable as the primary focus.

### V3 — Schematic Peek (light bg, schematic anchored)

For Hook C / D where there is **no well-known brand or framework name** to ride on, AND the mechanism's schematic is more memorable than any wordmark would be. Examples: a context-parallel zigzag split pattern, a 2D pipeline parallel grid, a dataflow shape like `Mamba` selective scan. The mini schematic is the anchor; the hero text shrinks to give it room.

**V3 is the rare fallback, not the default for Hook C.** If the post is about a named system (RadixAttention, SGLang, vLLM, FlashAttention, etc.), V2 wins because the brand wordmark gives stronger pre-attentive recognition than a schematic at thumbnail scale. Use V3 only when (a) there is no recognizable brand to put on the cover, OR (b) the schematic itself is iconic and recognizable across the engineer audience (rare).

**Structure:**
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

Use the schematic primitives in `visual-system.md` "Schematic SVG visual language". Hero text is 30-36px max — the schematic carries the visual weight, not the words. Subtitle is optional in V3 (the schematic is its own subtitle).

**Template skeleton** (full SVG content is post-specific, see hooks-patterns + schematic primitives):

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
        <!-- schematic content: 3-5 labeled boxes, arrows, amber loop -->
        <!-- see schematic SVG visual language in visual-system.md -->
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

### Picking V1 vs V2 vs V3

```
有硬 before-after 数字 / 可做大字 hero?  ──→ V1 Number Hero
        │ no
        ↓
有具名 brand / 框架 / 模型 / 版本?         ──→ V2 Logo Block
        │ no — 是一个抽象机制 (无品牌)
        ↓
                                        ──→ V3 Schematic Peek
```

**Default to V2.** Branded topics always go V2, even when the schematic is interesting — wordmark recognition beats schematic pattern-matching at 200px thumbnail scale. V3 is only for unbranded concepts (e.g. "zigzag split", "selective scan dataflow") where there is no recognizable name to put on the cover.

When in doubt between V1 and V2: if the headline number is a **single number-pair** (like `43 → 7`, `27% / 10%`), V1. If the headline is a **system/version** (like `DeepSeek V4`, `SGLang 0.5`), V2 — even if the post also has numbers (those go in tags or content cards, not the cover hero).

---

## 2. Concept card

Defines a concept. Includes a tinted "现状" sticky-note + mini-schematic + a bulleted "N 个 X" section.

### Structure

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

### Hand-drawn elements used (4)

1. Squiggle under the accent token in title
2. Amber star next to the accent token
3. Amber hand-drawn loop around key element in schematic
4. Hand-drawn × marks as bullet markers in the "N 个 X" list
5. Sticky-note tilt on the "现状" tinted box (counts as 5th if you want max density)

### Template

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
      {INTRO_BODY — 2-3 lines describing the situation}
    </div>
  </div>

  <div style="margin-top: 8px;">
    {SCHEMATIC_SVG — see schematic patterns in visual-system.md}
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
        {BULLET_1 with optional <b>emphasis</b> + parenthetical specifics}
      </li>
      <!-- repeat for bullets 2..N (3 to 5 max) -->
    </ul>
  </div>

  <div style="margin-top: auto; display: flex; align-items: center;
              gap: 6px; padding-top: 8px;">
    {TRADE_OFF_SVG_AND_LINE — see visual-system.md}
  </div>
</div>
```

### Bullets with parenthetical specifics (required)

Concept-card bullets must follow this pattern:
```
{symptom or claim} · <b>{key term}</b>（{specific 1}，{specific 2 or clarification}）
```

**Two specifics in parens, not one.** A specific is a number, a named tool, a concrete scenario, or a before/after. The two specifics should be different *kinds* — e.g. (concrete scenario, numerical consequence) — to layer the credibility.

Examples:
- `cosine sim 一刀切 · 时序丢光（早晨 vs 上周一视同仁，召回 ranking 完全失效）`
- `top-k 易塞满 16K context（k=20×800tok 就吃光，剩余 system+task 不够装）`
- `偏好被闲聊淹没（"喜欢 Python" 埋在 100 条 "thanks" 里，召回率 < 5%）`
- `长尾任务从未召回（embedding sim 偏向高频 query，新意图首次失败概率 ~ 70%）`
- `偏好 update 越积越多（旧条目不删，3 个月后 query 召回 5+ 条互相矛盾）`

The parenthetical is what makes the bullet *credible* to a peer reader — it signals lived experience. **Single-specific bullets pass v0 but fail v1.** Each bullet should give the reader two reasons to believe the author.

A concept card has 4–6 such bullets. Below 4 = card looks thin. Above 6 = visually crowded.

---

## 3. Architecture card

Shows N (3–6) parallel modules + their cooperation. Module boxes have dashed brand-red borders, cream backgrounds, lucide icons.

### Structure

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

### Layout density rules

- **3 modules** → 1 column (vertical stack), each module ~70–78px tall (with 2-field detail)
- **4–6 modules** → 2×2 or 2×3 grid; in grid mode, can fall back to 1-field detail (single dense line per module) if 2-field would overflow
- **7+ modules** → split into two cards or simplify; don't cram

### Module detail: structured 2-field pattern (required for vertical-stack architecture)

Each module's secondary block is **two short labeled lines**, not one dense line. The two fields capture *what the module IS* and *how it actually works*. The labels are italic-serif red, the detail is regular gray.

Pick the label pair that fits the module type:

| Module type | Field 1 | Field 2 | Example |
|---|---|---|---|
| Storage layer | `存储` | `召回` | `存储 SQLite KV，每条 50–200 字` / `召回 FTS5 全文 + LLM top-5 二次过滤` |
| Process / runtime layer | `触发` | `行为` | `触发 任务结束自动 nudge` / `行为 LLM 蒸馏 facts → 写 KV` |
| Data layer | `范围` | `持久化` | `范围 当前 step plan + tool 输出` / `持久化 完成 step 即清空，无独立 DB` |
| Integration | `输入` | `输出` | `输入 5KB 多轮原文` / `输出 200B 结构化 facts (~25:1 压缩)` |
| Generic fallback | `怎么用` | `不怎么用` | `怎么用 long-context 推理` / `不怎么用 检索式 query` |

Each field detail must contain **at least 1 specific** (number / named tool / file / scenario). A 2-field block with no specifics fails the density floor.

### Hand-drawn elements used (4)

1. Hand-drawn ellipse around the key word in title (amber)
2. Dashed red borders on module boxes
3. Tilted "关键" sticker (amber) at bottom
4. Star sticker peeking out of the "关键" sticker corner

### Template (3-module vertical variant)

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
    <!-- repeat module-box block for each module -->
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
          {FIELD_1_DETAIL — with specifics}<br/>
          <span style="font-family: var(--font-serif); font-style: italic;
                       color: #B23A26;">{FIELD_2_LABEL}</span>
          {FIELD_2_DETAIL — with specifics}
        </div>
      </div>
    </div>
  </div>

  <div style="margin-top: 8px; font-family: var(--font-serif); font-style: italic;
              font-size: 10px; color: #8C7E68; line-height: 1.5;">
    <span style="color: #B23A26; letter-spacing: 0.05em;">~ 数据流</span>
    &nbsp; {how modules cooperate at runtime}
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
                 margin-left: 6px;">{TAKEAWAY — 8-16 chars}</span>
  </div>

  <div style="margin-top: auto; display: flex; align-items: center;
              gap: 6px; padding-top: 8px;">
    {TRADE_OFF_LINE}
  </div>
</div>
```

### Lucide icon paths reference

(unchanged from v0)

| Concept | Lucide name | Path |
|---|---|---|
| Layered / context | `layers` | `<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>` |
| Workflow / routing | `workflow` | `<rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/>` |
| Shield / guard | `shield` | `<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>` |
| Database / state | `database` | `<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>` |
| Recovery / loop | `rotate-ccw` | `<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>` |
| Observability / eye | `eye` | `<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>` |
| Clock / timing | `clock` | `<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>` |
| History / timeline | `history` | `<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>` |
| GPU / hardware | `cpu` | `<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>` |

For others, search lucide.dev. Keep `stroke-width="1.6"`.

---

## 4. Compare card

Side-by-side or naïve-vs-ours comparison. The visual contrast IS the design — left side neutral/gray, right side brand-red emphasis.

### Structure

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

Left column: gray bullets (`#8C7E68`), neutral phrasing of pain points.
Right column: red bullets (`#B23A26`), with key terms bolded and red.

### Density floor for this card

Each bullet — both columns — must contain **≥ 1 specific** (number, named tool, concrete mechanism). Both columns get this rule because comparison only works when both sides are concrete. A vague-vs-vague compare card teaches nothing.

- ✗ `全部混在一起检索` / `三层独立检索` (both vague)
- ✓ `cosine sim 全部混着检（不带时间衰减）` / `三层各自检索（FTS5 + cosine + KV 三种召回）`

Right column bullets should bold + redden the **key term** (the substantive noun the technique introduces), with the rest of the bullet describing it. Visually this lets a skimmer absorb just the bold red words and still understand the post.

Bullet count: **4-5 per column**. 3 looks thin, 6+ visually crowds.

### Hand-drawn elements (3)

1. `vs` in title rendered in brand-red
2. Hand-drawn × marks for "naïve" header
3. Amber star for "ours" header

### Template

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
        <!-- repeat for left bullets -->
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
          {RIGHT_BULLET_1 with <b style="color:#B23A26;">key term</b>}
        </li>
        <!-- repeat for right bullets -->
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

## 5. Pitfall card

The "I assumed X but actually Y" card. Two stacked panels, the second with amber highlight (sticker-tilted).

### Structure

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

### Density floor for this card

The "实际" panel is the entire payoff of the pitfall card. It must contain **≥ 3 specifics** — without them the card is just an opinion. Use concrete forms:
- Numerical thresholds: `< 30 条样本里几乎随机` / `top-3 召回有 1-2 个噪声` / `约 50-100 个任务才进入可用区`
- Named mechanisms: `embedding ann 索引才有 cluster 结构` / `cosine sim 在小样本里坍缩`
- Time/scale: `前 1-2 周` / `accumulate 50+`
- Failure modes: `召回率 ~ 5%` / `延迟 +200ms`

The "看起来" panel can stay short (1-2 lines, just the assumption). Asymmetry between panels is intentional — the pitfall card sells *the gap*.

### Label conventions

- For analytical/解读 posts (you're explaining someone else's project): use `~ 看起来 / ★ 实际`
- For war-story/复盘 posts (you're writing about your own work): use `~ 以为 / ★ 结果`

### Hand-drawn elements (3)

1. Down arrow (custom SVG) between panels — brand-red
2. Star sticker on the "实际"/"结果" panel header
3. Sticker tilt (-0.6deg) on the "实际"/"结果" panel

### Template

```html
<div style="position: relative; aspect-ratio: 3/4; background: #FFFFFF;
            padding: 22px 22px 18px 22px; display: flex; flex-direction: column;
            border: 1px solid #E8E2D6; border-radius: 8px; color: #1F1B16;
            box-sizing: border-box; overflow: hidden;">

  <!-- corner number, kicker, rule (same as concept template) -->

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
        {EXPECTED_BODY — what you'd assume}
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
        {ACTUAL_BODY — what actually happens, with concrete details}
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

## 6. Summary card

The closing card. 适用 / 不适用 lists with bulleted takeaways.

### Structure

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

### Density floor for this card

Each bullet must include **a reason or specific in parens**, not just a category. The reader is deciding whether to adopt the approach — they need to see *why* each "适用" or "不适用" applies to them.

- ✗ `长期对话连续性是核心需求` (too generic)
- ✓ `长期对话连续性是核心需求（个人助手、24h+ 长任务 agent，需要 50+ 轮记忆）`
- ✗ `单次完成型任务` (too generic)
- ✓ `单次完成型任务（一次 LLM 调用就完成的，short-term 一层就够）`

Each list (适用/不适用) typically has 3 items. Below 3 the section looks thin. 2+2 is acceptable when the post is short.

### Hand-drawn elements (2)

1. Amber star next to "适用" header
2. Hand-drawn × next to "不适用" header

### Template

```html
<div style="position: relative; aspect-ratio: 3/4; background: #FFFFFF;
            padding: 22px 22px 18px 22px; display: flex; flex-direction: column;
            border: 1px solid #E8E2D6; border-radius: 8px; color: #1F1B16;
            box-sizing: border-box; overflow: hidden;">

  <!-- corner number, kicker, rule, title, gist (same as concept) -->

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
        {APPLY_BULLET_1 — short takeaway}
      </li>
      <!-- repeat -->
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
      <!-- repeat -->
    </ul>
  </div>

  <!-- trade-off omitted on summary cards (it's already implicit in 不适用) -->
</div>
```

---

## 7. Flow card (principle-only, template not yet locked)

Sequential pipeline. 3–5 stages with arrows between them.

**Structural primitives**:
- Vertical stack of stage boxes
- Each stage box: similar to architecture module box (icon + name + dense desc) but with arrow emerging downward to next stage
- Optional: arrow labels for the transition ("then", "if X", checkpoint markers)

**To be locked after a real demo run** — the design challenge is making vertical arrows feel editorial-tasteful (not flowchart-y).

---

## 8. Code card (principle-only, template not yet locked)

Key snippet with annotations.

**Constraints**:
- Use `font-family: var(--font-mono); font-size: 11px;`
- Background: `#1F1B1605` (very subtle ink tint, NOT a dark code block)
- Highlight 1–3 lines max with `background: #B23A2615`
- Annotation arrow + label can call out a specific line (use brand-red 0.8px)
- Snippet length: ≤12 lines. Longer code: excerpt or summarize.

**To be locked after a real demo run.**

---

## Density rules (apply across all card types)

- **Word count target**: **220–300 Chinese-character-equivalent** per card body (excluding kicker, page number, title, gist, trade-off line). See SKILL.md "Density floor" for the formal checklist.
- **Specificity floor**: ≥ **6 specific data points** per card body (numbers, named tools, concrete scenarios, before/after). Every bullet must carry ≥ 1 specific; concept-card bullets must carry ≥ 2 specifics.
- **Bullet count**: **4–6**. Below 4, the list reads as "padding". Above 6, the card looks too busy.
- **Sections per card**: at most 3 distinct sections (intro / schematic / list) plus the trade-off. More fragmentation makes scanning hard.
- **Architecture module detail**: structured 2-field pattern (see "Module detail: structured 2-field pattern" above). Single-line module detail is v0; v1.1 requires 2-field for vertical-stack architecture cards.
- **Pitfall 实际 panel**: ≥ 3 specifics. The reveal needs concrete proof, not just a counter-claim.
- **Sticker tilts**: at most 2 elements per card. More than that and the design gets disorienting.
- **Hand-drawn elements**: 3–5 per card per the visual-system.md vocabulary list. Don't combine all 7.

### How to grow density without breaking the layout

When the card body has too few specifics:
1. Add a parenthetical `(specific 1, specific 2)` to existing bullets — doesn't change visual structure, just text length
2. Convert single-line module detail to 2-field detail (architecture cards) — adds ~12px per module
3. Add a 现状 tinted box if the concept card lacks setup context
4. Add the 数据流 line if the architecture card lacks the runtime flow story

When the card body is over the 300 ceiling:
1. Trim parentheticals first (keep 1 specific, drop the second clarification)
2. Drop the optional intro line on architecture cards
3. Drop the 关键 callout if 数据流 already conveys the takeaway
4. Reduce bullet count by 1 (5 → 4)
5. As a last resort: split into two cards (one is too dense for 3:4)
