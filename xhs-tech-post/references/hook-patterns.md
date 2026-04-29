# Hook Patterns

The cover's job is to make a peer engineer want to swipe to card 02 — without using clickbait language that signals low-taste content. Four patterns are allowed; pick one based on the post's content shape.

## The 4 hooks

### A — 数字反差 (numeric before-after)

**Shape**: `<before number> → <after number>`

**When to use**: optimization posts, performance work, anything where the headline is a measured change.

**Examples from real material**:
- `75s → 24s` (TTFT optimization)
- `25K → 10K` (prompt token reduction)
- `5 GPU → 1 GPU` (resource reduction)

**Anti-example**: `slow → fast` (no number = not this hook). If you don't have a hard number, use a different hook.

**Subtitle pattern**: 1-line factual context — what was the workload, what was the constraint.
> "256K 上下文 · 单卡 KV 显存降至 1/cp_size"

**Accent token**: the arrow `→`.

---

### B — 过程式动作 ("我把 X 改成 Y")

**Shape**: `<count or label> → <count or label>`, but framed as a refactor / restructuring move

**When to use**: architecture refactors, design pattern changes, system redesigns where the headline is a structural shift.

**Examples**:
- `43 → 7` (43 tools refactored into 7 skills)
- `单点 → 三阶段` (monolithic to staged pipeline)
- `4 个服务 → 1 个 binary` (consolidation)

**Difference from A**: A is "the system got faster"; B is "I changed the structure". B's subtitle should mention the *kind* of change, not just the result.

**Subtitle pattern**:
> "把工具全量暴露重构成 Skill 渐进披露 / Prompt Token 直降 60%+"

**Accent token**: the arrow `→`.

---

### C — 技术名词 + 通俗动词 (concept-driven curiosity)

**Shape**: `<technical noun> <colloquial verb phrase>`

**When to use**: framework/concept deep-dives, mechanism explanations, "how does X work" posts.

**Examples**:
- `Zigzag 切分到底偷了哪一刀`
- `RadixAttention 凭什么能复用前缀 KV`
- `LangGraph 的状态持久化是不是一种逃避`

**Why it works**: peers who recognize the noun feel "this is in my domain"; the verb phrase signals the post will explain a mechanism, not just dump it. The verb should be slightly playful but not cute.

**Banned verb shapes**:
- "震惊！X 原来是 Y"
- "你不知道的 X"
- "99% 的人忽略的 X"
- Anything with "yyds / 神器 / 封神"

**Subtitle pattern**: a hint at the angle.
> "Ring Attention 负载均衡的小心机"

**Accent token**: the technical noun (Zigzag, RadixAttention, LangGraph).

---

### D — 我以为...结果 (cognitive update)

**Shape**: `以为 X (够了/收工/搞定)` followed by implied "结果不是" in subtitle.

**When to use**: war stories, debugging journeys, "things I learned the hard way" posts. The hook trades on self-deprecating honesty, which is a strong signal of authenticity.

**Examples**:
- `以为 GRPO 跑通就能收工`
- `以为 LangGraph 自带就行`
- `以为加 cache 是稳赚不亏`

**Subtitle pattern**: the consequence — usually a list of pitfalls.
> "Reward Hacking · KL 发散 · 长尾 OOM 三连"

**Accent token**: the technical noun in the cognitive object — `GRPO`, `LangGraph`, `cache`.

---

## Selection algorithm

Run the input through this decision tree:

1. **Is the post primarily about a measured improvement?** → A (数字反差)
2. **Is the post primarily about a structural/design change?** → B (过程式动作)
3. **Is the post explaining how a mechanism / framework works?** → C (技术名词)
4. **Is the post a war story about discovering pitfalls?** → D (我以为)

If two apply (e.g., a refactor that also produced numbers), pick the one matching the **emotional arc of the writing** — A and B are confident; C is curious; D is humble.

If none apply cleanly, the topic may be too thin for the format. Either ask the user to sharpen the angle or recommend a different content type.

## Anti-pattern banlist (for cover hooks specifically)

These never appear on covers in this skill, regardless of how well they "work" on mainstream Xiaohongshu:

- `震惊！...`
- `99% 的人 / 你不知道的 / 没人告诉你的`
- `永远不要用 X / 这就是 X 的真相`
- `绝绝子 / YYDS / 神器 / 封神 / 炸裂`
- `我宣布 / 求大数据把我推荐给 / 真的好用到哭`
- Multi-exclamation `!!!` or trailing `???`
- Aggression toward named tools / companies (`拳打 vLLM`, `xxx 早该淘汰`) — even as humor, this signals tribal posturing

### Cover failure modes (from real runs)

These are not banned phrases but banned visual+content patterns. If your draft cover matches one of these, redo:

| Failure | What it looks like | Fix |
|---|---|---|
| **Notion screenshot** | All-white bg, small kicker, 30px hero, 3-bar stack, corner outlined number | Switch to V2 Logo Block (dark bg + 80px wordmark) |
| **Buried anchor** | Hero "+1 → 三件套" at 56px — abstract enough that the small `+1` carries the meaning, lost at thumbnail | Switch to V1 Number Hero with the actual hard number (e.g. `27% / 10%`) |
| **Subtitle spoiler** | Subtitle gives the full answer in plain language, killing the swipe | Subtitle should be structural context only ("1M context · DeepSeek V3.2 → V4-Pro") |
| **Decoration-as-anchor** | The corner volume number or the 3-bar stack is the largest visual element | Add a real anchor (number / wordmark / schematic) — decoration can never be the anchor |

## Cover hero composition rules

Once a hook is chosen, compose the hero following these rules:

| Rule | Why |
|---|---|
| Hero is **at most 12 Chinese characters / 16 ASCII characters** | Otherwise font size has to drop below 60px and the cover loses thumbnail-readability |
| Number-type heroes (A, B-with-numbers): **80-96px** | Numbers are pre-attentive signals; this is the strongest anchor |
| Logo / wordmark heroes (B-without-numbers, C): **64-90px** | Brand mass needs to be visible at 200px feed thumbnail |
| Schematic-anchored covers: hero shrinks to **30-36px**, schematic carries the visual mass | When the schematic IS the anchor |
| Accent token in **first half** of the hero text | Reading order: eye lands on first 1-3 chars first |
| Hero must contain ≥ 1 specific anchor (number, named entity, technical noun) | "我做了一些优化" fails; "75s → 24s" succeeds |
| Subtitle must NOT resolve the curiosity | The subtitle gives structural context (workload, version, scale), not the answer |

## Anchor selection table (mapping hook → cover archetype)

For each chosen hook, pick the cover archetype that matches the post's evidence shape. These are the only valid combinations:

| Hook | Has hard number? | Recommended archetype | Hero shape |
|---|---|---|---|
| A (数字反差) | Yes (always) | **V1 Number Hero** | `<before> → <after>`, 80-96px |
| B (过程式) | Yes | **V1 Number Hero** | `<count> → <count>`, 80-96px (e.g. `43 → 7`) |
| B (过程式) | No (label-only) | **V2 Logo Block** | brand wordmark + structural verb in subtitle |
| C (技术名词) | — | **V2 Logo Block** OR **V3 Schematic Peek** | wordmark hero, OR mini diagram + smaller text |
| D (我以为) | — | **V2 Logo Block** | "以为 X" + brand wordmark of X |

V1 / V2 / V3 archetypes are defined in `references/card-templates.md`. A V2 cover MUST have either a dark/cream block bg or a logo block taking ≥ 30% of card height — otherwise it falls back to the failure mode of "small text on white".

## Thumbnail readability test (mandatory)

Every cover must pass this test before ship:

> Open the rendered HTML. Browser-zoom to 25% (or set the card to ~200px width). Squint. Can you see the anchor?

If the anchor is invisible or illegible at this scale, the cover has failed. Don't ship it. The two most common failures:

1. Hero text < 60px — looks like a blank card at thumbnail
2. White-bg + small accents + corner number — looks like a Notion screenshot
