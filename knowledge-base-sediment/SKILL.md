---
name: knowledge-base-sediment
description: Use when the user wants to distill a paper, blog post, code repository, or recent conversation into atomic markdown knowledge cards under D:\mys\kb\. Triggers include explicit /sediment, /kb-find, /kb-review, /kb-render, /kb-reindex commands, mentions of "沉淀", "knowledge base", "Zettelkasten", or requests like "save what we just learned" / "把这个记下来".
---

# Knowledge Base Sediment

## Overview

Turn unstructured input (paper / blog / code / conversation) into atomic Markdown knowledge cards under `D:\mys\kb\<primary_tag>/<YYYYMMDD-slug>.md`. Markdown is the source of truth; HTML rendering is on-demand. The skill is general-purpose technical knowledge sedimentation — not project- or interview-specific.

## Two entry forms

```
/sediment <path-or-url> [--tag X] [--atomic|--summary] [--level=b|i|e] [--yolo]   # Mode A: from source
/sediment [--tag X] [--atomic|--summary] [--level=b|i|e] [--yolo]                 # Mode B: from conversation context
```

## Reader-level (`--level=beginner|intermediate|expert`, default `intermediate`)

Sediment is **not just notes-for-me; it's also learn-with-me**. Ask the user (or honor `--level`) to set reading depth:

| Level | Per card | Tag README primer |
|---|---|---|
| `expert` (e) | No "前置概念" prelude. Cite source line numbers heavily. | Skip primer. README only has reading order. |
| `intermediate` (i, default) | 1-3 line "前置概念" / inline term gloss when first using a term that's not in CS undergrad core. | Primer with **§1 motivation + §3 architecture diagram + §4 reading order**. Skip "名词扫盲". |
| `beginner` (b) | Each term explained inline first time. Avoid jargon stacking. | **Full primer** (§1-§7 of `templates/tag-readme.md`), including "名词扫盲" + "为什么" 引导问题. |

Reader-level only affects writing voice and presence of primer; it does NOT change card count or template choice.

`--yolo` defaults level to `intermediate` if unset.

## Helper scripts (always invoke via the venv's python)

The bash `python` command is not on PATH on this machine. Always invoke the helper scripts with the explicit venv interpreter:

```
PY=~/.claude/skills/knowledge-base-sediment/scripts/.venv/Scripts/python.exe
SCRIPTS=~/.claude/skills/knowledge-base-sediment/scripts
```

## Mode A — sediment from source

1. **Parse input.** URL → `curl` (try direct, fall back to proxy `http://127.0.0.1:7897`). PDF → `pypdf` (already installed in the venv). Directory → list tree, ask user which paths or honor `--glob`. Single file → `Read` directly.
2. **Detect `source` type.** Code-file-dominant → `code`. Paper structure (abstract/intro/method/experiments) → `paper`. Blog HTML → `paper`.
3. **Decide granularity.** Default ≈ 3–6 cards. `--atomic` → 5–15 small cards. `--summary` → 1.
4. **Show candidate card list** (skip if `--yolo`). User accepts / picks / re-splits.
5. **Write each card** using `templates/paper-card.md` or `templates/code-card.md`. Preserve source citations (page / `file:line`). Estimate `confidence` (high=verified, medium=understood, low=secondhand). Propose `links` by grepping `INDEX-by-tag.md`.
6. **Persist** to `D:\mys\kb\<primary_tag>/<YYYYMMDD-slug>.md`. On id collision: prompt skip / overwrite / `-v2` variant.
7. **Run `$PY $SCRIPTS/update_index.py --kb D:\mys\kb`** — mandatory after any write.
8. **Git commit** only the touched cards + index files (never `git add -A`). Message: `sediment: <source-shorthand> +N cards`. **Never push.**

## Mode B — from conversation context

Skip steps 1–2; extract candidate cards from recent turns. `source: conversation`, `source_ref: session-<datetime>-<topic-slug>`. Same steps 4–8.

## Code-repo input (auto-detected during Mode A)

When the path passed to `/sediment` is a directory satisfying any of:
- contains `.git/`
- contains `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `Gemfile` / `pom.xml` / `setup.py` / `Makefile` / `CMakeLists.txt`
- contains ≥ 5 source files (`.py/.js/.ts/.tsx/.rs/.go/.java/.kt/.rb/.cpp/.cc/.c/.h/.hpp/.cs/.swift/.scala`)

…treat input as a code repository and override Mode A's "parse-then-write" with a **view selection** step. Ask:

```
检测到代码仓:<path>
请选 sediment 视角:
  A. 整仓架构总览  → 1 张总图卡
  B. 单 module 深挖 → 3-6 张机制卡
  D. 调用链 trace  → n 张顺序卡
  E. API 表面     → 1+ 张表卡
```

`--yolo` defaults to A. `--view=arch|deep|trace|api` skips the prompt. View D additionally needs `--entry=<file:func>` (or pass it inline as `<path>:<func>`). If selected B or E and the path is the repo root, ask which subdir.

### View A — arch overview

Read in order: `README.*`, `ls` top level (skip `.git/ node_modules/ dist/ build/ .venv/ __pycache__/ target/ .next/`), package manifest, each top-level source dir's entry file (`__init__.py | index.{ts,js} | main.{py,go,rs} | mod.rs | lib.rs`). Produce **1 card** using `templates/arch-card.md`. Save as `D:\mys\kb\<tag>\<YYYYMMDD>-<repo-slug>-arch.md`.

### View B — module deep-dive

Read all source files in the chosen subdir (skip `tests/ __tests__/ *.test.* *_test.* *.spec.*` + vendored). If > 20 files, ask "全读还是只挑入口/最大几个?". Produce **3-6 cards** with `templates/code-card.md`, each focused on one mechanism / class / interesting implementation. The "可迁移模式" section may be left empty.

### View D — call-chain trace (one hop per card, confirm each)

```
hop 1: read <entry>; write card 1 (focus: this fn does X, calls Y/Z)
       ask "下一跳进 <Y>? (y / n / 换 <Z> / stop)"
hop 2: read confirmed callee; write card 2 with `links` containing
       {id: <card_1>, rel: prev}; back-edit card 1 to add
       {id: <card_2>, rel: next}; ask next hop
...
stop conditions: user says stop / leaf reached / cycle / hop count ≥ 10
```

Each card uses `templates/code-card.md`. Save as `<YYYYMMDD>-<entry-slug>-trace-<N>.md`. The "可迁移模式" section may be left empty.

### View E — API surface

Identify "public" by language convention: Python (top-level def/class without `_` prefix or in `__all__`), JS/TS (`export`), Go (capitalized name), Rust (`pub`), Java/Kotlin (`public`).

If ≤ 15 APIs: **1 card** using `templates/api-card.md`. If > 15: split by submodule/file; each subcard's `links` cross-refs all peers with `rel: see-also`.

### Tag README — entry primer + navigation

**Mandatory** for any tag with > 1 card (i.e. all non-summary outputs). Generate `D:\mys\kb\<tag>\README.md` from `templates/tag-readme.md` after writing the cards. Sections (scaled by `--level`):

1. 这个领域 / 模块解决什么(2 分钟版)— 用户视角的痛点 → 解法
2. 名词扫盲(beginner 必填,intermediate 可选,expert 跳过)
3. **整体架构 / 概念图(Mermaid)** — view A/D 必有;view B 强烈建议
4. 推荐阅读顺序 — 标注哪张最难
5. 阅读时的"为什么" — 4-8 个引导问题
6. 读完之后能干什么
7. 与其他 tag 的关系

`update_index.py` 跳过 `README.md`(不计入 card 数,不出现在 INDEX-by-tag)。

### Math formulas (LaTeX via MathJax)

Cards can use **inline `$...$`** and **block `$$...$$`** LaTeX. `render_html.py` auto-injects MathJax v3 (SVG output) so formulas render in the browser.

- `$\hat A_t = r_t - \bar r$` → inline math
- `$$\nabla_\theta \mathcal{J}(\theta) = \mathbb{E}\left[\sum_t \nabla \log \pi_\theta\right]$$` → display math

**Don't** wrap math in code spans (`` ` ``) — those are skipped by MathJax. **Don't** rely on naked `_` outside `$...$`(it'd be eaten by markdown italic);always wrap math in `$..$`.

In markdown source viewers (VSCode etc.), `$..$` shows as literal text — OK; HTML render is the canonical view.

### Mermaid for visualization

Cards may embed ` ```mermaid ` fences. `render_html.py` injects mermaid.js CDN with **paper-and-ink theme override** (cream/leather palette + serif font) so all diagrams match the library's visual language without per-card config.

**Strongly recommended:**

- **View A 总览卡**:必有架构图(`graph TB / TD`)
- **状态机/调用链卡**:必有 `stateDiagram-v2` 或 `sequenceDiagram`
- **Tag README**:必有领域概念图(放在 §3)

不强求每卡都画;**只在文字读起来"绕"的地方上图**。

### When to use Excalidraw / frontend-design instead of Mermaid

Mermaid is great for **schematic** diagrams(box-arrow-state),配色已统一。三种 escalation 路径:

| Need | Tool | 产物 | 嵌入方式 |
|---|---|---|---|
| 流程 / 状态 / 序列 / 依赖 schematic | **Mermaid** ` ```mermaid ` 块 | 浏览器 runtime 渲染 | 直接写在 markdown body |
| README hero / 概念图 / 训练循环示意 | **Excalidraw skill** | `.excalidraw` JSON + 转 SVG | `_assets/*.svg`,`![](...)` 引用 |
| Hero illustration / 抽象艺术 / 卡片封面图 | **frontend-design skill** | HTML/CSS/SVG | 嵌入 markdown body |

#### Excalidraw 工作流(完整)

1. **生成**:调用 `excalidraw-diagram-generator` skill,产 `.excalidraw` JSON 落到 `kb/<tag>/_assets/<name>.excalidraw`
2. **转 SVG**:跑 `python ~/.claude/skills/knowledge-base-sediment/scripts/excalidraw_to_svg.py <input.excalidraw>` —— 同目录产 `<name>.svg`(简洁版,丢失 rough.js 手绘感)
   - 想要真正手绘感:把 `.excalidraw` 拖进 [excalidraw.com](https://excalidraw.com),File → Export image → SVG,**覆盖**自动生成的 `.svg`
3. **引用**:卡片或 README 用 `![alt](_assets/<name>.svg)`
4. **render_html.py 自动 inline**:把 `<img src="_assets/x.svg">` 替换成 `<figure class="diagram"><svg>...</svg></figure>`,产物自包含,无相对路径风险

`.excalidraw` 源文件保留在 `_assets/` 里,用户随时可以打开 excalidraw.com 编辑。

### Library navigation (catalog → tag → card)

The KB grows like a library. Three navigation surfaces are kept in sync:

| Surface | Path | Generated by |
|---|---|---|
| **Library catalog (HTML entry point)** | `D:\mys\kb\_render\index.html` | `render_html.py --tag library` |
| **Per-tag page** (primer + cards + back-link) | `D:\mys\kb\_render\<tag>.html` | `render_html.py --tag <tag>` |
| **Markdown indexes** (clickable tag list, by-date, by-tag) | `D:\mys\kb\INDEX*.md` | `update_index.py` |

User flow: open `_render/index.html` → click a tag entry → land on tag's primer + cards. Each per-tag HTML carries `← Library` back-link.

**Whenever any card or tag README changes, re-render BOTH the affected tag AND the library landing** (see kb-render slash command).

### Path / link integrity

`render_html.py` automatically rewrites markdown's `.md` links so HTML rendering never produces broken `href`s:

- **Same-tag link** `[X](OTHER-CARD-ID.md)` → `<a href="#OTHER-CARD-ID">` (in-page anchor)
- **Cross-tag link** `[X](../<other-tag>/CID.md)` → `<a href="<other-tag>.html#CID">` (relative HTML path)
- **External / fragment / absolute** links left untouched

When writing card markdown,**always** use sibling-relative `.md` paths (works in both VSCode preview and HTML render). Never hand-write `#id` anchors directly — let the renderer handle it.

### Frontmatter `links` schema

All cards use structured `links`:

```yaml
links:
  - id: <other-card-id>
    rel: see-also   # or: prev / next (D-trace only)
```

Legacy list-of-str format still parses. To migrate any kb in-place:

```
$PY $SCRIPTS/migrate_links.py --kb D:\mys\kb
```

## Bootstrap (first use of D:\mys\kb\)

If `D:\mys\kb\` does not exist or is empty:

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

Then write `D:\mys\kb\README.md` (template in `~/.claude/skills/knowledge-base-sediment/templates/kb-readme.md` if present, otherwise generate inline).

## Auto-load + passive recall

On session start, if cwd or topic mentions an existing tag (matched against `D:\mys\kb\INDEX.md`), Read `INDEX.md` (small) once. During conversation, when a topic strongly matches a card title, surface "你之前沉淀过 [card-id], 要不要先看看?" — only on confirmation read full content.

Don't read INDEX on every reply — only on topic shifts or explicit technical questions.

## Proactive suggestion (default OFF)

Only when `D:\mys\kb\.kbconfig` has `proactive_suggest: true`. Then **suggest** (never auto-write) `/sediment` when:
- User just solved a non-trivial bug with a non-obvious root cause.
- User just understood a non-obvious algorithm tradeoff.
- User just identified a transferable design pattern in source code.
- User says "原来如此 / 学到了 / 没想到 / 长见识 / wow / 草".

**Don't** suggest for: standard API usage; project-specific details (those go in CLAUDE.md / auto-memory); one-off debug traces.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Wrote one giant card instead of 3–6 atomic ones | Default granularity is medium. Ask "would these split better as N atomic cards?" before writing. |
| Forgot to call `update_index.py` after writing | Mandatory. INDEXes are how future Claude finds your work. |
| Used `git add -A` | Stage **only** the cards + index files touched this turn. |
| Auto-pushed to remote | Never. Push is the user's call. |
| Filled `confidence: high` for paper claims you didn't verify | Default `medium` for theoretical understanding; `high` only for code you've personally run. |
| Skipped the candidate confirmation list | Required unless `--yolo`. The user's vote on splitting is more important than yours. |
| Sedimented standard API usage | That's not knowledge — it's lookup. Skip. |
| Used `python` instead of the venv's python.exe | `python` is not on PATH; helper scripts won't be found. Always use the explicit venv interpreter. |
| Fed a code repo to `/sediment` and only wrote 1 card | Trigger view selection (A/B/D/E). Only view A is a single card; B/D/E produce multiple. |
| 写完一组卡没建 README primer | Tag README 是 navigation entry,**任何 > 1 卡的 sediment 都必须生成**。`update_index.py` 已跳过它,不计入 card count。 |
| 状态机/调用链/架构卡纯文字 | 在文字"读起来绕"的地方上 Mermaid。`render_html.py` 自动渲染 mermaid block。 |
| 用 expert level 写卡给 beginner 用户 | 反问 reader-level,不主观假设;`--level=beginner` 时每卡顶部给 "前置概念" prelude。 |

## Quick reference

| Command | Action |
|---|---|
| `/sediment <src>` | Mode A from path/URL |
| `/sediment` | Mode B from conversation |
| `/sediment --yolo <src>` | Skip candidate confirmation |
| `/kb-find <q>` | Search ranked title>tag>body |
| `/kb-review <tag>` | Walk a tag's cards interactively |
| `/kb-render <tag>` | Static HTML render to `_render/` |
| `/kb-reindex` | Force-rebuild all INDEXes |
| `/sediment <repo> --view=arch\|deep\|trace\|api [--entry=<f:fn>]` | Code-repo 4-view entry |
