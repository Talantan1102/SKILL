# Post Structure

How to compose 7–9 cards into a coherent post that reads in sequence. Order matters more than individual card quality — a great cover followed by 6 redundant cards is worse than a decent cover followed by 6 well-paced ones.

## The default sequence

For a 实战复盘 / 技术深度解读 post (the format this skill specializes in), use this sequence:

| Page | Type | Purpose |
|---|---|---|
| 01 | Cover | Hook |
| 02 | Concept card | Frame the thing being discussed (so non-experts can follow) |
| 03 | Compare card OR Setup card | Establish the "before" — what was the situation, why did it need work |
| 04 | Architecture / Flow card | Show the structural change |
| 05 | Concept card OR Code card | Drill into the key mechanism |
| 06 | Pitfall card | The honest "I assumed X but..." moment |
| 07 | Compare card OR Result card | The numbers or the after-state |
| 08 | Summary card | 3–5 takeaways |

This is 8 cards. Add a 09 if you have a second mechanism worth its own card. Drop 05 or 03 if your post is shorter / tighter.

## Variation: pure-optimization post (e.g., a kernel speedup)

| Page | Type | Why |
|---|---|---|
| 01 | Cover (Hook A) | Numeric hook |
| 02 | Concept | Frame the workload + what's being optimized |
| 03 | Architecture | Show the original vs. new structure |
| 04 | Code card | The key implementation detail |
| 05 | Pitfall card | A subtle gotcha hit during implementation |
| 06 | Compare card | Before-after benchmarks |
| 07 | Summary | When to apply / not apply |

7 cards. Skips the second concept/pitfall slot.

## Variation: pure war-story (debugging journey)

| Page | Type | Why |
|---|---|---|
| 01 | Cover (Hook D — 我以为) | Cognitive-update hook |
| 02 | Concept | Frame what's being debugged |
| 03 | Pitfall #1 | First wrong assumption |
| 04 | Pitfall #2 | Second wrong assumption |
| 05 | Pitfall #3 | Third (often the real root cause) |
| 06 | Concept / Code | The actual fix |
| 07 | Summary | "Things I should have checked first" |

7 cards. The pitfall cards are the soul of this format — concentrating them gives the post a clear emotional arc (denial → bargaining → acceptance, in a sense).

## Variation: framework / mechanism explainer

| Page | Type | Why |
|---|---|---|
| 01 | Cover (Hook C — 技术名词) | Curiosity hook |
| 02 | Concept | What problem this mechanism solves |
| 03 | Architecture | High-level structure |
| 04 | Flow card | How a request / call flows through |
| 05 | Concept | Drill into the key trick |
| 06 | Compare card | This vs. alternative approaches |
| 07 | Summary | When to use this |

7 cards. No pitfall — explainers don't need a war-story arc.

## Sequencing rules

These rules apply across all variations:

### 1. Cover hook implies first content card type

The hook chosen on the cover constrains card 02:

- Cover hook A (数字反差) → Card 02 should be a **concept card** that frames *what was being measured* (so the headline number lands)
- Cover hook B (过程式) → Card 02 should be a **concept card** that frames *what was being restructured*
- Cover hook C (技术名词) → Card 02 should be a **concept card** that defines the noun
- Cover hook D (我以为) → Card 02 should frame *what was being attempted* — could be a setup-style concept card

### 2. Information progresses from general → specific → again-general

The post should narrow from broad framing (cards 02–04) into specific mechanism / pitfalls (cards 05–07) and broaden back to takeaways (08–09). Avoid the inverted shape (specific → broad → specific) — readers find it disorienting.

### 3. Each card should answer a question the previous card raised

Read your draft sequence in order and silently ask "OK, but what about Z?" after each card. The next card should answer that. If it doesn't, your sequence is wrong.

### 4. The summary card is non-negotiable

Even if every other card is great, missing a summary card costs you ~30% of saves/screenshots. The summary is what readers come back to.

### 5. Pitfall cards are sticky

Posts with at least one pitfall card outperform posts without — even on optimization topics that "shouldn't" need them. Always look for an honest pitfall to include.

## Post-level coherence checks

Before finalizing, verify:

- **One narrative arc**: can you write the post in one sentence? "I refactored 43 tools into 7 skills, and here's the trick that made it actually work." If the one-sentence form has multiple "and"s, the post has multiple stories — split it or cut content.
- **Consistent kicker**: every card has the same kicker text (e.g., `agent harness · note 02`), only the page number changes.
- **No card is skippable**: if removing a card doesn't damage the narrative, remove it. Better 7 strong cards than 9 with filler.
- **Cover and summary echo**: the summary's first takeaway should restate the cover's promise. Closing the loop signals "this post delivered what it promised."

## Word count and read time targets

- Cover: ~30 words total (kicker + hero + subtitle + footer)
- Concept card: ~80–120 words (title + gist + body + stats labels)
- Architecture card: ~60–90 words (denser visual; less prose)
- Flow card: ~70–100 words
- Compare card: ~50–80 words (visual-heavy)
- Code card: ~30–60 words of prose + the snippet itself
- Pitfall card: ~80–120 words (this is where stories happen)
- Summary card: ~60–90 words (5 short takeaways)

Total post word count: roughly 500–800 words. At 300 chars/min reading + 0.33 min/card image-look, this works out to 4–7 minutes — which matches the read-time stamp on the cover.

## Post body (正文 below the images)

The post body sits below all the cards in Xiaohongshu's compose box. It is **not** another card — it's plain text. Length 80–150 characters.

### Body template

```
{One-sentence restatement of the core insight in plain words}.
{One sentence of context the cards couldn't fit — e.g., "这套方案在 30B MoE 上跑得稳，70B dense 还在验证"}.
{Optional invitation: "卡 N 那块的实现还在迭代，做过类似的同行欢迎评论区交流"}

{3-5 hashtags, ordered specific → broad}
```

### Body anti-patterns

- Don't restate every card. The cards are right above the text. Repetition is annoying.
- Don't end with "求三连 / 关注我" — readers know how to follow if they want to.
- Don't add "图源自制" or "首发小红书" type meta-disclaimers — they read as defensive.
- Don't use emoji in the body. The visual-language consistency matters even in the text block.

## Hashtag selection

Pick 3–5 hashtags. Order from specific to broad:

```
{Specific tool/concept tag} {Specific area tag} {Mid-level tag} {Broad role tag} [{Broad role tag 2}]
```

Examples:
- `#SGLang #ContextParallel #LLM推理 #大模型 #AI工程师`
- `#GRPO #RLHF #对齐训练 #大模型 #算法工程师`
- `#LangGraph #MultiAgent #Agent工程 #AI工程师`

Don't pad with unrelated trending tags like `#职场 #成长` unless the post is genuinely about those topics. The Xiaohongshu algorithm rewards relevance over reach, especially for technical content.
