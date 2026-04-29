# Pre-flight QA Checklist

Mandatory self-audit emitted at the end of Step 4, before Step 5. The model computes the metrics, emits the table, and auto-corrects any FAILs before delivering to the user.

## Per-card metrics

| Metric | How computed | PASS threshold |
|---|---|---|
| `char_count` | Chinese-character-equivalent count of card body, excluding kicker, page number, title, gist, and trade-off line | 220 ≤ x ≤ 300 |
| `specifics` | Count of: numbers, named tools/libraries/files/APIs/config flags, parenthetical concrete scenarios, before/after or vs comparisons | ≥ 6 |
| `hand_drawn_elements` | Count of distinct elements drawn from the `visual-system.md` vocabulary used in the card | 3 ≤ x ≤ 5 |
| `trade_off_present` | Boolean — does the card carry a trade-off line | PASS if (a) trade-off line is present, OR (b) card type is `summary`, OR (c) the model emits an explicit `trade_off_skipped_reason` (≤ 16 chars, e.g. "纯解释卡", "无实际代价") |
| `bullet_specifics_floor` | Every bullet has ≥ 1 specific; concept-card bullets have ≥ 2 specifics | true for all bullets |

A card PASSes only if every metric PASSes.

## Cover-specific checks

Source rules: `visual-system.md` "Cover anchor system v2", `hook-patterns.md` "Anchor selection table" + "Cover failure modes". The cover is the post's single shot at thumbnail recognition; cover failures sink the post even if every other card passes.

| Metric | How computed | PASS threshold |
|---|---|---|
| `archetype` | Which V1/V2/V3 was used | One of V1 (Number Hero) / V2 (Logo Block) / V3 (Schematic Peek) — not a v0 hybrid |
| `anchor_present` | One of (a)/(b)/(c) anchors visible | (a) numerals ≥ 80px or (b) wordmark ≥ 64px or (c) schematic ≥ 100×80px with ≥ 3 elements |
| `thumbnail_readable` | Anchor stays legible at 200px-wide thumbnail | Render the HTML, browser zoom 25%, the anchor must still register pre-attentively |
| `failure_mode_clear` | Not matching any pattern in `hook-patterns.md` "Cover failure modes" | None of: Notion-screenshot / buried-anchor / subtitle-spoiler / decoration-as-anchor |
| `supporting_count` | Count of supporting decorations (kicker/rule/read-time/stripe/VOL/corner-number) | 2 mandatory (kicker+rule, read-time) + 0–2 optional. Total ≤ 5. |
| `subtitle_role` | Subtitle gives structural context, not the answer | Subtitle is workload/version/scale/series — does not summarize the post thesis |

A cover PASSes only if every metric PASSes. If `archetype` doesn't match `chosen_hook` per the hook-patterns selection table, surface as a coherence ✗ — propose switching the hook OR the archetype, await user confirmation.

## Post-level coherence checks

Source rules: `post-structure.md`.

- [ ] Kicker text is identical across all cards (only the page number changes)
- [ ] Cover and Summary's first-takeaway echo each other
- [ ] One-sentence narrative arc has zero "and"s / "和" / "而且"
- [ ] No card is removable without damaging the narrative
- [ ] At least one pitfall card present (or explicit justification why not)
- [ ] Cover archetype matches chosen hook per `hook-patterns.md` Anchor selection table

## QA table format (user-visible output)

The model emits this Markdown block at the end of Step 4:

```markdown
## Pre-flight QA

### Cover (01)
| Archetype | Anchor | Thumbnail | Failure mode | Supports | Subtitle | 状态 |
|---|---|---|---|---|---|---|
| V2 Logo Block | DeepSeek/V4 84px wordmark, dark bg | ✓ readable @ 200px | clear | 4 (kicker+rule, VOL, corner triangle, ghost 01) | "三件套同时换装" — structural | PASS |

### Content cards
| 卡 | 字符数 | specifics | 手绘元素 | trade-off | 状态 |
|---|---|---|---|---|---|
| 02 concept | 248 | 7 | 4 (squiggle, star, ×, tilt) | ✓ | PASS |
| 03 architecture | 195 | 4 | 3 | — | **FAIL** (<220 字 / specifics<6) |
| 04 pitfall | 281 | 9 | 3 | ✓ | PASS |
| ...

### 一致性
- [✓] kicker 一致 ("agent harness · note 02")
- [✓] cover ↔ summary 首条呼应
- [✓] cover archetype 配对 hook (Hook B + numbers → V1 Number Hero ✓)
- [✓] one-sentence arc: "<the sentence>"
- [✗] 卡 05 是否多余? → 建议合并入卡 04

### Action
卡 03 不达标。改动:在"召回"模块加 2 个 specifics(FTS5 top-k=20、p95 120ms),字符推到 240,specifics 到 7。重生成中。
```

## Trigger protocol

| Situation | Model action |
|---|---|
| Any card FAILs | Regenerate ONLY that card (others stay), with an explicit fix targeting the named metric. Re-run QA on the regenerated card. Do NOT show user the failing version. Cap at 2 regen attempts per card — if still FAIL, surface to user with the specific shortfall. |
| Coherence ✗ | Surface the issue; propose a fix; await user confirmation before applying |
| All PASS + all coherence ✓ | Proceed to Step 5 (export instructions) |

## Why the table is user-visible

Two reasons:
1. The user gets density evidence with the post — no need to recount specifics manually.
2. Forcing the model to publicly quantify forces real self-audit instead of vibes-checking.
