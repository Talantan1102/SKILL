# Brief Gate + Pre-flight QA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two process-layer gates to the existing v1 `xhs-tech-post` skill — a Brief Gate that refuses fabricated specifics at input, and a Pre-flight QA self-audit that catches density-floor violations before delivery.

**Architecture:** Two new reference files (`brief-gate.md`, `qa-checklist.md`) hold the gate definitions; `SKILL.md` Process is updated to consult them. No visual / template changes. No HTML changes. No new tests in code — validation is end-to-end skill invocations against the 5 spec scenarios.

**Tech Stack:** Markdown only. The skill folder is **NOT a git repo** — replace any `git commit` step with file save + manual review. If the user later imports the folder into a git workflow, normal commits resume.

**Source spec:** `docs/spec/2026-04-29-brief-gate-and-qa-design.md`

---

## File Structure

| Path | Action | Responsibility |
|---|---|---|
| `references/brief-gate.md` | CREATE | 6-field schema, anchor-type taxonomy, refusal protocol, override flow, per-input-type question scripts |
| `references/qa-checklist.md` | CREATE | Per-card metric definitions, post-level coherence checks, QA table format, FAIL trigger protocol |
| `SKILL.md` | MODIFY (3 edits) | Inputs section wording fix; Step 1 replaced with Brief Gate pointer; Step 4.5 inserted before Step 5 |
| `references/visual-system.md` | UNCHANGED | — |
| `references/hook-patterns.md` | UNCHANGED | — |
| `references/card-templates.md` | UNCHANGED | — |
| `references/post-structure.md` | UNCHANGED | — |
| `assets/*` | UNCHANGED | — |

---

## Task 1: Create `references/brief-gate.md`

**Files:**
- Create: `references/brief-gate.md`

- [ ] **Step 1: Write the file**

Create `references/brief-gate.md` with this exact content:

````markdown
# Brief Gate

Mandatory schema and refusal protocol that gates entry into post generation. The model MUST emit a complete brief block before producing any HTML.

## Schema

```yaml
brief:
  topic: "<one-line, what the post is about>"
  key_insight: "<one-line, the non-obvious idea that ties the post together>"
  evidence:                          # REQUIRED, ≥ 1 concrete anchor (four types below)
    - "<number / before-after / named mechanism·tool·file·API / concrete scenario>"
    - "..."
  trade_off: "<one line, what this cost — REQUIRED, never '无'>"
  audience_anchor: "<familiar concept the reader already knows>"
  chosen_hook: <A | B | C | D>
```

## `evidence` — concrete anchor types

PASS criterion: the brief contains **≥ 1 concrete anchor** of any of the four types below.

| Type | Examples |
|---|---|
| (a) Hard number | `75s → 24s`, `p95 120ms`, `60% token 降幅` |
| (b) Before-after / comparison | `43 → 7`, `Zigzag vs Ring Attention` |
| (c) Named mechanism / tool / file / API | `RadixAttention prefix sharing`, `tokenizer.json offset 字段`, `SGLang 的 PCP 实现` |
| (d) Concrete scenario | `"喜欢 Python" 埋在 100 条 "thanks" 里`, `5 个 GPU 节点 RDMA 配置` |

The bar matches the card-level `specifics` definition: a specific, named, non-fabricable thing. Hooks A/B usually hit (a)(b); Hooks C/D usually hit (c)(d).

## Refusal protocol

When `evidence` is missing OR every entry is a vague claim with no number, no named mechanism, no concrete scenario, the model MUST stop and reply (verbatim, in the user's language):

> 需要至少一个具体锚点才能写——一个数字 / 一个前后对比 / 一个命名机制或工具 / 一个具体场景,任何一项都行。如果题目空到连这一条都给不出,先把题目收窄,这个 skill 故意不允许虚构。

When `trade_off` is missing OR filled with "无" / "无明显代价" / vague hedges, the model MUST stop and reply (verbatim):

> 这个改动一定有代价(哪怕轻微)。是慢了一点 / 多耗显存 / 新人读不懂?写出来才往下走。

### evidence override

The user can bypass the evidence refusal only by typing an explicit phrase like "我先这么写,锚点之后补". When this happens:

- The model records `evidence_overridden: true` in the brief block
- The post is downgraded to **draft** mode: post body MUST start with `[draft · 锚点待补]`
- The QA report MUST flag every card whose claims rest on the missing anchor
- The user is responsible for filling anchors in before publishing

There is no override for `trade_off` — if a user genuinely cannot articulate a trade-off, the topic is not yet ready for this format.

## Per-input-type question scripts

| Input | Order of operations |
|---|---|
| Topic string | Ask for all 6 fields in 2–3 messages. Group: (topic + key_insight), (evidence + trade_off), (audience_anchor + chosen_hook) |
| Repo URL / path | (1) Read README + key directories. Auto-fill `topic`, `key_insight`, `audience_anchor`, and propose specific named modules / files / APIs as `evidence` candidates. (2) Ask: "benchmark 跑得出哪个数?或者你想 highlight 哪个具体机制?" to confirm or augment evidence. (3) Ask `trade_off`. (4) Recommend `chosen_hook` based on content shape. |
| Paper PDF / arXiv | (1) Extract abstract, headline number(s) or named method(s), 1 figure → auto-fill `topic`, `key_insight`, `evidence`. (2) Ask `audience_anchor` and `chosen_hook`. (3) Ask `trade_off` (papers rarely state honest trade-offs). |
| Blog URL | (1) `web_fetch` → auto-fill `topic`. (2) Ask "你看完想 highlight 哪 1 句作为 key_insight". (3) Continue as topic-string flow. |

## Gate boundary

A complete brief — emitted as a YAML block, all required fields filled, override flag explicit if used — is the only path into Step 2 (card sequence planning). Without it, the model does not produce HTML.
````

- [ ] **Step 2: Verify content**

Open the file and check:
- All 4 anchor types are listed in the table
- The exact verbatim refusal-protocol Chinese text appears
- The override phrase ("我先这么写,锚点之后补") appears
- The 4 input-type question scripts are present

- [ ] **Step 3: Save**

Skill folder is not a git repo. No commit. The file existing on disk is sufficient.

---

## Task 2: Create `references/qa-checklist.md`

**Files:**
- Create: `references/qa-checklist.md`

- [ ] **Step 1: Write the file**

Create `references/qa-checklist.md` with this exact content:

````markdown
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

## Post-level coherence checks

Source rules: `post-structure.md`.

- [ ] Kicker text is identical across all cards (only the page number changes)
- [ ] Cover and Summary's first-takeaway echo each other
- [ ] One-sentence narrative arc has zero "and"s / "和" / "而且"
- [ ] No card is removable without damaging the narrative
- [ ] At least one pitfall card present (or explicit justification why not)

## QA table format (user-visible output)

The model emits this Markdown block at the end of Step 4:

```markdown
## Pre-flight QA

| 卡 | 字符数 | specifics | 手绘元素 | trade-off | 状态 |
|---|---|---|---|---|---|
| 02 concept | 248 | 7 | 4 (squiggle, star, ×, tilt) | ✓ | PASS |
| 03 architecture | 195 | 4 | 3 | — | **FAIL** (<220 字 / specifics<6) |
| 04 pitfall | 281 | 9 | 3 | ✓ | PASS |
| ...

### 一致性
- [✓] kicker 一致 ("agent harness · note 02")
- [✓] cover ↔ summary 首条呼应
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
````

- [ ] **Step 2: Verify content**

Open the file and check:
- All 5 metric rows present
- `trade_off_present` shows the three-clause OR pass condition
- The trigger protocol shows the 2-attempt regen cap
- All 5 post-level coherence bullets present

- [ ] **Step 3: Save**

No git commit (folder is not a git repo).

---

## Task 3: SKILL.md edit A — fix Inputs-section wording

**Files:**
- Modify: `SKILL.md` line 26 (the topic-string input description under `## Inputs the skill accepts`)

- [ ] **Step 1: Apply the edit**

Use the Edit tool with these exact strings:

`old_string`:
```
   → Skill should ask 2–3 quick clarifying questions about specifics (numbers, the key insight, trade-off) before generating.
```

`new_string`:
```
   → Skill should ask 2–3 quick clarifying questions about specifics (a concrete anchor, the key insight, trade-off) before generating.
```

- [ ] **Step 2: Verify**

Read SKILL.md lines 25-27. Confirm the new wording is in place and no other text changed.

---

## Task 4: SKILL.md edit B — replace Step 1 with Brief Gate pointer

**Files:**
- Modify: `SKILL.md` lines 55-68 (Step 1 entire block, from `### Step 1 — Build the post brief` through `Don't fabricate.`)

- [ ] **Step 1: Apply the edit**

Use the Edit tool with these exact strings:

`old_string`:
```
### Step 1 — Build the post brief

Before writing any HTML, extract or elicit these 6 fields from the input:

| Field | What goes here |
|---|---|
| `topic` | One-line: "把 43 个 tool 重构成 7 个 Skill 渐进披露" |
| `key_insight` | One-line: the non-obvious idea that ties the post together |
| `evidence` | Hard numbers / before-after / named comparisons. **Required.** A post without at least one specific number is rejected. |
| `trade_off` | What did this cost? **Required**, even if mild. Honesty is a credibility multiplier with this audience. |
| `audience_anchor` | What familiar concept does the reader already know that this builds on? Used to make abstractions land. |
| `chosen_hook` | Pick one of the 4 cover hooks (A/B/C/D) — see `references/hook-patterns.md` for selection rules. |

If the user provides a topic without numbers or trade-offs, **ask for them** before proceeding. Don't fabricate.
```

`new_string`:
```
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
```

- [ ] **Step 2: Verify**

Read SKILL.md around lines 55-70. Confirm:
- New header is `### Step 1 — Build the post brief (Brief Gate)`
- The `evidence` row mentions "concrete anchor" not "specific number"
- The closing paragraph references `brief-gate.md` and the override mechanism

---

## Task 5: SKILL.md edit C — insert Step 4.5 before Step 5

**Files:**
- Modify: `SKILL.md` — insert new section between the end of Step 4 (line 103) and the `### Step 5` header (line 105)

- [ ] **Step 1: Apply the edit**

Use the Edit tool with these exact strings:

`old_string`:
```
Hashtags: 3–5, ordered specific → broad. Example: `#SGLang #ContextParallel #LLM推理 #大模型 #AI工程师`. Don't pad with irrelevant trending tags.

### Step 5 — Output and instructions for export
```

`new_string`:
```
Hashtags: 3–5, ordered specific → broad. Example: `#SGLang #ContextParallel #LLM推理 #大模型 #AI工程师`. Don't pad with irrelevant trending tags.

### Step 4.5 — Pre-flight QA

Consult `references/qa-checklist.md`. After all cards + post body + hashtags are drafted, emit the QA table for the user. Auto-regenerate any FAILing card (only that card, capped at 2 attempts); surface coherence ✗ items to the user. Only proceed to Step 5 when all cards PASS and all coherence checks are ✓ (or explicitly accepted by the user).

### Step 5 — Output and instructions for export
```

- [ ] **Step 2: Verify**

Read SKILL.md around the Step 4 → Step 5 boundary. Confirm:
- A new `### Step 4.5 — Pre-flight QA` section sits between Step 4 and Step 5
- It references `references/qa-checklist.md`
- It mentions the 2-attempt regen cap
- The `### Step 5` header is still present and unchanged

---

## Task 6: End-to-end validation (5 scenarios)

**Files:** None modified. This task verifies the integrated behavior by running the skill against 5 inputs from the spec test plan.

For each scenario, invoke the skill in a fresh chat (or fresh skill invocation) with the input listed below, and check the output against the expected behavior. Mark each step `- [x]` only when the expected behavior is observed.

- [ ] **Step 1: Empty topic refusal**

Input: `想写一篇关于 LLM 的贴`

Expected: model MUST emit the verbatim refusal sentence from `brief-gate.md`:

> 需要至少一个具体锚点才能写——一个数字 / 一个前后对比 / 一个命名机制或工具 / 一个具体场景,任何一项都行。如果题目空到连这一条都给不出,先把题目收窄,这个 skill 故意不允许虚构。

The model must NOT generate any HTML or attempt to fill `evidence` itself.

- [ ] **Step 2: Pure-concept topic passes**

Input: `聊聊 RadixAttention 的 prefix sharing 机制`

Expected: model auto-fills `evidence` with anchor type (c) — e.g. `["RadixAttention prefix sharing 机制", "vanilla KV cache 复用差异"]` — and proceeds to ask for `trade_off`. No refusal triggered. The brief block YAML must be visible in the model's response.

- [ ] **Step 3: Repo URL flow**

Input: `把 sgl-project/sglang 里的 PCP 实现做成一篇贴` (or any concrete repo path the user has access to)

Expected: model reads README + key directories first, auto-fills `topic` / `key_insight` / `audience_anchor` / candidate `evidence`, then asks specifically about `trade_off`. The brief block YAML must be emitted before any HTML.

- [ ] **Step 4: End-to-end with QA table**

Input: A complete brief (manually compose one with all 6 fields). Allow the model to generate all cards + body + hashtags.

Expected at end of Step 4: the model emits a `## Pre-flight QA` Markdown block matching the format in `qa-checklist.md`. Every card row has values for all 5 metric columns. The "一致性" subsection has 5 boxes (some ✓, some ✗ if applicable). Only after all PASS does the Step 5 export instruction appear.

To stress-test FAIL handling: edit the model's draft of one card to be sparse (≤ 200 chars, ≤ 4 specifics). Re-run QA. Expected: that card shows **FAIL**, the model auto-regenerates only that card with a stated fix, then re-emits the QA table showing PASS for that row.

- [ ] **Step 5: evidence_overridden draft mode**

Input: A vague topic. When refusal protocol triggers, reply with `我先这么写,锚点之后补`.

Expected:
- Model sets `evidence_overridden: true` in the brief block
- Final post body starts with `[draft · 锚点待补]`
- QA report flags every card whose claims would rest on the missing anchor (typically the architecture / pitfall / result cards)
- No regen attempts for the flagged cards on density grounds alone (since draft mode is by definition under-specified)

- [ ] **Step 6: Record findings**

Open `docs/spec/2026-04-29-brief-gate-and-qa-design.md` and add (at the bottom, in a new `## Validation log` section):
- Date of validation
- Which scenarios PASSed and which needed clarification
- Any new edge cases discovered

This is the test record. No code coverage tool exists for skills — this manual log is the substitute.

---

## Self-review notes

Spec coverage check:

| Spec section | Covered by task |
|---|---|
| Component 1 (brief-gate.md content) | Task 1 |
| Component 2 (qa-checklist.md content) | Task 2 |
| Component 3 — Step 1 replace | Task 4 |
| Component 3 — Step 4.5 insert | Task 5 |
| Component 3 — fix old SKILL.md inconsistency (Inputs section) | Task 3 |
| Component 3 — fix old SKILL.md inconsistency (Step 1 evidence row + closing paragraph) | Task 4 (folded — Step 1 is replaced wholesale, both lines in the diff) |
| Test plan #1 (empty topic refusal) | Task 6, Step 1 |
| Test plan #2 (pure-concept passes) | Task 6, Step 2 |
| Test plan #3 (repo URL flow) | Task 6, Step 3 |
| Test plan #4 (end-to-end QA) | Task 6, Step 4 |
| Test plan #5 (evidence_overridden draft mode) | Task 6, Step 5 |

No placeholders. All file contents are inlined verbatim. All edit `old_string` / `new_string` pairs are exact. No "TODO", "TBD", or "implement later" anywhere.

Type / path consistency: brief-gate.md and qa-checklist.md are both under `references/`, matching SKILL.md's existing reference convention. The override phrase, refusal sentences, and field names are identical across all three files where they appear.
