# 简报关卡 + 发布前自检 实施计划

> **致 agentic 执行者:** 必需子 skill:使用 superpowers:subagent-driven-development(推荐)或 superpowers:executing-plans 按任务逐步实施本计划。各步骤使用 checkbox(`- [ ]`)语法做进度追踪。

**目标:** 给现有 v1 `xhs-tech-post` skill 加两个流程层关卡 —— 一个简报关卡,在输入端拒绝编造的具体细节;一个发布前自检,在交付前抓住密度下限违规。

**架构:** 两个新参考文件(`brief-gate.md`、`qa-checklist.md`)承载关卡定义;`SKILL.md` 流程更新为引用它们。视觉 / 模板不变。HTML 不变。代码层不新增测试 —— 验证方式是按规格中 5 个场景做端到端 skill 调用。

**技术栈:** 仅 Markdown。该 skill 文件夹**不是 git repo** —— 把所有 `git commit` 步骤替换为文件保存 + 人工复核。如果用户后续把该文件夹纳入 git 流程,正常 commit 即可恢复。

**源规格:** `docs/spec/2026-04-29-brief-gate-and-qa-design.md`

---

## 文件结构

| 路径 | 操作 | 职责 |
|---|---|---|
| `references/brief-gate.md` | 新建 | 6 字段 schema、anchor 类型分类、拒绝协议、override 流程、按输入类型的提问脚本 |
| `references/qa-checklist.md` | 新建 | 逐卡指标定义、post-level 一致性检查、QA 表格式、FAIL 触发协议 |
| `SKILL.md` | 修改(3 处编辑) | Inputs 段落措辞修正;Step 1 替换为简报关卡的指针;Step 5 之前插入 Step 4.5 |
| `references/visual-system.md` | 不变 | — |
| `references/hook-patterns.md` | 不变 | — |
| `references/card-templates.md` | 不变 | — |
| `references/post-structure.md` | 不变 | — |
| `assets/*` | 不变 | — |

---

## 任务 1:创建 `references/brief-gate.md`

**文件:**
- 新建:`references/brief-gate.md`

- [ ] **步骤 1:写入文件**

按以下完整内容创建 `references/brief-gate.md`:

````markdown
# Brief Gate

强制 schema 与拒绝协议,作为进入贴子生成的关卡。Model 必须在产出任何 HTML 之前 emit 一个完整的 brief block。

## Schema

```yaml
brief:
  topic: "<一行,这篇贴在讲什么>"
  key_insight: "<一行,串联整篇的非显然观点>"
  evidence:                          # 必填,≥ 1 个 concrete anchor(下方四种类型)
    - "<数字 / 前后对比 / 命名机制·工具·文件·API / 具体场景>"
    - "..."
  trade_off: "<一行,这事的代价是什么 —— 必填,禁止填 '无'>"
  audience_anchor: "<读者已经熟悉、可作为锚点的概念>"
  chosen_hook: <A | B | C | D>
```

## `evidence` —— concrete anchor 类型

PASS 标准:brief 包含**≥ 1 个 concrete anchor**,以下四种类型任一即可。

| 类型 | 例子 |
|---|---|
| (a) 硬数字 | `75s → 24s`、`p95 120ms`、`60% token 降幅` |
| (b) 前后/对比 | `43 → 7`、`Zigzag vs Ring Attention` |
| (c) 命名机制/工具/文件/API | `RadixAttention prefix sharing`、`tokenizer.json offset 字段`、`SGLang 的 PCP 实现` |
| (d) 具体场景 | `"喜欢 Python" 埋在 100 条 "thanks" 里`、`5 个 GPU 节点 RDMA 配置` |

门槛与 card 层 `specifics` 定义一致:具体的、有名字的、不可虚构的东西。Hook A/B 通常命中 (a)(b);Hook C/D 通常命中 (c)(d)。

## 拒绝协议

当 `evidence` 缺失,或每一项都是空泛 claim(没有任何数字、命名机制、具体场景),model 必须停下,逐字回复(用用户的语言):

> 需要至少一个具体锚点才能写——一个数字 / 一个前后对比 / 一个命名机制或工具 / 一个具体场景,任何一项都行。如果题目空到连这一条都给不出,先把题目收窄,这个 skill 故意不允许虚构。

当 `trade_off` 缺失,或填成 "无" / "无明显代价" / 模糊托词,model 必须停下,逐字回复:

> 这个改动一定有代价(哪怕轻微)。是慢了一点 / 多耗显存 / 新人读不懂?写出来才往下走。

### evidence override

用户只能用一句明确表态(如 "我先这么写,锚点之后补")来绕过 evidence 拒绝。一旦发生:

- Model 在 brief block 中记录 `evidence_overridden: true`
- 整篇贴子降级为 **draft** 模式:正文必须以 `[draft · 锚点待补]` 开头
- QA 报告必须标记每一张论点依赖缺失锚点的卡
- 用户在发布前自行补齐锚点

`trade_off` 没有 override —— 如果用户真的讲不出 trade-off,这个题目就还没准备好用这个格式写。

## 按输入类型的提问脚本

| 输入 | 操作顺序 |
|---|---|
| 主题字符串 | 在 2–3 条消息中问完 6 字段。分组:(topic + key_insight)、(evidence + trade_off)、(audience_anchor + chosen_hook) |
| Repo URL / 路径 | (1) 读 README + 主要目录。自填 `topic`、`key_insight`、`audience_anchor`,并把具名模块 / 文件 / API 作为 `evidence` 候选项。(2) 问:"benchmark 跑得出哪个数?或者你想 highlight 哪个具体机制?" 用于确认或补强 evidence。(3) 问 `trade_off`。(4) 根据内容形态推荐 `chosen_hook`。 |
| Paper PDF / arXiv | (1) 抽 abstract、headline 数字或命名方法、1 张 figure → 自填 `topic`、`key_insight`、`evidence`。(2) 问 `audience_anchor` 和 `chosen_hook`。(3) 问 `trade_off`(论文很少诚实写 trade-off)。 |
| Blog URL | (1) `web_fetch` → 自填 `topic`。(2) 问 "你看完想 highlight 哪 1 句作为 key_insight"。(3) 后续走主题字符串流程。 |

## 关卡边界

完整的 brief —— emit 为 YAML block,所有必填字段填齐,如使用 override 则显式写出 —— 是进入 Step 2(卡片序列规划)的唯一通路。否则 model 不产出 HTML。
````

- [ ] **步骤 2:验证内容**

打开文件检查:
- 表格中列出全部 4 种 anchor 类型
- 出现完全一致(逐字)的中文拒绝协议文本
- 出现 override 短语("我先这么写,锚点之后补")
- 4 种输入类型的提问脚本都在

- [ ] **步骤 3:保存**

Skill 文件夹不是 git repo。不需要 commit。文件存在于磁盘上即可。

---

## 任务 2:创建 `references/qa-checklist.md`

**文件:**
- 新建:`references/qa-checklist.md`

- [ ] **步骤 1:写入文件**

按以下完整内容创建 `references/qa-checklist.md`:

````markdown
# Pre-flight QA Checklist

强制自检,在 Step 4 末尾、Step 5 之前 emit。Model 计算指标、emit 表格,并在交付给用户之前自动修复任何 FAIL。

## 逐卡指标

| 指标 | 计算方式 | PASS 阈值 |
|---|---|---|
| `char_count` | 卡正文的中文字符等量计数,排除 kicker、页码、标题、gist、trade-off 行 | 220 ≤ x ≤ 300 |
| `specifics` | 计数:数字、命名工具/库/文件/API/配置 flag、括号内具体场景、前后或 vs 对比 | ≥ 6 |
| `hand_drawn_elements` | 卡内使用的、来自 `visual-system.md` 词汇表中不同元素的数量 | 3 ≤ x ≤ 5 |
| `trade_off_present` | 布尔 —— 这张卡是否带 trade-off 行 | PASS 当 (a) trade-off 行存在,**或** (b) 卡类型是 `summary`,**或** (c) model 显式给出 `trade_off_skipped_reason`(≤ 16 字,例:"纯解释卡"、"无实际代价") |
| `bullet_specifics_floor` | 每条 bullet ≥ 1 specific;concept 卡 bullet ≥ 2 specifics | 全部 bullet 为 true |

一张卡所有指标都 PASS 才算 PASS。

## Post-level 一致性检查

规则来源:`post-structure.md`。

- [ ] 所有卡的 kicker 文字完全一致(只换页码)
- [ ] Cover 与 Summary 首条要点彼此呼应
- [ ] One-sentence narrative arc 不含 "and" / "和" / "而且"
- [ ] 任何卡都不能在不破坏叙事的前提下删除
- [ ] 至少 1 张 pitfall 卡(否则需显式说明为什么没有)

## QA 表格式(用户可见输出)

Model 在 Step 4 末尾 emit 这块 Markdown:

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

## 触发协议

| 情形 | Model 行为 |
|---|---|
| 任一卡 FAIL | 只重生这一张(其他不动),给出针对命中指标的明确修复。重生后对该卡再跑 QA。不允许把 FAIL 版本展示给用户。同卡重试上限 2 次 —— 仍 FAIL 则把具体差距上报用户。 |
| 一致性 ✗ | 点出问题;给出修法;等用户确认再改 |
| 全 PASS + 一致性全 ✓ | 进入 Step 5(导出指引) |

## 为什么这张表对用户可见

两点理由:
1. 用户拿到稿子的同时也拿到密度证据 —— 不用自己重新数 specifics。
2. 强迫 model 公开量化,等于强迫真自检,而不是凭感觉过一遍。
````

- [ ] **步骤 2:验证内容**

打开文件检查:
- 5 行指标全部存在
- `trade_off_present` 展示出三段式 OR 通过条件
- 触发协议中体现 2 次重生上限
- 5 条 post-level 一致性检查全部存在

- [ ] **步骤 3:保存**

不要 git commit(文件夹不是 git repo)。

---

## 任务 3:SKILL.md 编辑 A —— 修正 Inputs 段落措辞

**文件:**
- 修改:`SKILL.md` 第 26 行(`## Inputs the skill accepts` 下的主题字符串输入描述)

- [ ] **步骤 1:执行 edit**

使用 Edit 工具,严格使用以下字符串:

`old_string`:
```
   → Skill should ask 2–3 quick clarifying questions about specifics (numbers, the key insight, trade-off) before generating.
```

`new_string`:
```
   → Skill should ask 2–3 quick clarifying questions about specifics (a concrete anchor, the key insight, trade-off) before generating.
```

- [ ] **步骤 2:验证**

读 SKILL.md 的 25-27 行。确认新措辞已就位,且无其他文本被改动。

---

## 任务 4:SKILL.md 编辑 B —— 把 Step 1 替换为简报关卡指针

**文件:**
- 修改:`SKILL.md` 第 55-68 行(Step 1 整段,从 `### Step 1 — Build the post brief` 到 `Don't fabricate.`)

- [ ] **步骤 1:执行 edit**

使用 Edit 工具,严格使用以下字符串:

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

- [ ] **步骤 2:验证**

读 SKILL.md 第 55-70 行附近。确认:
- 新标题为 `### Step 1 — Build the post brief (Brief Gate)`
- `evidence` 行写的是 "concrete anchor",不再是 "specific number"
- 收尾段落引用了 `brief-gate.md` 与 override 机制

---

## 任务 5:SKILL.md 编辑 C —— 在 Step 5 之前插入 Step 4.5

**文件:**
- 修改:`SKILL.md` —— 在 Step 4 末尾(第 103 行)和 `### Step 5` 标题(第 105 行)之间插入新章节

- [ ] **步骤 1:执行 edit**

使用 Edit 工具,严格使用以下字符串:

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

- [ ] **步骤 2:验证**

读 SKILL.md 中 Step 4 → Step 5 的衔接处。确认:
- Step 4 与 Step 5 之间多出一个新的 `### Step 4.5 — Pre-flight QA` 章节
- 引用了 `references/qa-checklist.md`
- 提到了 2 次重生上限
- `### Step 5` 标题仍存在且未变动

---

## 任务 6:端到端验证(5 个场景)

**文件:** 不修改文件。本任务通过对照规格中测试计划的 5 个输入运行 skill,验证集成行为。

对每个场景,在新对话(或新 skill 调用)中以下面列出的输入调用 skill,然后对照预期行为检查输出。仅在观察到预期行为时才把对应步骤勾为 `- [x]`。

- [ ] **步骤 1:空主题拒绝**

输入:`想写一篇关于 LLM 的贴`

预期:model 必须 emit 来自 `brief-gate.md` 的逐字拒绝句:

> 需要至少一个具体锚点才能写——一个数字 / 一个前后对比 / 一个命名机制或工具 / 一个具体场景,任何一项都行。如果题目空到连这一条都给不出,先把题目收窄,这个 skill 故意不允许虚构。

Model 不能产出任何 HTML,也不能尝试自己填 `evidence`。

- [ ] **步骤 2:纯概念主题通过**

输入:`聊聊 RadixAttention 的 prefix sharing 机制`

预期:model 用 anchor 类型 (c) 自填 `evidence` —— 例如 `["RadixAttention prefix sharing 机制", "vanilla KV cache 复用差异"]` —— 然后继续问 `trade_off`。不触发拒绝。Brief block YAML 必须出现在 model 的回复中。

- [ ] **步骤 3:Repo URL 流程**

输入:`把 sgl-project/sglang 里的 PCP 实现做成一篇贴`(或任何用户能访问的具体 repo 路径)

预期:model 先读 README + 主要目录,自填 `topic` / `key_insight` / `audience_anchor` / 候选 `evidence`,然后专门追问 `trade_off`。Brief block YAML 必须在任何 HTML 之前 emit。

- [ ] **步骤 4:端到端 + QA 表**

输入:一份完整 brief(手动凑出全部 6 字段)。让 model 生成全部卡片 + 正文 + 话题。

预期 Step 4 末尾:model emit 一块 `## Pre-flight QA` Markdown,格式与 `qa-checklist.md` 中规定的一致。每张卡的行都填齐 5 列指标。"一致性"小节有 5 个 box(部分 ✓,如有问题则部分 ✗)。只有全部 PASS 后才会出现 Step 5 的导出指引。

为对 FAIL 处理做压力测试:把 model 草稿中的某张卡改稀(≤ 200 字、≤ 4 specifics)。重跑 QA。预期:那张卡显示 **FAIL**,model 仅对该卡自动重生,并写明修复要点,然后再次 emit QA 表,显示该行 PASS。

- [ ] **步骤 5:evidence_overridden draft 模式**

输入:一个空泛主题。当拒绝协议触发时,回复 `我先这么写,锚点之后补`。

预期:
- Model 在 brief block 中设置 `evidence_overridden: true`
- 最终正文以 `[draft · 锚点待补]` 开头
- QA 报告标记每一张论点会依赖缺失锚点的卡(通常是 architecture / pitfall / result 卡)
- 不因密度问题对被标记的卡发起重生(因为 draft 模式按定义就处于欠规格状态)

- [ ] **步骤 6:记录验证结果**

打开 `docs/spec/2026-04-29-brief-gate-and-qa-design.md`,在文档底部新增一个 `## Validation log` 章节,写入:
- 验证日期
- 哪些场景 PASS、哪些需要澄清
- 发现的任何新边界情况

这就是测试记录。skill 没有代码覆盖率工具 —— 这份手工日志是替代物。

---

## 自审笔记

规格覆盖检查:

| 规格章节 | 由哪个任务覆盖 |
|---|---|
| 组件 1(brief-gate.md 内容) | 任务 1 |
| 组件 2(qa-checklist.md 内容) | 任务 2 |
| 组件 3 —— Step 1 替换 | 任务 4 |
| 组件 3 —— Step 4.5 插入 | 任务 5 |
| 组件 3 —— 修正 SKILL.md 旧不一致(Inputs 段落) | 任务 3 |
| 组件 3 —— 修正 SKILL.md 旧不一致(Step 1 evidence 行 + 收尾段落) | 任务 4(整合处理 —— Step 1 整段替换,两处差异都包含在 diff 中) |
| 测试计划 #1(空主题拒绝) | 任务 6 步骤 1 |
| 测试计划 #2(纯概念通过) | 任务 6 步骤 2 |
| 测试计划 #3(Repo URL 流程) | 任务 6 步骤 3 |
| 测试计划 #4(端到端 QA) | 任务 6 步骤 4 |
| 测试计划 #5(evidence_overridden draft 模式) | 任务 6 步骤 5 |

无占位符。所有文件内容均逐字内联。所有 edit 的 `old_string` / `new_string` 配对均为精确字符串。无任何 "TODO"、"TBD" 或 "implement later"。

类型 / 路径一致性:brief-gate.md 与 qa-checklist.md 都置于 `references/` 下,与 SKILL.md 现有的 reference 约定一致。override 短语、拒绝句、字段名在三处文件中出现时完全一致。
