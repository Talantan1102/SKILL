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
