---
name: xhs-tech-post
description: Use this skill whenever the user wants to draft, design, or generate a Xiaohongshu (小红书 / RedNote) post about a technical engineering topic — LLM training, inference infrastructure, agent systems, model architecture, RAG, distributed systems, or any peer-targeted technical writeup. Triggers include phrases like "帮我写一篇小红书", "做一张小红书技术贴", "我想把 X 发到小红书", "RedNote 技术贴", or when the user provides a code repo / paper / blog URL with the goal of turning it into Xiaohongshu content. The skill produces a complete post — cover image (3:4 HTML) + 7–9 content cards + post body text + hashtags — using editorial-restrained design tuned for engineer audiences (cream background, terracotta accent, lucide icons, no clickbait language). Apply this skill even if the user only loosely mentions Xiaohongshu, RedNote, or "技术贴 / 知识卡片" formatting.
---

# Xiaohongshu Tech Post

Generate complete Xiaohongshu posts targeting fellow engineers — covers, content cards, post body, and hashtags — in a consistent editorial visual language.

## Audience and intent

The reader is a fellow engineer (LLM apps, inference infra, ML systems, agents) at roughly the author's seniority. They will judge the post on:
- whether the author has actually shipped the thing being described
- information density and specificity (numbers, named tools, concrete decisions)
- whether trade-offs are honestly disclosed

This means the design and writing style differs from mainstream Xiaohongshu lifestyle posts. Avoid clickbait words: 绝绝子, YYDS, 神器, 封神, 震惊, 永远不要 X, 99% 的人不知道, emoji-heavy openings. These are negative signals to the target audience.

But the design isn't pure editorial restraint either — v1 deliberately uses hand-drawn doodles (squiggles, stars, hand-drawn loops, × bullets, sticker tilts) and a secondary amber accent to keep the visual lively. The goal: peer-engineer credibility (specifics, honesty, no hype) + scrapbook-style visual energy (so the deck doesn't feel like a sterile internal presentation). Both pieces matter.

## Inputs the skill accepts

The user may provide one of:

1. **A topic string**: "我想写一篇关于 GRPO reward hacking 的复盘"
   → Skill should ask 2–3 quick clarifying questions about specifics (a concrete anchor, the key insight, trade-off) before generating.

2. **A code repo path or URL**: "把 sgl-project/sglang 里的 PCP 实现做成一篇贴"
   → Read README + key directories. Identify the architecture / mechanism. Propose a card map; let the user confirm before generating.

3. **A paper (PDF or arXiv URL)**: "把这篇论文做成笔记"
   → Use pdf-reading skill to extract abstract, key claim, headline numbers, and at least one figure/table. Map to card sequence.

4. **A blog post or article URL**: web_fetch → extract claims → reorganize into card sequence.

If the input is ambiguous, default to **interactive mode**: ask the user to confirm scope, key insight, and one specific number/example before generating any HTML.

## Output format

A complete post is delivered as a single HTML file with all cards rendered side-by-side, plus a markdown block at the bottom containing:
- **Post body** (正文): 80–150 字, conversational but technical, no clickbait words
- **Hashtags** (话题): 3–5 tags, mix of broad ("#AI工程师") and specific ("#SGLang #ContextParallel")

The user screenshots each card individually from the HTML to upload to Xiaohongshu (each card is `aspect-ratio: 3/4`, no extra surrounding chrome).

A finished post has:
- 1 cover (page 01)
- 7–9 content cards (pages 02–N)
- 1 post body text + hashtags

## Process

Follow these steps in order. Don't skip step 1 — the post quality is determined more by the brief than by the templates.

### Step 1 — Build the post brief (Brief Gate)

Consult `references/brief-gate.md`. Emit a complete brief YAML block before generating any HTML. The 6 required fields:

| Field | What goes here |
|---|---|
| `topic` | One-line: "把 43 个 tool 重构成 7 个 Skill 渐进披露" |
| `key_insight` | One-line: the non-obvious idea that ties the post together |
| `evidence` | Hard numbers / before-after / named mechanism or tool / concrete scenario. **Required.** A post without at least one concrete anchor is rejected. See `brief-gate.md` for the four anchor types. |
| `trade_off` | What did this cost? **Required**, even if mild. Honesty is a credibility multiplier with this audience. |
| `audience_anchor` | What familiar concept does the reader already know that this builds on? Used to make abstractions land. |
| `chosen_hook` | Pick one of the 4 cover hooks (A/B/C/D) — see `references/hook-patterns.md` for selection rules. |

If `evidence` or `trade_off` is missing, follow the refusal protocol in `brief-gate.md`. Do not fabricate. Only proceed to Step 2 once the brief is complete (or the user has explicitly invoked the evidence override).

### Step 2 — Plan the card sequence

Map the brief to 7–9 cards. Card-type taxonomy and selection rules are in `references/card-templates.md`. The default sequence for a 实战复盘 post:

1. **Cover** — chosen hook
2. **Concept card** — what is this thing (with mini schematic if non-obvious)
3. **Setup card** — context: what was the situation before, why it matters
4. **Architecture / flow card** — the structural change you made
5. **Pitfall card** — the trade-off or counterintuitive thing
6. **Result card** — the numbers (compare / data layout)
7. **Summary card** — 3–5 takeaways

Adjust to the topic. A pure optimization post might skip the architecture card and have 2 result cards. A pure war-story might skip the architecture card and have 2 pitfall cards. Don't force-fit.

### Step 3 — Generate cards in order

For each card, follow the template in `references/card-templates.md`. All cards inherit the visual contract from `references/visual-system.md` — same kicker, same color, same corner page number, same footer pattern.

Hard rules across all cards (these are the ones that, if violated, undermine credibility):
- Every card has a **specific anchor** — a number, named entity, code reference, or before/after pair. Never purely abstract.
- Every card has at most **one main claim**. Two claims → split into two cards.
- The trade-off line (small triangle + italic line) appears on cards where there's a real cost worth disclosing — not every card.
- The hero token (the brand-red highlighted word) is the most technical-but-still-readable token in the title — usually a proper noun (RadixAttention, Zigzag) or a delta (43→7).

### Step 4 — Generate the post body and hashtags

The post body (正文 in Xiaohongshu's compose box) sits below the images. Length 80–150 字. Structure:
- Sentence 1: restate the core insight in plain language
- Sentence 2–3: one concrete detail or context the cards couldn't fit
- Sentence 4 (optional): an honest invitation to discuss — "卡 N 那块的实现我还在迭代，有同行做过类似的可以评论区交流"

Ban list (do not generate): 绝绝子, YYDS, 神器, 封神, 震惊, 你不知道的 X, 99% 的人, !!!, 多个连续 emoji.

Hashtags: 3–5, ordered specific → broad. Example: `#SGLang #ContextParallel #LLM推理 #大模型 #AI工程师`. Don't pad with irrelevant trending tags.

### Step 4.5 — Pre-flight QA

Consult `references/qa-checklist.md`. After all cards + post body + hashtags are drafted, emit the QA table for the user. Auto-regenerate any FAILing card (only that card, capped at 2 attempts); surface coherence ✗ items to the user. Only proceed to Step 5 when all cards PASS and all coherence checks are ✓ (or explicitly accepted by the user).

### Step 5 — Output and instructions for export

Render all cards into a single HTML file: `xhs-post-<short-topic-slug>.html`. The HTML wraps cards in a `display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 360px));` layout for browser preview.

Tell the user:
- "Open the HTML in a browser. Each card is `aspect-ratio: 3/4`. Right-click → 'Inspect' → screenshot each card individually (or use a browser screenshot tool that captures by selector). Recommended export size: at least 1242×1656 px to satisfy Xiaohongshu's image quality threshold."

## Hard constraints

These apply globally across the skill. They encode the design we agreed on; deviating from them creates inconsistency across posts that defeats the brand-series effect.

### Visual constants (locked)

These come from `references/visual-system.md`. They are **not** parameters:
- Content card background: `#FFFFFF` (white) — locked
- Cover background: `#FFFFFF` light, `#1F1B16` dark, or split block — see cover archetypes below
- Card border: `1px solid #E8E2D6` (warm gray) for light surfaces; `none` on dark covers
- Tinted block bg: `#FAF5E8` (cream — used inside cards as accent surface)
- Primary ink: `#1F1B16`
- Secondary text: `#5A5246`
- Tertiary text / kicker: `#8C7E68`
- Brand primary (terracotta): `#B23A26`
- Brand secondary (amber, decorative-only): `#D4A017`
- Card aspect ratio: `3/4`
- Two type families only: `var(--font-sans)` for body, `var(--font-serif)` italic for kickers, section labels, schematic captions, trade-off lines, data-flow notes
- Border radius: `8px` for cards, `4px` for inner boxes, `2px` for SVG rects

### Cover anchor (1 mandatory + 2–3 supporting)

**The most important rule in this skill.** A cover that fails to land in 小红书 feed thumbnail (~200px wide) has wasted the entire post.

Every cover MUST contain exactly **one visual anchor** from this list:

| # | Anchor type | Minimum spec | Pairs with hook |
|---|---|---|---|
| (a) | **Number anchor** — big number / arrow / before-after pair | Numerals ≥ 80px, occupies ≥ 25% card area | Hook A (always), Hook B (when ratio is the headline) |
| (b) | **Logo block** — brand or framework name as visual mass | Wordmark ≥ 64px, in a colored block ≥ 30% card height OR contrasted on dark bg | Hook B, Hook C |
| (c) | **Schematic peek** — minimal architecture diagram | ≥ 100×80px with ≥ 3 labeled elements | Hook C, Hook D (when the mechanism IS the hook) |

The anchor is **the single thing that must remain readable** when the card is displayed at 200px wide. If it's not, regenerate.

Supporting decorations (2–3 of):
- Outlined volume number (top-right, optional on dark covers)
- Kicker line + 32×1.5px brand-red rule (mandatory — sets brand series)
- Diagonal stripe / dashed corner pattern (optional — replaces v0's 3-bar stack)
- Read-time stamp (mandatory — the only place it appears in the post)

The 3 cover archetypes are detailed in `references/card-templates.md` (Cover variants V1 / V2 / V3) with full HTML for each. The archetype is selected by the chosen hook + the kind of evidence the post has — `references/hook-patterns.md` has the selection table.

### Content card variations from cover

Content cards inherit decorations 1–3 from cover, but:
- Decoration 4 (3-bar stack) is **dropped** — content cards use that real-estate for info density
- Decoration 5 (read-time stamp) is **dropped** — read-time is post-level metadata, lives on the cover
- The footer row (author signature + page indicator) is **removed entirely** — Xiaohongshu's app shows the author next to the post; reprinting it on every card is redundant and noisy
- Corner number is the **page number** (02, 03, …), not the post number
- The trade-off line (small triangle + italic line) becomes the **last visible element** on the card, pushed to bottom with `margin-top: auto`

In addition, content cards layer in v1's hand-drawn / playful vocabulary (3–5 elements per card from this list):

- Squiggle underline beneath the accent token in the title
- Amber star pictogram next to a section label or sticker
- Hand-drawn ellipse around a key word in the title (amber)
- Hand-drawn × bullets for negative-toned lists (hidden costs, pitfalls, 不适用)
- Hand-drawn loop highlight around an element in a schematic (amber)
- Sticker tilt (`rotate(-0.6deg)` to `rotate(-0.7deg)`) on one tinted element
- Dashed brand-red borders on module boxes (architecture cards)

Each card type has its own canonical 3–5 element combo — see `references/card-templates.md`.

### Hook patterns (4, no others)

Cover hook is one of A/B/C/D — see `references/hook-patterns.md`. No other hook types. If a post can't be expressed in one of these 4, the topic is probably wrong for this format.

### Banned design moves

Do not use:
- Any background color other than `#FFFFFF` for **content cards** (cards 02+). Covers may use the dark/tinted variants in `card-templates.md`.
- Pure black text (use the warm off-black `#1F1B16`)
- Multi-color hero (only one accent token, in brand-red `#B23A26`)
- Amber `#D4A017` for body text or structural lines (amber is decorative-only — stars, hand-drawn loops, "关键" sticker)
- `font-weight: 600` (skip from 500 to 700; 600 reads as "design indecision")
- Gradient fills, drop shadows, glow effects, blur
- Emoji in card content (`✅⚠️🎉🔥` etc.) — the design has custom geometric icons + lucide for these roles
- All-caps Chinese phrases
- More than 3 hashtags inside a single card body (hashtags belong in the post body block, not on cards)
- Author signature on content cards (the platform shows it; printing it on cards is noise)
- More than 2 sticker-tilted elements per card (disorienting)

#### Cover-specific bans (failure modes from prior runs)

- **Hero text < 60px when there is no other anchor** — reads as a blank card at thumbnail scale
- **Centered-text-only layout with no anchor** — the all-white "Notion screenshot" failure mode
- **3-bar stack as the only visual element** — was v0's main decoration; alone, it does not anchor
- **Subtitle that resolves the curiosity** — covers should provoke a swipe, not summarize the post
- **Volume number used as the anchor** — outlined corner number is decoration, not anchor
- **Multi-color hero on cover** — exactly one accent color (brand red OR cream-on-dark), never both

### Density floor (every content card must satisfy)

A card that fails any of these checks isn't ready to ship:

1. **≥ 6 specific data points** in the card body. A "specific" is **one** of:
   - A number (count, percentage, ratio, size, version, time, threshold)
   - A named tool / library / function / file / API / config flag (`SQLite`, `FTS5`, `cosine sim`, `top-k`, `tokenizer.json`, etc.)
   - A concrete scenario in parentheses (`"喜欢 Python" 埋在 100 条 "thanks" 里`)
   - A before/after or vs comparison (`25K → 10K`, `vanilla vs 三层`)
2. **Body content 220–300 Chinese-character-equivalent** (excluding kicker, page number, title, gist, trade-off line). Below 220 = filler. Above 300 = crowded at 3:4.
3. **No bullet without specifics.** A bullet of pure assertion ("this is bad", "performance improves", "更快了") fails. Every bullet must contain at least one specific from the list above. Concept-card bullets must have **two** specifics (see `card-templates.md` for the canonical pattern).
4. **Architecture module detail uses the structured two-field pattern** (see `card-templates.md`). A single dense line is not enough.
5. **Pitfall "实际" panel ≥ 3 specifics.** The whole point of the pitfall card is the surprise reveal — it needs concrete proof.

The density floor is non-negotiable. If the source material doesn't yield enough specifics, the card type is wrong (probably should be a different card type, or the content should be merged into a denser card).

## References

When generating a post, consult these files as needed. Read them once at the start of the session — they're stable and you'll re-use the same patterns across posts.

| File | When to read |
|---|---|
| `references/visual-system.md` | At session start. The visual contract that all cards inherit. |
| `references/hook-patterns.md` | When picking the cover hook (Step 1, `chosen_hook` field). |
| `references/card-templates.md` | When generating each card (Step 3). Has full HTML templates for concept and architecture cards; principles + skeletons for the rest. |
| `references/post-structure.md` | When planning card sequence (Step 2). Rules of thumb for different post types. |
| `assets/example-post.html` | When you want to see a complete reference output. Useful for calibrating density and pacing. |

## A note on iteration

This skill is **v1**. Five card types have fully-locked HTML templates: `cover`, `concept`, `architecture`, `compare`, `pitfall`, `summary`. Two are still principle-only: `flow` and `code` — their visual language hasn't been validated through real demo runs yet. When generating a post that needs a not-yet-locked card type, follow the principles in `card-templates.md` and the visual constants — the resulting card may need user feedback to lock the template for the next iteration.
