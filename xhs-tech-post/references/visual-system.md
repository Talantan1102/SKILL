# Visual System (v1)

The visual contract every card inherits. Constants, not parameters — brand-series consistency comes from rigid uniformity across posts.

## Color palette

```
Card background:   #FFFFFF  /* white — main canvas, locked for content cards 02+ */
Card border:       #E8E2D6  /* warm gray, 1px — defines card edge against page */

Tinted block bg:   #FAF5E8  /* cream — was the v0 main bg, now demoted to accent */
Primary ink:       #1F1B16  /* warm off-black — for hero/title text */
Secondary text:    #5A5246  /* warm gray — for body, captions */
Tertiary text:     #8C7E68  /* kicker, footer, faint UI */

Brand primary:     #B23A26  /* terracotta — key tokens, decorations, primary accents */
Brand deep:        #8C2A1B  /* darker terracotta — used as cover block bg in V2 dark mode */
Brand secondary:   #D4A017  /* deep amber — decorative stars, hand-drawn loops, "关键" sticker */
Amber-on-tint text:#8B6809  /* darker amber for text on amber-tinted bg (contrast) */

Border / divider:  #1F1B1622 /* primary ink at 13% — hairline rules */
Inner box border:  #1F1B1625 /* primary ink at 15% — subtle box outlines */
Dashed brand:      #B23A26 with stroke-dasharray — module boxes, sketched outlines */

/* Cover-only extensions (do not use on content cards) */
Cover dark bg:     #1F1B16  /* poster mode background, full bleed */
Cover cream-on-dark:#F5EDDC  /* hero text color when bg is dark */
Cover dim-on-dark: #8C7E68  /* secondary text on dark — same tertiary as light */
```

Color use rules:
- **Terracotta** is the primary brand color: kicker rule, key tokens in titles, ×-marks for negative bullets, trade-off triangle, schematic arrows, dashed module borders.
- **Amber** is decorative-only: hand-drawn stars, hand-drawn ellipses around emphasis words, "关键" callout sticker bg/border. Never used for body text or structural lines.
- **Cream** is for tinted blocks inside the white card: "现状" boxes, module box backgrounds, schematic terminal containers.
- Never use pure black `#000000` or pure white text on a colored bg.

## Typography

Two type families only:
- **Sans** (default): body, hero, titles, stats, module names
- **Serif italic** (`var(--font-serif)` + `font-style: italic`): kickers, schematic captions, section labels ("→ XXX" / "~ XXX"), trade-off line, data-flow notes, "关键" callout label

Two weights only:
- **400** (regular): body, descriptions, captions
- **700** (bold): hero, title, module names, stat numbers, bullet emphasis

Skip 600 entirely. Skipping a weight creates clearer hierarchy than gradual ramping.

### Type scale

```
Cover hero (number / arrow):  72-96px / 700 / line-height 0.92 / letter-spacing -0.03em
Cover hero (logo / wordmark): 64-90px / 700 / line-height 0.95 / letter-spacing -0.02em
Cover hero (text-on-schematic): 30-36px / 700 / line-height 1.1 (used only when schematic is the anchor)
Card title:              21-23px / 700 / line-height 1.2 / letter-spacing -0.01em
Gist line:               12px / 500 / brand-red color
Body / intro paragraph:  11-12px / 400 / line-height 1.55
Bullet list:             10.5-11px / 400 / line-height 1.55-1.6
Module name (in box):    11px / 700
Module description:      10px / 400 / line-height 1.4
Schematic label (inside):10-11px / 400 / serif italic / fill ink
Schematic caption (below):9-10px / 400 / serif italic / fill secondary text
Section label:           10px / 400 / serif italic / tracking 0.05em / brand-red OR amber
Kicker:                  11px / 400 / serif italic / tracking 0.05em
Stat label:              10px / 400 / serif italic / tracking 0.05em
Stat number:             17-18px / 700
Trade-off line:          11px / 400 / serif italic / secondary text
Data-flow note:          10px / 400 / serif italic / secondary text (with red marker prefix)
Corner page number:      70-78px / 700 / serif / outlined (text-stroke) / opacity 0.4-0.5
```

## Card frame (shared by cover and all content cards)

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

`box-sizing: border-box;` always. Use `margin-top: auto;` on the trade-off line to push it to the card bottom.

## Cover anchor system (v2)

**The single rule that overrides all others:** the cover must be readable when displayed at 200px wide in the 小红书 feed thumbnail. If the visual main element disappears at that scale, the cover has failed. Test with: open the HTML, browser zoom to 25% — can you tell what the post is about from the cover alone?

### Mandatory: 1 visual anchor (one of three)

**Anchor (a) — Number anchor**

A large number, arrow, or before-after pair. Use when the post has a hard measurable result.

- Numerals: 80-96px, weight 700, line-height 0.92
- Arrow `→` rendered in brand red, same size class as the numerals
- Occupies ≥ 25% of card area
- Often the entire vertical center of the cover

**Anchor (b) — Logo block**

A brand / framework / model name as a large wordmark, typically inside a colored block or as the central mass of a dark/poster cover. Use when the post is about a named system (DeepSeek V4, SGLang, GRPO, etc.) or when the post has no single hero number.

- Wordmark text: 64-90px, weight 700
- Color: cream `#F5EDDC` on dark `#1F1B16` background, OR primary ink on cream block, OR mixed (one word in primary ink, the version/edition in brand red)
- Block fill OR full-bleed bg covers ≥ 30% card height
- Diagonal stripe / corner block is allowed as a secondary accent

**Anchor (c) — Schematic peek**

A minimal architecture / data-flow diagram, hand-drawn-feeling. Use when the mechanism IS the hook (hooks C and D), and the post does not have a single dominant number.

- Min size: 100×80px (occupies right or center band of card)
- ≥ 3 labeled elements (boxes, arrows, or layered shapes)
- Stroke 1px brand red, captions in serif italic, dashed connectors
- Hero text shrinks to 30-36px to make room for the schematic

### Mandatory supporting elements (every cover)

- **Kicker line** + 32×1.5px brand-red rule below it (top-left)
- **Read-time stamp** at the bottom (`读完约 X 分钟`, computed from total content word count ÷ 300 + 0.3 min/card; for cover-only renders or drafts, use a placeholder estimate based on planned card count and refine after content cards exist)

### Optional supporting elements (pick 1–2, no more)

- **Outlined volume number** (top-right) — font-size 70-78px, text-stroke 1px, opacity 0.4 on light bg, opacity 0.25 on dark bg. **Optional**, not the anchor.
- **Diagonal stripe** (corner) — brand red, 6-8px wide, 30°-45° angle, runs from one edge into the cover. Replaces the v0 3-bar stack.
- **Author signature pill** — bottom-left, only on cover. `谭磊 · 类目` in tertiary text, with brand-red dot prefix.
- **Edition/series mark** — like `Vol.01` or `note 02 / 04`, in serif italic, tertiary text.

### Banned on cover

- The v0 3-bar descending stack as a primary visual — alone it does not anchor
- Centered, text-only, no anchor — the "Notion screenshot" failure mode
- Hero text smaller than 60px with no other anchor element
- Volume number used as the anchor (it's decoration)
- Multi-color hero (one accent only — brand red OR cream-on-dark, never both)

**No author signature on content cards.** Xiaohongshu app already shows the author handle next to the post; printing it on every card is redundant. Cover may have it as the optional pill (above).

## Content card decorations

Content cards drop:
- Decoration 4 (3-bar stack) — cover-only flair
- Decoration 5 (read-time) — replaced by trade-off line

Content cards add the v1 hand-drawn / playful element vocabulary (use 3–5 per card):

### Element vocabulary (use sparingly, max 5 per card)

| Element | When to use | Implementation |
|---|---|---|
| **Squiggle underline** | Under one key phrase in title (usually the accent-colored token) | `<svg viewBox="0 0 65 8"><path d="M 1 5 Q 10 1 20 5 T 40 5 T 64 5" stroke="#B23A26" stroke-width="1.6" fill="none"/></svg>`, absolute-positioned beneath text |
| **Amber star** | Next to a section label or as a sticker on a callout | Pentagon-star SVG path filled `#D4A017`, 9–14px |
| **Hand-drawn ellipse** | Loop around a key word in title | `<svg viewBox="0 0 42 22"><path d="M 5 11 Q 2 4 21 3 Q 39 4 38 11 Q 37 19 21 19 Q 4 19 5 11 Z" stroke="#D4A017" stroke-width="1.4" fill="none"/></svg>`, absolute behind text with `z-index: -1` |
| **Hand-drawn × bullet** | Bullet marker for negative-toned lists ("hidden costs", "踩坑", "不适用") | `<svg viewBox="0 0 9 9"><path d="M 1 1 L 8 8 M 8 1 L 1 8" stroke="#B23A26" stroke-width="1.4"/></svg>`, 9px |
| **Hand-drawn loop highlight** | Around a key element in schematic (the "vector store" callout) | Imperfect closed Bézier path, `stroke="#D4A017"`, 1.2px |
| **Sticker tilt** | Apply to one element only — usually a tinted callout box | `transform: rotate(-0.6deg)` to `rotate(-0.7deg)` |
| **Dashed border** | Module boxes (architecture cards) | `border: 0.8px dashed #B23A26` |

Don't combine all 7 in one card. Pick **3–5** that fit the content shape:
- Concept card with bullets: squiggle + star + ×-bullets + tilted box (4)
- Architecture card: ellipse around key word + dashed module borders + sticker callout (3 elements; modules count as one repeated element)
- Compare card: ×-bullets on left + squiggle on right header (2 elements; restraint is right here, the comparison itself is the visual)

## Section label conventions

Section labels appear inside cards to chunk content. Two styles, pick by tone:

- **`→ XXX`** — neutral/structural sections ("→ 现状", "→ 4 个隐藏成本", "→ 关键", "→ 数据流")
- **`~ XXX`** — softer/casual sections ("~ 现状", "~ 顺手记一下"), use for sticky-note style boxes

Both are serif italic 10px, letter-spacing 0.05em, color either `#B23A26` (red) or `#8C7E68` (gray) depending on emphasis.

When a section label is paired with a star pictogram (`<svg>` 9px amber), put the star to the left of the label text.

## The "data-flow note" (for architecture cards)

A new structural element introduced in v1: a one-line italic-serif annotation **below** module boxes, prefixed with a red `~ 数据流` label, summarizing how the modules cooperate at runtime.

```html
<div style="margin-top: 8px; font-family: var(--font-serif); font-style: italic;
            font-size: 10px; color: #8C7E68; line-height: 1.5;">
  <span style="color: #B23A26; letter-spacing: 0.05em;">~ 数据流</span>
  &nbsp;
  {one-line description of how modules feed each other at runtime}
</div>
```

This converts a static structural diagram into a dynamic mental model — readers see not just "what the parts are" but "how they actually work together". Required on architecture cards, optional on concept cards if the concept involves multiple cooperating subparts.

## The "关键" callout (sticker style)

When a card needs to land a single takeaway line at the end of body content, use a tilted amber sticker:

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
               margin-left: 6px;">{takeaway, 8-16 chars}</span>
</div>
```

Use sparingly: at most one "关键" sticker per card. Recommended on architecture cards, summary cards.

## Schematic SVG visual language

When a card embeds a schematic (concept-card mini-diagram, etc.):

- viewBox typically `0 0 280 X`
- Stroke widths: 0.5–0.8px for shapes, 0.6–0.8px for arrows. Hairline.
- **Connectors use dashed lines** (`stroke-dasharray="2 2"`) for "data flow" or "ingestion" semantics — feels more notebook than blueprint.
- Boxes: `fill="none"` (outline) OR `fill="#FAF5E8"` (cream tint)
- Arrows: brand-red 0.8px stroke + 6px polygon arrowhead. Never unicode `→` inside SVG.
- Labels: serif italic, 9–11px, `fill="#5A5246"` for captions or `#1F1B16` for in-box labels
- Add ONE hand-drawn loop highlight (amber, imperfect Bézier path) to draw attention to the key element

## Trade-off line (the credibility multiplier, kept from v0)

Same as v0:

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
    代价 · {trade-off text in 8-16 chars}
  </span>
</div>
```

In v1 layout, this is the **last visible element on the card** (footer was removed). Use `margin-top: auto;` to push it to the bottom.

If a card has no real trade-off, omit. Forced trade-offs read as fake humility.

## Icon usage (lucide library)

Same as v0 — lucide outline icons in brand-red, stroke 1.6px, sizes 12/14/15/16px. Hand-drawn icons reserved for brand-specific symbols (caveat triangle, amber star sticker) and schematic primitives.

## Density target

A v1 content card body must contain **220–300 Chinese-character-equivalent words** of substantive content, excluding kicker, page number, title, gist, and trade-off line. Below 220 reads as filler. Above 300 crowds the card at 3:4 aspect.

Density is not just word count — it is **specificity**. Every card must contain ≥ 6 specific data points (numbers, named tools, concrete scenarios, before/after comparisons). A 280-character card with 0 specifics fails; a 240-character card with 8 specifics passes. See SKILL.md "Density floor" for the formal checklist.

Concrete content elements per card type:
- **Concept card**: title + gist + intro tinted box (2-3 lines) + schematic + N-item bulleted list (4-6 items, each with **2 specifics in parens**) + trade-off
- **Architecture card**: title + gist + (optional) intro line + 3-6 module boxes (each with **structured 2-field detail**) + data-flow note + (optional) key callout + trade-off. If modules use the dense 2-field pattern, intro line and key callout become optional — the modules carry the substance.
- **Compare card**: title + gist + 2 columns (4-5 items each, each with **≥ 1 specific**) + trade-off
- **Pitfall card**: title + gist + 看起来/实际 (or 以为/结果) panels — 实际 panel must have **≥ 3 specifics** + trade-off
- **Summary card**: title + gist + 适用/不适用 lists (each item with reason in parens) + trade-off
- **Code card**: title + gist + code block + 2-3 annotation bullets with **specifics** + trade-off

## Spacing rhythm

Vertical rhythm uses these values, in order of preference:
- 4px, 6px, 8px, 10px, 12px, 14px, 16px, 18px, 22px

Avoid odd values (e.g., 11px, 19px). Avoid arbitrary px (e.g., 17px).
