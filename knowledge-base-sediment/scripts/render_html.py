#!/usr/bin/env python3
"""把 kb/<tag>/*.md(或 all / library)渲染成单个静态 HTML 页面。

用法:
    python render_html.py --kb <path> --tag <tag>|all|library --template <path-to-base.html>
"""
from __future__ import annotations

import argparse
import html
import pathlib
import re
import sys

import yaml
from markdown_it import MarkdownIt

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

md = MarkdownIt("commonmark", {"html": False, "linkify": True}).enable("table").enable("strikethrough")


def _render_fence(self, tokens, idx, options, env):
    """Custom fence: emit ```mermaid blocks as <pre class="mermaid"> for mermaid.js."""
    token = tokens[idx]
    info = (token.info or "").strip()
    if info == "mermaid":
        return f'<pre class="mermaid">{html.escape(token.content)}</pre>\n'
    lang = info.split()[0] if info else ""
    cls = f' class="language-{html.escape(lang)}"' if lang else ""
    return f'<pre><code{cls}>{html.escape(token.content)}</code></pre>\n'


md.add_render_rule("fence", _render_fence)


MERMAID_SCRIPT = """
<script type="module">
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
mermaid.initialize({
  startOnLoad: true,
  securityLevel: "loose",
  theme: "base",
  themeVariables: {
    fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", "Source Han Serif SC", serif',
    fontSize: "15px",
    primaryColor: "#faf6ef",
    primaryTextColor: "#1f1d1a",
    primaryBorderColor: "#7a3b14",
    secondaryColor: "#fff5d6",
    secondaryTextColor: "#1f1d1a",
    secondaryBorderColor: "#d8b596",
    tertiaryColor: "#f3efe6",
    tertiaryTextColor: "#1f1d1a",
    tertiaryBorderColor: "#d8d2c4",
    lineColor: "#5a554d",
    textColor: "#1f1d1a",
    mainBkg: "#ffffff",
    nodeBorder: "#7a3b14",
    clusterBkg: "#faf6ef",
    clusterBorder: "#d8d2c4",
    edgeLabelBackground: "#faf6ef",
    noteBkgColor: "#fff5d6",
    noteTextColor: "#1f1d1a",
    noteBorderColor: "#d8b596"
  }
});
</script>
"""

MATHJAX_SCRIPT = """
<script>
window.MathJax = {
  tex: {
    inlineMath:  [["$", "$"], ["\\\\(", "\\\\)"]],
    displayMath: [["$$", "$$"], ["\\\\[", "\\\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    skipHtmlTags: ["script", "noscript", "style", "textarea", "pre", "code"]
  },
  svg: { fontCache: "global" }
};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
"""


def parse_card(path: pathlib.Path) -> tuple[dict, str] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None
    return fm, parts[2]


def collect(kb: pathlib.Path, tag: str) -> list[tuple[pathlib.Path, dict, str]]:
    if tag == "all":
        paths = sorted(kb.glob("*/*.md"))
        paths = [p for p in paths
                 if not p.parent.name.startswith(".") and p.parent.name != "_render"]
    else:
        d = kb / tag
        if not d.exists() or not d.is_dir():
            return []
        paths = sorted(d.glob("*.md"))
    out = []
    for p in paths:
        if p.name == "README.md":
            continue  # README is rendered separately as primer
        parsed = parse_card(p)
        if parsed:
            out.append((p, parsed[0], parsed[1]))
    out.sort(key=lambda t: str(t[1].get("created", "")), reverse=True)
    return out


def render_tag_readme(kb: pathlib.Path, tag: str,
                      current_ids: set[str], all_tag_ids: dict[str, set[str]]) -> str:
    """If kb/<tag>/README.md exists, render its body as a primer HTML section.
    Returns "" if no README or tag == "all"."""
    if tag == "all":
        return ""
    readme = kb / tag / "README.md"
    if not readme.exists():
        return ""
    text = readme.read_text(encoding="utf-8")
    text_safe, math_saved = _protect_math(text)
    text_safe, bold_saved = _protect_bold(text_safe)
    body_html = md.render(text_safe)
    body_html = _restore_bold(body_html, bold_saved)
    body_html = _restore_math(body_html, math_saved)
    body_html = _inline_local_svgs(body_html, readme.parent)
    body_html = _rewrite_links(body_html, current_ids, all_tag_ids)
    return f'<section class="primer">{body_html}</section>\n'


def build_tag_index(kb: pathlib.Path) -> dict[str, set[str]]:
    """Walk all kb tag dirs, collect {tag_name: set of card_ids}."""
    out: dict[str, set[str]] = {}
    for tag_dir in kb.iterdir():
        if not tag_dir.is_dir() or tag_dir.name.startswith(".") or tag_dir.name == "_render":
            continue
        ids: set[str] = set()
        for md_path in tag_dir.glob("*.md"):
            if md_path.name == "README.md":
                continue
            parsed = parse_card(md_path)
            if parsed and "id" in parsed[0]:
                ids.add(str(parsed[0]["id"]))
        out[tag_dir.name] = ids
    return out


_HREF_RE = re.compile(r'href="([^"]+)"')
_CROSS_TAG_RE = re.compile(r"^\.\./([^/]+)/([^/]+)\.md$")

_BLOCK_MATH_RE = re.compile(r"\$\$.+?\$\$", re.DOTALL)
_INLINE_MATH_RE = re.compile(r"\$[^$\n]+?\$")
_BOLD_RE = re.compile(r"\*\*([^*\n]+?)\*\*")
_LOCAL_SVG_IMG_RE = re.compile(r'<img[^>]*\ssrc="(_assets/[^"]+\.svg)"[^>]*/?>')


def _inline_local_svgs(body_html: str, source_dir: pathlib.Path) -> str:
    """Replace <img src="_assets/*.svg"> with the SVG file's contents inline.
    The rendered HTML lives in _render/, so relative paths to _assets/ would
    otherwise be broken. Inlining makes the page self-contained."""
    def repl(m: re.Match) -> str:
        rel = m.group(1)
        svg_path = source_dir / rel
        if not svg_path.exists():
            return m.group(0)
        try:
            svg_text = svg_path.read_text(encoding="utf-8")
        except OSError:
            return m.group(0)
        # Strip any XML prolog so the SVG nests cleanly inside <p>.
        svg_text = re.sub(r"^\s*<\?xml[^?]*\?>\s*", "", svg_text)
        return f'<figure class="diagram">{svg_text}</figure>'
    return _LOCAL_SVG_IMG_RE.sub(repl, body_html)


def _protect_math(body: str) -> tuple[str, dict[str, str]]:
    """Replace `$..$` and `$$..$$` with alphanumeric placeholders so markdown's
    emphasis processing won't mangle underscores inside formulas."""
    saved: dict[str, str] = {}
    counter = [0]

    def stash(m: re.Match) -> str:
        key = f"MATHPLACEHOLDER{counter[0]:04d}"
        counter[0] += 1
        saved[key] = m.group(0)
        return key

    body = _BLOCK_MATH_RE.sub(stash, body)
    body = _INLINE_MATH_RE.sub(stash, body)
    return body, saved


def _restore_math(html_text: str, saved: dict[str, str]) -> str:
    """HTML-escape math content during restore. Browsers MUST NOT see literal `<`,
    `>`, `&` (e.g. `o_{i,<t}` would be parsed as a tag opening). MathJax reads
    textContent which decodes entities, so LaTeX `<` still renders correctly."""
    for key, value in saved.items():
        html_text = html_text.replace(key, html.escape(value, quote=False))
    return html_text


def _protect_bold(body: str) -> tuple[str, dict[str, str]]:
    """Replace `**X**` with placeholders to bypass CommonMark's strict
    flanking rule, which fails when adjacent chars are Unicode punctuation
    (e.g. CJK fullwidth quotes block bold from closing). Run AFTER math
    protection so we don't munge $ ... ** ... $ math accidentally."""
    saved: dict[str, str] = {}
    counter = [0]

    def stash(m: re.Match) -> str:
        key = f"BOLDPLACEHOLDER{counter[0]:04d}"
        counter[0] += 1
        saved[key] = m.group(1)
        return key

    return _BOLD_RE.sub(stash, body), saved


def _restore_bold(html_text: str, saved: dict[str, str]) -> str:
    """Replace each placeholder with <strong>HTML-escaped(content)</strong>.
    The inner content was raw markdown text — we lose nested inline formatting
    (e.g. links inside bold), an acceptable trade for fixing CJK bold."""
    for key, value in saved.items():
        html_text = html_text.replace(
            key, f"<strong>{html.escape(value, quote=False)}</strong>"
        )
    return html_text


def _rewrite_links(body_html: str,
                   current_ids: set[str],
                   all_tag_ids: dict[str, set[str]]) -> str:
    """Rewrite markdown's .md hrefs into HTML-friendly anchors / cross-page paths.

    Same-tag card link  '<id>.md'           → '#<id>'
    Cross-tag card link '../<tag>/<id>.md'  → '<tag>.html#<id>'
    External / fragment / absolute          left untouched.
    """
    def replace(m: re.Match) -> str:
        href = m.group(1)
        if href.startswith(("http://", "https://", "mailto:", "#", "/")):
            return m.group(0)
        # Same-tag bare filename
        if "/" not in href and href.endswith(".md"):
            cid = href[:-3]
            if cid in current_ids:
                return f'href="#{cid}"'
            # Same filename happens to live in another tag dir
            for tag, ids in all_tag_ids.items():
                if cid in ids:
                    return f'href="{tag}.html#{cid}"'
            return m.group(0)
        # Cross-tag relative path
        m2 = _CROSS_TAG_RE.match(href)
        if m2:
            tag, cid = m2.group(1), m2.group(2)
            if tag in all_tag_ids and cid in all_tag_ids[tag]:
                return f'href="{tag}.html#{cid}"'
        return m.group(0)
    return _HREF_RE.sub(replace, body_html)


def render_card_html(card: tuple[pathlib.Path, dict, str],
                     current_ids: set[str] | None = None,
                     all_tag_ids: dict[str, set[str]] | None = None) -> tuple[str, str]:
    path, fm, body = card
    cid = str(fm.get("id", path.stem))
    title = html.escape(str(fm.get("title", cid)))
    primary_tag = html.escape(str(fm.get("primary_tag", "")))
    source = html.escape(str(fm.get("source", "")))
    confidence = html.escape(str(fm.get("confidence", "")))
    tags = " ".join(f'<span class="tag">{html.escape(str(t))}</span>'
                    for t in (fm.get("tags") or []))
    body_safe, math_saved = _protect_math(body.strip())
    body_safe, bold_saved = _protect_bold(body_safe)
    body_html = md.render(body_safe)
    body_html = _restore_bold(body_html, bold_saved)
    body_html = _restore_math(body_html, math_saved)
    body_html = _inline_local_svgs(body_html, path.parent)
    if current_ids is not None and all_tag_ids is not None:
        body_html = _rewrite_links(body_html, current_ids, all_tag_ids)
    block = (
        f'<article class="card" id="{html.escape(cid)}">'
        f'<h2>{title}</h2>'
        f'<div class="meta">'
        f'<span class="tag">{primary_tag}</span> {tags} '
        f'· source: {source} · confidence: {confidence}'
        f'</div>'
        f'{body_html}'
        f'</article>'
    )
    return cid, block


def render_library_index(kb: pathlib.Path, template: str,
                         all_tag_ids: dict[str, set[str]]) -> str:
    """Build the library catalog page listing every tag as a card."""
    entries = []
    for tag in sorted(all_tag_ids):
        ids = all_tag_ids[tag]
        if not ids:
            continue
        # Pull first non-trivial paragraph from tag's README.md as blurb.
        blurb = ""
        readme = kb / tag / "README.md"
        if readme.exists():
            text = readme.read_text(encoding="utf-8")
            for para in text.split("\n\n"):
                p = para.strip()
                if not p or p.startswith("#") or p.startswith(">"):
                    continue
                # First plain paragraph
                blurb = p.replace("\n", " ").strip()[:240]
                break
        # Find newest card date in this tag
        newest = ""
        for md_path in (kb / tag).glob("*.md"):
            if md_path.name == "README.md":
                continue
            parsed = parse_card(md_path)
            if parsed:
                d = str(parsed[0].get("created", ""))
                if d > newest:
                    newest = d
        if blurb:
            # Escape HTML metachars first, then promote `**X**` → <strong>X</strong>
            # so blurb's bold markers don't leak as literal `**`.
            escaped = html.escape(blurb, quote=False)
            blurb_html = _BOLD_RE.sub(r"<strong>\1</strong>", escaped)
        else:
            blurb_html = "<em>(no README primer)</em>"
        entries.append(
            f'<a class="library-entry" href="{html.escape(tag)}.html">'
            f'<h3>{html.escape(tag)} <span class="count">({len(ids)} cards)</span></h3>'
            f'<p class="blurb">{blurb_html}</p>'
            f'<p class="meta">Last update: {html.escape(newest) or "—"}</p>'
            f'</a>'
        )
    catalog = (
        '<section class="library">'
        '<h1>Knowledge Base 知识库</h1>'
        f'<p class="lib-meta">{len(entries)} tags · '
        f'{sum(len(v) for v in all_tag_ids.values())} cards total</p>'
        + "\n".join(entries)
        + '</section>'
    )
    rendered = (template
                .replace("{{TAG}}", "library")
                .replace("{{COUNT}}", str(len(entries)))
                .replace("{{TOC}}", "")
                .replace("{{CARDS}}", catalog))
    scripts = MERMAID_SCRIPT + MATHJAX_SCRIPT
    if "</body>" in rendered:
        rendered = rendered.replace("</body>", scripts + "</body>", 1)
    else:
        rendered += scripts
    return rendered


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", required=True, type=pathlib.Path)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--template", required=True, type=pathlib.Path)
    args = ap.parse_args()

    template = args.template.read_text(encoding="utf-8")

    if args.tag == "library":
        all_tag_ids = build_tag_index(args.kb)
        out_dir = args.kb / "_render"
        out_dir.mkdir(exist_ok=True)
        out = out_dir / "index.html"
        out.write_text(render_library_index(args.kb, template, all_tag_ids),
                       encoding="utf-8")
        print(f"Wrote {out} ({len(all_tag_ids)} tags)")
        return 0

    cards = collect(args.kb, args.tag)
    if not cards:
        existing = sorted(p.name for p in args.kb.iterdir()
                          if p.is_dir() and not p.name.startswith(".") and p.name != "_render")
        print(f"ERROR: tag '{args.tag}' has no cards. Available tags: {existing}",
              file=sys.stderr)
        return 1

    all_tag_ids = build_tag_index(args.kb)
    if args.tag == "all":
        current_ids: set[str] = set().union(*all_tag_ids.values()) if all_tag_ids else set()
    else:
        current_ids = all_tag_ids.get(args.tag, set())

    toc_lines = []
    card_blocks = []
    for c in cards:
        anchor, block = render_card_html(c, current_ids, all_tag_ids)
        toc_lines.append(f'<a href="#{html.escape(anchor)}">{html.escape(str(c[1].get("title", anchor)))}</a>')
        card_blocks.append(block)

    primer_html = render_tag_readme(args.kb, args.tag, current_ids, all_tag_ids)
    back_link = '<nav class="library-back"><a href="index.html">← Library</a></nav>\n'
    page_heading = f'<h1>{html.escape(args.tag)} <span class="count">({len(cards)} cards)</span></h1>\n'
    cards_section = back_link + page_heading + primer_html + "\n".join(card_blocks)

    rendered = (template
                .replace("{{TAG}}", html.escape(args.tag))
                .replace("{{COUNT}}", str(len(cards)))
                .replace("{{TOC}}", "\n".join(toc_lines))
                .replace("{{CARDS}}", cards_section))

    # Inject mermaid.js + MathJax once per page.
    scripts = MERMAID_SCRIPT + MATHJAX_SCRIPT
    if "</body>" in rendered:
        rendered = rendered.replace("</body>", scripts + "</body>", 1)
    else:
        rendered += scripts

    out_dir = args.kb / "_render"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{args.tag}.html"
    out.write_text(rendered, encoding="utf-8")
    print(f"Wrote {out} ({len(cards)} cards)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
