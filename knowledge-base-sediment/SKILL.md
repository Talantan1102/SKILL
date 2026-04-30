---
name: knowledge-base-sediment
description: 当用户想把一篇论文、博客、代码仓库或最近一段对话沉淀成 `D:\mys\kb\` 下的原子化 markdown 知识卡片时使用此 skill。触发条件包括显式的 `/sediment`、`/kb-find`、`/kb-review`、`/kb-render`、`/kb-reindex` 命令,提到"沉淀"、"知识库"、"Zettelkasten",或"帮我把这个记下来 / save what we just learned"等表达。
---

# 知识库沉淀(Knowledge Base Sediment)

## 概览

把非结构化输入(论文 / 博客 / 代码仓 / 对话)蒸馏成 `D:\mys\kb\<primary_tag>/<YYYYMMDD-slug>.md` 下的原子化 Markdown 知识卡。**Markdown 是 source of truth,HTML 是按需渲染。**这个 skill 是通用技术知识沉淀工具,不绑定项目也不绑定面试场景。

## 两个入口形式

```
/sediment <path-or-url> [--tag X] [--atomic|--summary] [--level=b|i|e] [--yolo]   # Mode A: 从源文件
/sediment [--tag X] [--atomic|--summary] [--level=b|i|e] [--yolo]                 # Mode B: 从对话上下文
```

## Reader-level (`--level=beginner|intermediate|expert`,默认 `intermediate`)

沉淀**不仅是给我自己留的笔记,更是带我学**的过程。要么让用户选,要么尊重 `--level`:

| Level | 单卡处理 | tag README primer |
|---|---|---|
| `expert` (e) | 不加"前置概念"段。多引用源文件 `file:line`。 | 跳过 primer。README 只列阅读顺序。 |
| `intermediate` (i,默认) | 首次出现非 CS 本科核心术语时,加 1-3 行"前置概念"或 inline 解释。 | Primer 含 **§1 动机 + §3 架构图 + §4 阅读顺序**,跳过"名词扫盲"段。 |
| `beginner` (b) | 每个新术语首次出现就在 inline 解释,避免术语堆叠。 | **完整 primer**(`templates/tag-readme.md` §1-§7),含"名词扫盲" + "为什么"引导问题。 |

reader-level 只影响**写作语气和 primer 是否出现**,不改变卡片数量或模板选择。

`--yolo` 缺省时 level 默认 `intermediate`。

## Helper 脚本(必须用 venv 内的 python)

本机的 bash `python` 不在 PATH 上,所有辅助脚本要用 venv 里的解释器:

```
PY=~/.claude/skills/knowledge-base-sediment/scripts/.venv/Scripts/python.exe
SCRIPTS=~/.claude/skills/knowledge-base-sediment/scripts
```

## Mode A — 从源文件沉淀

1. **解析输入。** URL → `curl`(先直连,失败时回退代理 `http://127.0.0.1:7897`)。PDF → `pypdf`(已装在 venv 里)。目录 → 列树,问用户选哪些路径或尊重 `--glob`。单文件 → 直接 `Read`。
2. **检测 source 类型。** 代码文件占多 → `code`。论文结构(abstract / intro / method / experiments)→ `paper`。博客 HTML → `paper`。
3. **决定颗粒度。** 默认 ≈ 3-6 卡。`--atomic` → 5-15 张小卡。`--summary` → 1 张。
4. **展示候选卡列表**(`--yolo` 时跳过)。用户接受 / 挑选 / 重新拆分。
5. **逐卡撰写**,套 `templates/paper-card.md` 或 `templates/code-card.md`。保留源引用(页码 / `file:line`)。给 `confidence` 估值(high = 已验证,medium = 已理解,low = 二手)。`links` 通过 grep `INDEX-by-tag.md` 提议。
6. **落地** `D:\mys\kb\<primary_tag>/<YYYYMMDD-slug>.md`。id 冲突时:提示 skip / overwrite / `-v2` 变体。
7. **运行 `$PY $SCRIPTS/update_index.py --kb D:\mys\kb`** —— 任何写入后**强制必跑**。
8. **Git commit** 只 stage 这次写的卡 + INDEX 文件(**绝不 `git add -A`**)。Message: `sediment: <source-shorthand> +N cards`。**绝不自动 push。**

## Mode B — 从对话上下文沉淀

跳过步骤 1-2;从最近几轮对话提取候选卡。`source: conversation`,`source_ref: session-<datetime>-<topic-slug>`。其余步骤同 4-8。

## 代码仓输入(在 Mode A 里自动检测)

如果 `/sediment` 传入的 path 是目录且满足任一:
- 含 `.git/`
- 含 `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `Gemfile` / `pom.xml` / `setup.py` / `Makefile` / `CMakeLists.txt`
- 该目录下源文件(`.py/.js/.ts/.tsx/.rs/.go/.java/.kt/.rb/.cpp/.cc/.c/.h/.hpp/.cs/.swift/.scala`)≥ 5 个

→ 当成代码仓处理,Mode A 的"解析-然后-写"被替换为 **view 选择**步骤。反问:

```
检测到代码仓:<path>
请选 sediment 视角:
  A. 整仓架构总览  → 1 张总图卡
  B. 单 module 深挖 → 3-6 张机制卡
  D. 调用链 trace  → n 张顺序卡
  E. API 表面     → 1+ 张表卡
```

`--yolo` 时缺省走 A。`--view=arch|deep|trace|api` 跳过反问。View D 还需要 `--entry=<file:func>`(也可以在 path 里直接带 `<path>:<func>`)。如果选了 B 或 E 但 path 是 repo 根,二次反问选哪个 subdir。

### View A — 整仓总览

读取顺序:`README.*`,顶层 `ls`(剔除 `.git/ node_modules/ dist/ build/ .venv/ __pycache__/ target/ .next/`),包清单,每个顶层源代码目录的入口文件(`__init__.py | index.{ts,js} | main.{py,go,rs} | mod.rs | lib.rs`)。产 **1 张卡**,套 `templates/arch-card.md`,落地 `D:\mys\kb\<tag>\<YYYYMMDD>-<repo-slug>-arch.md`。

### View B — 单 module 深挖

读所选 subdir 下所有源文件(剔 `tests/ __tests__/ *.test.* *_test.* *.spec.*` 与 vendored)。文件 > 20 时反问"全读还是只挑入口/最大几个?"。产 **3-6 张卡**,套 `templates/code-card.md`,每张聚焦一个机制 / 一个核心类 / 一段有趣实现。"可迁移模式"段允许留空。

### View D — 调用链 trace(每跳一卡,每跳 confirm)

```
hop 1: 读 <entry>;写候选卡 1(focus: 这个函数干嘛 + 调用了谁)
       问"下一跳进 <Y>?(y / n / 换 <Z> / stop)"
hop 2: 读用户确认的 callee;写候选卡 2,frontmatter `links` 加
       {id: <card_1>, rel: prev};回写 card 1 加 {id: <card_2>, rel: next};
       继续问下一跳
...
stop 条件: 用户说 stop / 走到叶子 / 检测到循环 / hop 数 ≥ 10
```

每张卡用 `templates/code-card.md`,落地 `<YYYYMMDD>-<entry-slug>-trace-<N>.md`。"可迁移模式"段允许留空。

### View E — API 表面

按语言惯例识别"public"接口:Python(顶层 def/class 名不以 `_` 开头或在 `__all__` 里),JS/TS(`export`),Go(首字母大写),Rust(`pub`),Java/Kotlin(`public`)。

如果 ≤ 15 个 API:**1 张卡**,套 `templates/api-card.md`。如果 > 15:按 submodule/file 拆,每张子卡的 `links` 互引同组 peer,`rel: see-also`。

### Tag README — 入口 primer + 导航

**任何超过 1 张卡的 tag 强制生成。**写完卡之后,从 `templates/tag-readme.md` 生成 `D:\mys\kb\<tag>\README.md`。各段(按 `--level` 缩放):

1. 这个领域 / 模块解决什么(2 分钟版)— 用户视角的痛点 → 解法
2. 名词扫盲(beginner 必填,intermediate 可选,expert 跳过)
3. **整体架构 / 概念图(Mermaid)** — view A/D 必有;view B 强烈建议
4. 推荐阅读顺序 — 标注哪张最难
5. 阅读时的"为什么" — 4-8 个引导问题
6. 读完之后能干什么
7. 与其他 tag 的关系

`update_index.py` 跳过 `README.md`(不计入 card 数,不出现在 INDEX-by-tag)。

### 数学公式(LaTeX,经 MathJax 渲染)

卡片可以用 **inline `$...$`** 与 **block `$$...$$`** LaTeX。`render_html.py` 自动注入 MathJax v3(SVG 输出),公式会在浏览器里渲染。

- `$\hat A_t = r_t - \bar r$` → 行内公式
- `$$\nabla_\theta \mathcal{J}(\theta) = \mathbb{E}\left[\sum_t \nabla \log \pi_\theta\right]$$` → 展示公式

**别**把公式包在 code span(`` ` ``)里 —— MathJax 会跳过 code 元素。**别**在 `$...$` 之外裸写 `_` —— 会被 markdown italic 吃。**始终把公式包在 `$..$` 里。**

在 markdown 预览器(VSCode 等)里,`$..$` 显示为字面字符 —— 这是预期的;HTML 渲染才是规范视图。

### Mermaid 可视化

卡片可以嵌 ` ```mermaid ` 围栏块。`render_html.py` 注入 mermaid.js CDN,**默认套用 paper-and-ink theme**(米色 + 皮革色调色板 + serif 字体),所有图都跟 library 视觉语言一致,不需要每张图单独配色。

**强烈建议:**

- **View A 总览卡**:必有架构图(`graph TB / TD`)
- **状态机/调用链卡**:必有 `stateDiagram-v2` 或 `sequenceDiagram`
- **Tag README**:必有领域概念图(放在 §3)

不强求每卡都画;**只在文字读起来"绕"的地方上图**。

### 什么时候用 Excalidraw / frontend-design 而不是 Mermaid

Mermaid 适合**示意图**(box-arrow-state),配色已统一。三种 escalation 路径:

| 需要 | 工具 | 产物 | 嵌入方式 |
|---|---|---|---|
| 流程 / 状态 / 序列 / 依赖示意 | **Mermaid** ` ```mermaid ` 块 | 浏览器运行时渲染 | 直接写在 markdown body |
| README hero / 概念图 / 训练循环示意 | **Excalidraw skill** | `.excalidraw` JSON + 转 SVG | `_assets/*.svg`,`![](...)` 引用 |
| Hero 插画 / 抽象艺术 / 卡片封面图 | **frontend-design skill** | HTML/CSS/SVG | 嵌入 markdown body |

#### Excalidraw 工作流(完整)

1. **生成**:调用 `excalidraw-diagram-generator` skill,产 `.excalidraw` JSON 落到 `kb/<tag>/_assets/<name>.excalidraw`
2. **转 SVG**:跑 `python ~/.claude/skills/knowledge-base-sediment/scripts/excalidraw_to_svg.py <input.excalidraw>` —— 同目录产 `<name>.svg`(简洁版,丢失 rough.js 手绘感)
   - 想要真正的手绘感:把 `.excalidraw` 拖进 [excalidraw.com](https://excalidraw.com),File → Export image → SVG,**覆盖**自动生成的 `.svg`
3. **引用**:卡片或 README 里写 `![alt](_assets/<name>.svg)`
4. **render_html.py 自动 inline**:把 `<img src="_assets/x.svg">` 替换成 `<figure class="diagram"><svg>...</svg></figure>`,产物自包含,无相对路径风险

`.excalidraw` 源文件保留在 `_assets/` 里,用户随时可以打开 excalidraw.com 编辑。

### Library 导航(catalog → tag → card)

KB 像图书馆一样长大。三层导航相互保持同步:

| 入口 | 路径 | 由谁产 |
|---|---|---|
| **Library catalog(HTML 总入口)** | `D:\mys\kb\_render\index.html` | `render_html.py --tag library` |
| **单 tag 页**(primer + 卡 + 返回链接) | `D:\mys\kb\_render\<tag>.html` | `render_html.py --tag <tag>` |
| **Markdown 索引**(可点击 tag 列表 / 按日期 / 按 tag) | `D:\mys\kb\INDEX*.md` | `update_index.py` |

用户路径:打开 `_render/index.html` → 点某个 tag 卡片 → 跳到该 tag 的 primer + 卡片。每张 tag 页面顶部都有 `← Library` 返回链接。

**任何卡片或 tag README 改动,必须同时重渲染该 tag 与 library 入口**(参见 `kb-render` slash command)。

### 路径 / 链接完整性

`render_html.py` 自动改写 markdown 的 `.md` 链接,HTML 渲染绝不产生失效 `href`:

- **同 tag 链接** `[X](OTHER-CARD-ID.md)` → `<a href="#OTHER-CARD-ID">`(同页锚点)
- **跨 tag 链接** `[X](../<other-tag>/CID.md)` → `<a href="<other-tag>.html#CID">`(相对 HTML 路径)
- **外部 / fragment / 绝对路径**链接保持原样

写卡 markdown 时,**永远用 sibling-relative `.md` 路径**(VSCode 预览和 HTML 渲染都能工作)。**永远不要手写 `#id` 锚点** —— 让 renderer 处理。

### Frontmatter `links` schema

所有卡片用结构化 `links`:

```yaml
links:
  - id: <other-card-id>
    rel: see-also   # 或: prev / next(仅 D-trace 用)
```

旧的 list-of-str 格式仍能解析。要把已有 kb 原地迁移:

```
$PY $SCRIPTS/migrate_links.py --kb D:\mys\kb
```

## 启动 (`D:\mys\kb\` 首次使用)

如果 `D:\mys\kb\` 不存在或为空:

```bash
mkdir -p /d/mys/kb
cd /d/mys/kb
git init
echo "_render/" > .gitignore
cat > .kbconfig <<'EOF'
proactive_suggest: false
default_granularity: medium
auto_commit: true
default_confidence: medium
EOF
```

然后写 `D:\mys\kb\README.md`(模板在 `~/.claude/skills/knowledge-base-sediment/templates/kb-readme.md`,不存在则 inline 生成)。

## 自动加载 + 被动唤起

会话开始时,如果 cwd 或话题命中 `D:\mys\kb\INDEX.md` 里已有的 tag,Read `INDEX.md`(很小)一次。对话中如果话题强烈匹配某张卡的 title,提一句"你之前沉淀过 [card-id],要不要先看看?" —— 用户确认后再读全文。

**不要**每次回复都 read INDEX —— 只在话题切换或显式技术问题时读。

## 主动建议(默认 OFF)

只有当 `D:\mys\kb\.kbconfig` 里 `proactive_suggest: true` 才生效。然后**建议**(永远不自动写)`/sediment`,在以下场景:
- 用户刚解决一个 root cause 不显然的非平凡 bug
- 用户刚理解一个不显然的算法 trade-off
- 用户刚在源代码里识别出一个可迁移的设计模式
- 用户说"原来如此 / 学到了 / 没想到 / 长见识 / wow / 草"

**不要**给以下场景建议:标准 API 用法;项目特定细节(那些归 CLAUDE.md / auto-memory);一次性 debug trace。

## 常见错误

| 错误 | 修法 |
|---|---|
| 写了一张巨型大卡,没拆成 3-6 张原子卡 | 默认颗粒度 medium。先问"要不要拆成 N 张原子卡?"再写。 |
| 写完卡忘了跑 `update_index.py` | 强制必跑。INDEX 是未来的 Claude 找到这次工作的方式。 |
| 用了 `git add -A` | **只 stage** 这一轮触发的卡 + INDEX 文件。 |
| 自动 push 到远端 | 永不。push 是用户的决定。 |
| 给没验证过的论文论断填 `confidence: high` | 理论理解默认 `medium`;只有自己跑过的代码才 `high`。 |
| 跳过候选确认列表 | `--yolo` 时才能跳。用户对拆分的意见比你的更重要。 |
| 把标准 API 用法做成卡 | 那不是知识,是 lookup。跳过。 |
| 用 `python` 而不是 venv 内的 `python.exe` | `python` 不在 PATH,辅助脚本会找不到。永远用显式 venv 解释器路径。 |
| 喂代码仓给 `/sediment` 但只产了 1 张卡 | 触发 view 选择(A/B/D/E)。只有 view A 是单卡,B/D/E 都产多卡。 |
| 写完一组卡没建 README primer | Tag README 是导航入口,**任何 > 1 卡的 sediment 都必须生成**。`update_index.py` 已跳过它,不计入 card count。 |
| 状态机 / 调用链 / 架构卡纯文字 | 在文字"读起来绕"的地方上 Mermaid。`render_html.py` 自动渲染 mermaid block。 |
| 用 expert level 写卡给 beginner 用户 | 反问 reader-level,不主观假设;`--level=beginner` 时每卡顶部加"前置概念" prelude。 |

## 快速参考

| 命令 | 动作 |
|---|---|
| `/sediment <src>` | Mode A,从 path/URL 沉淀 |
| `/sediment` | Mode B,从对话沉淀 |
| `/sediment --yolo <src>` | 跳过候选确认 |
| `/kb-find <q>` | 搜索,排序按 title > tag > body |
| `/kb-review <tag>` | 交互式翻该 tag 的卡 |
| `/kb-render <tag>` | 静态 HTML 渲染到 `_render/` |
| `/kb-reindex` | 强制重建所有 INDEX |
| `/sediment <repo> --view=arch\|deep\|trace\|api [--entry=<f:fn>]` | 代码仓 4 视角入口 |
