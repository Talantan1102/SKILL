"""Tests for render_html.py."""
import pathlib
import re
import subprocess
import sys

SCRIPT = pathlib.Path(__file__).parent.parent / "render_html.py"
TEMPLATE = pathlib.Path(__file__).parent.parent.parent / "templates" / "render-base.html"


def run(kb: pathlib.Path, tag: str, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--kb", str(kb), "--tag", tag,
         "--template", str(TEMPLATE), *extra],
        capture_output=True, text=True, encoding="utf-8",
    )


def test_renders_single_tag(kb_dir: pathlib.Path):
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    out = kb_dir / "_render" / "grpo.html"
    assert out.exists()
    html = out.read_text(encoding="utf-8")
    assert "GRPO 核心算法" in html
    assert "GRPO 的非对称 clip" in html


def test_renders_all_tag(kb_dir: pathlib.Path):
    res = run(kb_dir, "all")
    assert res.returncode == 0, res.stderr
    out = kb_dir / "_render" / "all.html"
    assert out.exists()
    html = out.read_text(encoding="utf-8")
    assert "GRPO 核心算法" in html
    assert "SGLang Context-Parallel" in html


def test_unknown_tag_errors_with_listing(kb_dir: pathlib.Path):
    res = run(kb_dir, "nonexistent-tag")
    assert res.returncode != 0
    msg = res.stderr + res.stdout
    assert "grpo" in msg and "sglang" in msg


def test_html_contains_card_count(kb_dir: pathlib.Path):
    run(kb_dir, "grpo")
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    assert re.search(r"\b2\s*cards?", html, re.IGNORECASE)


def test_render_dir_is_created(kb_dir: pathlib.Path):
    assert not (kb_dir / "_render").exists()
    run(kb_dir, "grpo")
    assert (kb_dir / "_render").exists() and (kb_dir / "_render").is_dir()


def test_intra_tag_md_links_rewritten_to_anchors(kb_dir: pathlib.Path):
    """Cards in the same tag should rewrite [X](OTHER-CARD-ID.md) → href="#OTHER-CARD-ID"."""
    import textwrap
    (kb_dir / "grpo" / "20260101-grpo-x.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-grpo-x
        title: GRPO x
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        See [the core](20260101-grpo-core.md) and [the clip](20260101-grpo-clip.md).
    """), encoding="utf-8")
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    # Old broken href must be gone, replaced by anchor
    assert 'href="20260101-grpo-core.md"' not in html
    assert 'href="20260101-grpo-clip.md"' not in html
    assert 'href="#20260101-grpo-core"' in html
    assert 'href="#20260101-grpo-clip"' in html


def test_cross_tag_md_links_rewritten_to_html_paths(kb_dir: pathlib.Path):
    """Cards linking to another tag's card should become href="../<tag>.html#<id>"."""
    import textwrap
    (kb_dir / "grpo" / "20260101-grpo-y.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-grpo-y
        title: GRPO y
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        See [sglang ref](../sglang/20260201-sglang-cp-overlap.md).
    """), encoding="utf-8")
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    assert 'href="../sglang/20260201-sglang-cp-overlap.md"' not in html
    # Different tag's card → cross-page link
    assert 'href="sglang.html#20260201-sglang-cp-overlap"' in html


def test_math_block_preserved_and_mathjax_injected(kb_dir: pathlib.Path):
    """LaTeX `$...$` content must survive markdown rendering, MathJax CDN injected."""
    import textwrap
    (kb_dir / "grpo" / "20260101-grpo-math.md").write_text(textwrap.dedent(r"""
        ---
        id: 20260101-grpo-math
        title: GRPO with math
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        Inline: $q \sim P_{sft}(Q)$.

        Block: $$\hat A_t = r_t - \bar r$$
    """).lstrip(), encoding="utf-8")
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    # The $...$ markers must survive (markdown-it-py shouldn't eat them)
    assert "P_{sft}" in html, "underscored subscript got stripped"
    assert r"\sim" in html or "&bsol;sim" in html, "LaTeX command stripped"
    # MathJax CDN script must be present
    assert "mathjax" in html.lower()
    # Inline + display math configs both supported
    assert "inlineMath" in html or "MathJax" in html


def test_cjk_bold_renders_as_strong(kb_dir: pathlib.Path):
    """`**X**` with Chinese punctuation inside must still produce <strong>X</strong>.

    CommonMark emphasis rule blocks flanking when adjacent to Unicode punctuation
    (e.g. fullwidth quote U+201D), causing literal `**` to leak into output.
    """
    import textwrap
    (kb_dir / "grpo" / "20260101-grpo-bold.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-grpo-bold
        title: GRPO with CJK bold
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        这个表对**做技术选型时怎么向上游汇报"为什么不用 X 用 Y"**很有用。

        差异不仅仅在 reward function,**还在 sampling strategy**(注意)。
    """), encoding="utf-8")
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    # Strong tags must appear
    assert "<strong>做技术选型时怎么向上游汇报" in html
    assert "<strong>还在 sampling strategy</strong>" in html
    # Literal ** must NOT leak through (outside pre/code)
    body_only = re.sub(r"<pre[^>]*>.*?</pre>", "", html, flags=re.DOTALL)
    body_only = re.sub(r"<code[^>]*>.*?</code>", "", body_only, flags=re.DOTALL)
    assert "**" not in body_only, "raw ** still leaks in non-code body"


def test_math_html_metachars_escaped(kb_dir: pathlib.Path):
    """`<`, `>`, `&` inside $..$ must be HTML-escaped on restore so the browser
    doesn't treat them as tag openings before MathJax runs."""
    import textwrap
    (kb_dir / "grpo" / "20260101-grpo-meta.md").write_text(textwrap.dedent(r"""
        ---
        id: 20260101-grpo-meta
        title: GRPO with HTML metachars in math
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        Inline trouble: $\rho = \pi_\theta(o_{i,<t})$ end.
    """).lstrip(), encoding="utf-8")
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    # Browser would gobble "<t)" as tag opening; the entity form must replace it.
    assert "o_{i,<t}" not in html, "raw `<` survived; browser will eat it"
    assert "o_{i,&lt;t}" in html, "math content not HTML-escaped"


def test_block_math_underscores_not_eaten_by_markdown(kb_dir: pathlib.Path):
    """`$$...\\sum_{i}^{G}...$$` must survive — markdown italic must not wrap on `_`."""
    import textwrap
    (kb_dir / "grpo" / "20260101-grpo-blockmath.md").write_text(textwrap.dedent(r"""
        ---
        id: 20260101-grpo-blockmath
        title: GRPO with block math
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        $$\mathcal{J}_{GRPO}(\theta) = \mathbb{E}\Big[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_i|}\Big]$$
    """).lstrip(), encoding="utf-8")
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    # If markdown ate the underscores it would emit <em>{GRPO}...\sum</em>{i=1}
    assert r"\mathcal{J}_{GRPO}" in html, "underscore-subscript got mangled"
    assert r"\sum_{i=1}^{G}" in html, "sum subscript got mangled"
    # No <em> tag inserted inside the math span
    body_after_math = html[html.find("$$"):]
    assert "<em>" not in body_after_math.split("$$")[1] if "$$" in body_after_math else True


def test_mermaid_theme_uses_paper_and_ink_palette(kb_dir: pathlib.Path):
    """Mermaid init must include themeVariables matching the library palette."""
    res = run(kb_dir, "grpo")
    assert res.returncode == 0
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    assert "themeVariables" in html
    # accent / paper colors from CSS should be passed to mermaid
    assert "#7a3b14" in html or "primaryBorderColor" in html


def test_local_svg_image_inlined_into_html(kb_dir: pathlib.Path):
    """`![alt](_assets/x.svg)` should be replaced with the SVG content inline so the
    rendered HTML is self-contained (no broken image links into _assets/)."""
    import textwrap
    assets_dir = kb_dir / "grpo" / "_assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / "tiny.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
        '<circle cx="5" cy="5" r="4" fill="#7a3b14"/></svg>',
        encoding="utf-8",
    )
    (kb_dir / "grpo" / "20260101-grpo-svg.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-grpo-svg
        title: GRPO with svg embed
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        Below is the diagram:

        ![GRPO loop](_assets/tiny.svg)
    """), encoding="utf-8")
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    # Old <img> tag with broken relative path must be gone
    assert 'src="_assets/tiny.svg"' not in html
    # Inline SVG content must be present
    assert '<circle cx="5" cy="5" r="4" fill="#7a3b14"/>' in html


def test_missing_local_svg_falls_back_to_img(kb_dir: pathlib.Path):
    """If the referenced SVG doesn't exist, leave the <img> tag — broken-link
    behaviour is the user's signal to generate the asset."""
    import textwrap
    (kb_dir / "grpo" / "20260101-grpo-noasset.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-grpo-noasset
        title: GRPO with missing asset
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        ![oops](_assets/does-not-exist.svg)
    """), encoding="utf-8")
    run(kb_dir, "grpo")
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    assert 'src="_assets/does-not-exist.svg"' in html


def test_external_links_untouched(kb_dir: pathlib.Path):
    import textwrap
    (kb_dir / "grpo" / "20260101-grpo-z.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-grpo-z
        title: GRPO z
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        See [paper](https://arxiv.org/abs/2402.03300) and [hf](http://huggingface.co/x.md).
    """), encoding="utf-8")
    run(kb_dir, "grpo")
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    assert 'href="https://arxiv.org/abs/2402.03300"' in html
    assert 'href="http://huggingface.co/x.md"' in html  # external .md untouched


def test_library_mode_writes_index_html_with_all_tags(kb_dir: pathlib.Path):
    """`--tag library` emits `_render/index.html` listing every tag as catalog entry."""
    res = run(kb_dir, "library")
    assert res.returncode == 0, res.stderr
    out = kb_dir / "_render" / "index.html"
    assert out.exists()
    html = out.read_text(encoding="utf-8")
    # Every tag must appear with link to its rendered HTML
    assert 'href="grpo.html"' in html
    assert 'href="sglang.html"' in html
    # Each catalog entry should show its card count
    assert "2" in html  # 2 grpo cards in fixture
    # Title indicates this is the library / index
    assert "<title>" in html
    assert "Knowledge Base" in html or "知识库" in html or "Library" in html


def test_library_blurb_renders_bold_inline(kb_dir: pathlib.Path):
    """A README's first paragraph used as catalog blurb should still render `**X**`
    as <strong>X</strong>, not leak literal `**` markers."""
    (kb_dir / "grpo" / "README.md").write_text(
        "# GRPO 导览\n\n"
        "GRPO 抛掉 **value network**,改用组内 baseline 当 advantage。\n",
        encoding="utf-8",
    )
    run(kb_dir, "library")
    html = (kb_dir / "_render" / "index.html").read_text(encoding="utf-8")
    assert "<strong>value network</strong>" in html
    assert "**value network**" not in html


def test_library_mode_uses_readme_first_paragraph_as_blurb(kb_dir: pathlib.Path):
    """Catalog should pull a brief description from each tag's README.md (if present)."""
    (kb_dir / "grpo" / "README.md").write_text(
        "# GRPO 导览\n\n"
        "> Reader-level: beginner.\n\n"
        "GRPO is a value-network-free RL method.\n",
        encoding="utf-8",
    )
    run(kb_dir, "library")
    html = (kb_dir / "_render" / "index.html").read_text(encoding="utf-8")
    assert "value-network-free" in html


def test_per_tag_html_has_back_to_library_link(kb_dir: pathlib.Path):
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    assert 'href="index.html"' in html


def test_library_mode_skips_back_link(kb_dir: pathlib.Path):
    run(kb_dir, "library")
    html = (kb_dir / "_render" / "index.html").read_text(encoding="utf-8")
    # The library page itself shouldn't say "back to library"
    assert "library-back" not in html or html.count('href="index.html"') == 0


def test_readme_md_links_rewritten_too(kb_dir: pathlib.Path):
    """Tag README's reading-order links are the most common breakage; must rewrite."""
    (kb_dir / "grpo" / "README.md").write_text(
        "# GRPO 导览\n\n"
        "1. [core card](20260101-grpo-core.md) — first read\n"
        "2. [clip card](20260101-grpo-clip.md) — second\n",
        encoding="utf-8",
    )
    run(kb_dir, "grpo")
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    assert 'href="20260101-grpo-core.md"' not in html
    assert 'href="#20260101-grpo-core"' in html
    assert 'href="#20260101-grpo-clip"' in html


def test_tag_readme_appears_at_top_of_rendered_html(kb_dir: pathlib.Path):
    """If kb/<tag>/README.md exists, render its body as a primer section before cards."""
    (kb_dir / "grpo" / "README.md").write_text(
        "# GRPO 导览\n\nThis is the primer text.\n\n```mermaid\ngraph TD\n  A --> B\n```\n",
        encoding="utf-8",
    )
    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    assert "GRPO 导览" in html
    assert "primer text" in html
    # README's mermaid block must also be rendered
    assert html.count('<pre class="mermaid">') >= 1
    # Primer must appear BEFORE the first <article class="card"> body.
    # (Card titles also appear in nav TOC at top; check the actual card section.)
    primer_pos = html.index('<section class="primer">')
    first_card_pos = html.index('<article class="card"')
    assert primer_pos < first_card_pos, "primer must precede first card body"


def test_mermaid_block_renders_as_pre_class_mermaid(kb_dir: pathlib.Path, tmp_path):
    """```mermaid``` fences become <pre class="mermaid"> + page injects mermaid CDN."""
    import textwrap
    (kb_dir / "grpo" / "20260101-grpo-mermaid.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-grpo-mermaid
        title: GRPO with diagram
        source: paper
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        ## arch

        ```mermaid
        graph TD
            A[policy] --> B[reward]
            B --> C[grpo update]
        ```
    """), encoding="utf-8")

    res = run(kb_dir, "grpo")
    assert res.returncode == 0, res.stderr
    html = (kb_dir / "_render" / "grpo.html").read_text(encoding="utf-8")
    assert '<pre class="mermaid">' in html
    assert "graph TD" in html
    assert "A[policy] --&gt; B[reward]" in html or "A[policy] --> B[reward]" in html
    assert "mermaid.esm.min.mjs" in html
    # Make sure non-mermaid fences keep being treated as code blocks.
    assert "language-mermaid" not in html  # we redirect mermaid out of generic path
