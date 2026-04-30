# 简报关卡

进入帖子生成环节前的强制 schema 与拒绝协议。模型必须在产出任何 HTML 之前先输出一段完整的简报块。

## Schema

```yaml
brief:
  topic: "<一行话,这篇帖子讲什么>"
  key_insight: "<一行话,把全篇串起来的那个不那么显而易见的点>"
  evidence:                          # 必填,≥ 1 个具体锚点(下表四种类型之一)
    - "<数字 / 前后对比 / 命名机制·工具·文件·API / 具体场景>"
    - "..."
  trade_off: "<一行话,这件事的代价 —— 必填,绝不能写'无'>"
  audience_anchor: "<读者已经熟悉的某个概念>"
  chosen_hook: <A | B | C | D>
```

## `evidence` —— 具体锚点类型

PASS 标准:简报中包含 **≥ 1 个具体锚点**,属于下面四类中任一种。

| 类型 | 示例 |
|---|---|
| (a) 硬数字 | `75s → 24s`、`p95 120ms`、`60% token 降幅` |
| (b) 前后对比 / 比较 | `43 → 7`、`Zigzag vs Ring Attention` |
| (c) 命名的机制 / 工具 / 文件 / API | `RadixAttention prefix sharing`、`tokenizer.json offset 字段`、`SGLang 的 PCP 实现` |
| (d) 具体场景 | `"喜欢 Python" 埋在 100 条 "thanks" 里`、`5 个 GPU 节点 RDMA 配置` |

这条门槛与单卡级别的 `specifics` 定义一致:一个具体的、有名字的、不可编造的东西。Hook A/B 通常踩 (a)(b);Hook C/D 通常踩 (c)(d)。

## 拒绝协议

当 `evidence` 缺失,或所有条目都是没有数字、没有命名机制、没有具体场景的空泛说法时,模型必须停下,并(原文照抄,使用用户的语言)回复:

> 需要至少一个具体锚点才能写——一个数字 / 一个前后对比 / 一个命名机制或工具 / 一个具体场景,任何一项都行。如果题目空到连这一条都给不出,先把题目收窄,这个 skill 故意不允许虚构。

当 `trade_off` 缺失,或被填成 "无" / "无明显代价" / 含糊其辞的搪塞时,模型必须停下,并(原文照抄)回复:

> 这个改动一定有代价(哪怕轻微)。是慢了一点 / 多耗显存 / 新人读不懂?写出来才往下走。

### evidence 强制覆盖

用户只有显式输入诸如 "我先这么写,锚点之后补" 这样的明确语句,才能绕过 evidence 拒绝。一旦触发:

- 模型在简报块中记录 `evidence_overridden: true`
- 帖子降级为 **draft** 模式:正文必须以 `[draft · 锚点待补]` 开头
- QA 报告必须标记每一张论据依赖该缺失锚点的卡片
- 用户负责在发布前把锚点补齐

`trade_off` 不存在强制覆盖通道 —— 如果用户真的说不出 trade-off,这个题目就还没准备好用这种格式来写。

## 按输入类型的提问脚本

| 输入 | 操作顺序 |
|---|---|
| 题目字符串 | 在 2–3 条消息内问齐全部 6 个字段。分组:(topic + key_insight)、(evidence + trade_off)、(audience_anchor + chosen_hook) |
| Repo URL / 路径 | (1) 读 README 和关键目录,自动填 `topic`、`key_insight`、`audience_anchor`,并提出具体的命名模块 / 文件 / API 作为 `evidence` 候选。(2) 提问:"benchmark 跑得出哪个数?或者你想 highlight 哪个具体机制?" 用以确认或扩展 evidence。(3) 询问 `trade_off`。(4) 根据内容形态推荐 `chosen_hook`。 |
| 论文 PDF / arXiv | (1) 抽取摘要、标题数字或命名方法、1 张图 → 自动填 `topic`、`key_insight`、`evidence`。(2) 询问 `audience_anchor` 和 `chosen_hook`。(3) 询问 `trade_off`(论文很少诚实写出代价)。 |
| 博客 URL | (1) `web_fetch` → 自动填 `topic`。(2) 提问 "你看完想 highlight 哪 1 句作为 key_insight"。(3) 后续按题目字符串流程继续。 |

## 关卡边界

完整的简报 —— 以 YAML 块的形式输出、所有必填字段已填、若使用了强制覆盖则覆盖标志显式标出 —— 是进入第 2 步(卡片序列规划)的唯一通道。没有它,模型不产出 HTML。
