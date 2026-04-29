# Spec:Brief Gate + Pre-flight QA(xhs-tech-post v1.1)

日期:2026-04-29
状态:用户已在对话中确认设计,待进入实施
范围:对现有 v1 skill 做**流程层**加固,不动视觉/模板层。

## 问题

v1 skill 在 brief 充足时产出质量很高,但 brief 较薄时会出现两类静默失败:

1. **specifics 编造** — 用户没给具体锚点(数字 / 命名机制 / 具体场景)或代价时,model 观察到会自己"补"一个,而不是停下来追问。这直接破坏整个视觉 + 文案系统赖以建立的"同侪可信度"。
2. **卡片密度不达标** — 现有密度底线(≥ 6 specifics、220–300 字、每条 bullet ≥ 1 specific)在 `SKILL.md` 里以散文形式存在,但 model 没有强制自检环节。卡片有时以 180 字 / 4 specifics 的状态被交付,用户毫无察觉。

两类失败都是静默的:用户往往要等到把贴子粘进小红书、再读一遍时才发现问题。

## 目标

加两个流程层 gate:

- **④ Brief Gate** — 把 Step 1 从"问 2-3 个问题"形式化为 6 字段 schema,带拒绝协议(缺 `evidence` 或 `trade_off` 时不允许往下走)。
- **③ Pre-flight QA** — 在 Step 4 与 Step 5 之间插入 Step 4.5,model 在交付 HTML 前必须 emit 一个逐卡自审表(字符数、specifics、手绘元素、trade-off 是否存在)。任何 FAIL 自动重生 + 复检。

## 非目标(本次推迟)

- 锁定 `flow` 与 `code` 两类卡片模板(v1 仍是 principle-only)。
- 自动化截图导出。
- 重构现有卡片模板 / 视觉语言。
- 修 `var(--font-serif)` 与字面字体栈不一致问题。

## 文件改动

| 路径 | 改动 |
|---|---|
| `references/brief-gate.md` | **新增** — 6 字段 schema、拒绝协议、按输入类型的提问脚本 |
| `references/qa-checklist.md` | **新增** — 逐卡指标、post-level 一致性检查、QA 表格式、触发协议 |
| `SKILL.md` | **改** — 重写 Step 1(改为引用 brief-gate.md);Step 4 与 Step 5 之间新增 Step 4.5(引用 qa-checklist.md) |
| `visual-system.md` | 不动 |
| `hook-patterns.md` | 不动 |
| `card-templates.md` | 不动 |
| `post-structure.md` | 不动 |
| `assets/*` | 不动 |

## 组件 1 — `references/brief-gate.md`

### Schema

Model 在产出任何 HTML 之前先 emit 这个 YAML block(用户可见,不是内部记账)。

```yaml
brief:
  topic: "<一行 — 这篇贴在讲什么>"
  key_insight: "<一行 — 串联整篇的非显然观点>"
  evidence:                  # 必填,≥ 1 个 concrete anchor(四选一,见下)
    - "<数字 / 前后对比 / 命名机制·工具·文件·API / 具体场景>"
    - "..."
  trade_off: "<一行 — 这事的代价是什么。必填,禁止填'无'>"
  audience_anchor: "<读者已经熟悉、可作为锚点的概念>"
  chosen_hook: <A | B | C | D>
```

`evidence` 字段的 PASS 标准:**≥ 1 个 concrete anchor**,四选一即可——

| 类型 | 例子 |
|---|---|
| (a) 硬数字 | `75s → 24s`、`p95 120ms`、`60% token 降幅` |
| (b) 前后/对比 | `43 → 7`、`Zigzag vs Ring Attention` |
| (c) 命名机制/工具/文件/API | `RadixAttention prefix sharing`、`tokenizer.json offset 字段`、`SGLang 的 PCP 实现` |
| (d) 具体场景 | `"喜欢 Python" 埋在 100 条 "thanks" 里`、`5 个 GPU 节点 RDMA 配置` |

定义和 card 层 `specifics` 完全一致——这就是这个 skill 的最低可信度门槛:你能不能讲出至少一个**具体的、有名字的、不可虚构的**东西。Hook A/B 通常天然命中 (a)(b);Hook C/D 多走 (c)(d)。

### 拒绝协议

当 `evidence` 缺失,或填的内容都是空泛 claim(没有任何具名机制、数字、场景),model **必须**停下,逐字回复(用用户的语言):

> 需要至少一个具体锚点才能写——一个数字 / 一个前后对比 / 一个命名机制或工具 / 一个具体场景,任何一项都行。如果题目空到连这一条都给不出,先把题目收窄,这个 skill 故意不允许虚构。

当 `trade_off` 缺失或被填成 "无" / "无明显代价" / 模糊托词,model **必须**停下,逐字回复:

> 这个改动一定有代价(哪怕轻微)。是慢了一点 / 多耗显存 / 新人读不懂?写出来才往下走。

用户只能用类似"我先这么写,锚点之后补"的明确表态来跳过 evidence 检查。绕开后:
- model 在 brief block 里记 `evidence_overridden: true`
- 整篇贴子被降级为 **draft** 模式:正文必须以 `[draft · 锚点待补]` 开头
- QA 报告必须高亮"哪些卡的论点缺乏锚点支撑"
- 用户在发布前自己负责把锚点补上

### 按输入类型的提问脚本

| 输入类型 | 操作顺序 |
|---|---|
| 主题字符串 | 用 2-3 条消息把 6 字段问完(分组:topic+insight、evidence+trade_off、anchor+hook) |
| Repo URL/路径 | (1) 读 README + 主要目录,自填 `topic` / `key_insight` / `audience_anchor`,并把仓库里出现的具名模块/文件/API 当作 `evidence` 候选。(2) 问用户:"benchmark 跑得出哪个数?或者你想 highlight 哪个具体机制?" 让用户确认或补充 evidence。(3) 问 `trade_off`。(4) 根据内容推荐 `chosen_hook`。 |
| Paper PDF / arXiv | (1) 抽 abstract、headline 数字 / 命名方法、1 张 figure → 自填 `topic` / `key_insight` / `evidence`。(2) 问 `audience_anchor` 和 `chosen_hook`。(3) 问 `trade_off`(论文很少诚实写代价)。 |
| Blog URL | (1) `web_fetch` → 自填 `topic`。(2) 问"你看完想 highlight 哪 1 句作为 key_insight"。(3) 后续走主题字符串流程。 |

## 组件 2 — `references/qa-checklist.md`

### 逐卡指标(model 对每张卡计算)

| 指标 | 算法 | PASS 阈值 |
|---|---|---|
| char_count | 卡正文的中文字符等量计数,排除 kicker / 页码 / 标题 / gist / trade-off 行 | 220 ≤ x ≤ 300 |
| specifics | 计数:数字、命名工具/库/文件/API、括号内具体场景、前后对比 | ≥ 6 |
| hand_drawn_elements | 卡内使用的、来自 visual-system.md 词汇表的元素数 | 3 ≤ x ≤ 5 |
| trade_off_present | 这张卡是否带 trade-off 行 | PASS 当 (a) trade-off 行存在,**或** (b) 卡类型是 `summary`,**或** (c) model 显式给出 `trade_off_skipped_reason`(≤ 16 字,例:"纯解释卡 / 无实际代价") |
| bullet_specifics_floor | 每条 bullet ≥ 1 specific;concept 卡 bullet ≥ 2 | true |

一张卡所有指标都 PASS 才算 PASS。

### Post-level 一致性检查

(规则源头见 `post-structure.md`。)

- 所有卡的 kicker 文字一致(只换页码)
- Cover 与 Summary 首条彼此呼应
- One-sentence narrative arc 中没有"和 / 而且"
- 任何卡删掉都会破坏叙事(否则该删)
- 至少有 1 张 pitfall 卡(否则需显式说明为什么没有)

### QA 表格式

Model 在 Step 4 末尾、Step 5 之前 emit 这块 Markdown:

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
- [✓] one-sentence arc: "<那一句>"
- [✗] 卡 05 是否多余? → 建议合并入卡 04

### Action
卡 03 不达标。改动:在"召回"模块加 2 个 specifics(FTS5 top-k=20、p95 120ms),字符推到 240,specifics 到 7。重生成中。
```

### 触发协议

| 情形 | Model 行为 |
|---|---|
| 任一卡 FAIL | **只重生这一张**(其他不动),按命中的指标定向修复;重生后再跑 QA;不能把 FAIL 版本给用户。同卡重试上限 2 次,超出后显式上报用户具体差距。 |
| 一致性 ✗ | 点出问题、给出修法,等用户确认再改 |
| 全 PASS | 进 Step 5(导出指引) |

QA 表是**用户可见的**——这是它的核心价值。用户拿到稿子的同时也拿到了"密度证据",不用回头自己数字数。

## 组件 3 — `SKILL.md` 改动

### Step 1(整段替换)

```
### Step 1 — 收集 post brief(Brief Gate)

参考 `references/brief-gate.md`。在产出任何 HTML 之前,emit 一个填齐的
brief YAML block。如果 `evidence` 或 `trade_off` 缺失,按拒绝协议执行——
不许自己编。

只有 brief 完整(或被用户明确 override)后才能进 Step 2。
```

### Step 4.5(新增,介于 Step 4 和 Step 5 之间)

```
### Step 4.5 — Pre-flight QA

参考 `references/qa-checklist.md`。当所有卡 + 正文 + 话题都生成完后,
emit QA 表。任一 FAIL 卡自动重生;一致性 ✗ 项点给用户。全 PASS 才进 Step 5。
```

### 顺手修正 SKILL.md 里旧的不一致表述

SKILL.md 现有 evidence 字段定义里写的是 "Hard numbers / before-after / named comparisons. **Required.**",紧跟一句 "A post without at least one specific number is rejected"——前后矛盾。改成统一表述:

> Hard numbers / before-after / named mechanism or tool / concrete scenario. **Required.** A post without at least one concrete anchor is rejected.

同时 `## Inputs the skill accepts` 那段里"ask 2–3 quick clarifying questions about specifics (numbers, the key insight, trade-off)"也改成"about a concrete anchor, the key insight, trade-off",和上面一致。

## 测试计划

实施完成后,验证以下场景:

1. 用一个空泛主题(例如"想写一篇关于 LLM 的贴")→ 必须按 evidence 拒绝协议停下。
2. 用一个**纯概念解读**主题(例如"聊聊 RadixAttention 的 prefix sharing 机制")→ 必须 PASS evidence(命名机制 = anchor 类型 c),正常进入下一步。
3. 用一个带 benchmark 的 repo URL 跑 → 必须自动填 `evidence`,主动问 `trade_off`。
4. 完整 brief 跑端到端 → 必须 emit QA 表;手动把某张卡改稀,验证 model 自动重生那一张。
5. 走 `evidence_overridden: true` 流程 → 正文必须以 `[draft · 锚点待补]` 开头,QA 报告高亮受影响卡。

## 迁移

完全是加法。已经在用 v1 的流程不会断——Step 1 散文只是变得更严格,Step 4.5 是新增的输出面。现有 card / asset / 模板不需要改。

## 待解问题(不阻塞)

- `SKILL.md` 与 example HTML 之间 `var(--font-serif)` 的不一致先留着,留给单独一次文档清理。
- 是否要加第 5 个 `chosen_hook` 取值(`mixed`,用于真正混合 hook A + B 的贴子)。等有真实需求再说。
