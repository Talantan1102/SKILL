# 发布前自检清单

在第 4 步末尾、第 5 步之前强制输出的自审环节。模型计算各项指标、输出表格,并在交付给用户之前自动修正所有 FAIL。

## 单卡指标

| 指标 | 计算方式 | PASS 阈值 |
|---|---|---|
| `char_count` | 卡片正文的中文字符等价数,不计 kicker、页码、标题、gist 和 trade-off 行 | 200 ≤ x ≤ 260(硬上限 280,超过则拆成两张卡) |
| `specifics` | 计数:数字、命名的工具/库/文件/API/配置开关、括号里的具体场景、前后对比或 vs 比较 | ≥ 6 |
| `hand_drawn_elements` | 卡片中使用的、来自 `visual-system.md` 词汇表的不同元素的数量 | 3 ≤ x ≤ 5 |
| `trade_off_present` | 布尔值 —— 卡片是否带有一行 trade-off | 满足以下任一即 PASS:(a) 有 trade-off 行,或 (b) 卡片类型是 `summary`,或 (c) 模型显式输出 `trade_off_skipped_reason`(≤ 16 字,例如 "纯解释卡"、"无实际代价") |
| `bullet_specifics_floor` | 每个 bullet 至少 1 个 specific;概念卡的 bullet 至少 2 个 specifics | 所有 bullet 均满足 |
| `bullet_wrap_visual` | 心算法:11px 字号、360px 卡片、约 316px 内容宽度。纯中文 bullet 60 字左右换行 2 行;90+ 字会换行 3+ 行 | 每个 bullet ≤ 2 视觉行。3 行 bullet 必须拆或裁 |
| `watermark_present` | 卡片有 `<svg>` 水印层(对应 `visual-system.md` 的"水印层"):pattern id `wm-NN`、opacity 0.05–0.06、文本与帖子选定的作者 handle 匹配 | 三项全 true 才 PASS。缺失水印 → 重新生成卡片 |

只有当每一项指标都 PASS,该卡片才算 PASS。

## 封面专项检查

规则来源:`visual-system.md` 的 "Cover anchor system v2"、`hook-patterns.md` 的 "Anchor selection table" 与 "Cover failure modes"。封面是这篇帖子在缩略图中被识别的唯一一次机会;封面失手,即便其他卡全部通过,这篇帖子也会沉。

| 指标 | 计算方式 | PASS 阈值 |
|---|---|---|
| `archetype` | 用了哪个 V1/V2/V3 | V1(Number Hero)/ V2(Logo Block)/ V3(Schematic Peek)三选一 —— 不能是 v0 那种混搭 |
| `anchor_present` | (a)/(b)/(c) 三种锚点之一可见 | (a) 数字 ≥ 80px,或 (b) wordmark ≥ 64px,或 (c) 示意图 ≥ 100×80px 且至少 3 个元素 |
| `thumbnail_readable` | 锚点在 200px 宽缩略图下仍可辨认 | 渲染 HTML、浏览器缩放至 25%,锚点必须仍能被前注意识别 |
| `failure_mode_clear` | 不命中 `hook-patterns.md` "Cover failure modes" 中的任何一种模式 | 不出现:Notion 截图风 / 锚点被埋 / 副标题剧透 / 装饰当锚点 |
| `supporting_count` | 辅助装饰元素计数(kicker/分割线/阅读时长/色条/VOL/角标数字) | 强制 2 个(kicker+分割线、阅读时长)+ 0–2 个可选。总数 ≤ 5。 |
| `subtitle_role` | 副标题给出的是结构性背景而不是答案 | 副标题是 workload/版本号/规模/系列号 —— 不能概括帖子的主论点 |
| `wordmark_fit`(仅 V2) | 每行 wordmark 估算渲染宽度 = `字符数 × 字号 × 0.55` | ≤ 316 px(= 360 卡宽 − 2×22 padding)。失败 → 按 `card-templates.md` "Wordmark length cap" 调字号(如 84 → 64)或缩写。**常见踩坑**:`DeepSeek`(8 字)在 84px 下 = 370px,会溢出。 |
| `watermark_present` | 封面有 `visual-system.md` 中定义的 SVG 水印层,V2 用深色变体(米色文本、opacity 0.06),V1/V3 用浅色变体(深色文本、opacity 0.05) | 存在 + 表面变体匹配,才 PASS |

只有当每一项指标都 PASS,该封面才算 PASS。如果 `archetype` 与 `chosen_hook` 在 hook-patterns 选择表中不匹配,作为一致性 ✗ 上抛 —— 提议要么换 hook、要么换 archetype,等待用户确认。

## 帖子级别一致性检查

规则来源:`post-structure.md`。

- [ ] 所有卡片的 kicker 文案完全一致(只有页码变化)
- [ ] 封面与 Summary 卡的第一条 takeaway 互相呼应
- [ ] 一句话叙事弧中没有 "and" / "和" / "而且"
- [ ] 任何一张卡都不能在不破坏叙事的前提下删掉
- [ ] 至少存在一张 pitfall 卡(或显式说明为什么没有)
- [ ] 封面 archetype 与所选 hook 在 `hook-patterns.md` 锚点选择表中匹配

## QA 表格格式(对用户可见的输出)

模型在第 4 步末尾输出如下 Markdown 块:

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

## 触发协议

| 情形 | 模型动作 |
|---|---|
| 任一卡片 FAIL | 仅重生成该张卡片(其它保留),并显式针对命中的指标修复。在重生成的卡片上重新跑 QA。不要把失败版本展示给用户。每张卡至多重生成 2 次 —— 仍然 FAIL,则把具体差距上抛给用户。 |
| 一致性 ✗ | 把问题上抛、提出修复方案,等待用户确认后再应用 |
| 全部 PASS + 一致性全 ✓ | 进入第 5 步(导出说明) |

## 为什么这张表对用户可见

两个理由:
1. 用户拿到帖子的同时就拿到了密度证据 —— 不必再手动数 specifics。
2. 强迫模型公开量化,会逼出真正的自查,而不是凭感觉过一遍。
