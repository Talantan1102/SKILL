"""KB-sediment 脚本测试用的共享 pytest fixture。"""
import pathlib
import textwrap
import pytest


@pytest.fixture
def kb_dir(tmp_path: pathlib.Path) -> pathlib.Path:
    """A temporary KB directory with two tag dirs and four sample cards."""
    kb = tmp_path / "kb"
    (kb / "grpo").mkdir(parents=True)
    (kb / "sglang").mkdir(parents=True)

    (kb / "grpo" / "20260101-grpo-core.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-grpo-core
        title: GRPO 核心算法
        source: paper
        source_ref: D:\\papers\\GRPO.pdf
        primary_tag: grpo
        tags: [grpo, rlhf]
        created: 2026-01-01
        updated: 2026-01-01
        confidence: high
        status: reviewed
        links: [20260101-grpo-clip]
        ---

        ## 要解决什么问题
        减少 PPO 对 value network 的依赖。

        ## 核心方法
        组内基线代替 advantage estimation。
    """), encoding="utf-8")

    (kb / "grpo" / "20260101-grpo-clip.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-grpo-clip
        title: GRPO 的非对称 clip
        source: paper
        source_ref: D:\\papers\\GRPO.pdf
        primary_tag: grpo
        tags: [grpo, clipping]
        created: 2026-01-01
        updated: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        ## 要解决什么问题
        对正负 advantage 用不同 clip 上界。
    """), encoding="utf-8")

    (kb / "sglang" / "20260201-sglang-cp-overlap.md").write_text(textwrap.dedent("""\
        ---
        id: 20260201-sglang-cp-overlap
        title: SGLang Context-Parallel 通信/计算重叠
        source: code
        source_ref: D:\\repos\\sglang
        primary_tag: sglang
        tags: [sglang, cp, performance]
        created: 2026-02-01
        updated: 2026-02-01
        confidence: high
        status: draft
        links: [20260201-sglang-radixattention]
        ---

        ## 场景
        长序列推理时 CP 通信开销显著。
    """), encoding="utf-8")

    (kb / "sglang" / "20260201-sglang-radixattention.md").write_text(textwrap.dedent("""\
        ---
        id: 20260201-sglang-radixattention
        title: SGLang RadixAttention 前缀复用
        source: code
        source_ref: D:\\repos\\sglang
        primary_tag: sglang
        tags: [sglang, kvcache, attention]
        created: 2026-02-01
        updated: 2026-02-01
        confidence: high
        status: reviewed
        links: []
        ---

        ## 场景
        多请求共享前缀 KV cache。
    """), encoding="utf-8")

    return kb


@pytest.fixture
def kb_with_broken_link(kb_dir: pathlib.Path) -> pathlib.Path:
    """KB with one card linking to a non-existent id."""
    p = kb_dir / "grpo" / "20260101-grpo-core.md"
    text = p.read_text(encoding="utf-8")
    text = text.replace("links: [20260101-grpo-clip]",
                        "links: [20260101-grpo-clip, 99999999-does-not-exist]")
    p.write_text(text, encoding="utf-8")
    return kb_dir


@pytest.fixture
def kb_with_bad_yaml(kb_dir: pathlib.Path) -> pathlib.Path:
    """KB with one card whose frontmatter has a YAML syntax error."""
    p = kb_dir / "grpo" / "20260101-grpo-clip.md"
    text = p.read_text(encoding="utf-8")
    text = text.replace("tags: [grpo, clipping]", "tags: [grpo, clipping")  # missing ]
    p.write_text(text, encoding="utf-8")
    return kb_dir


@pytest.fixture
def kb_with_structured_links(tmp_path: pathlib.Path) -> pathlib.Path:
    """KB whose cards use the new structured `links: [{id, rel}]` format.

    Uses a `structured-kb` subdir so it can coexist with `kb_dir` in the same test.
    """
    kb = tmp_path / "structured-kb"
    grpo = kb / "grpo"
    grpo.mkdir(parents=True)

    (grpo / "20260101-card-a.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-card-a
        title: Card A
        source: paper
        source_ref: D:\\papers\\A.pdf
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        updated: 2026-01-01
        confidence: medium
        status: draft
        links:
          - id: 20260101-card-b
            rel: see-also
        ---

        ## 要解决什么问题
        Body of A.
    """), encoding="utf-8")

    (grpo / "20260101-card-b.md").write_text(textwrap.dedent("""\
        ---
        id: 20260101-card-b
        title: Card B
        source: paper
        source_ref: D:\\papers\\B.pdf
        primary_tag: grpo
        tags: [grpo]
        created: 2026-01-01
        updated: 2026-01-01
        confidence: medium
        status: draft
        links:
          - id: 20260101-card-a
            rel: see-also
          - id: 20260101-missing
            rel: see-also
        ---

        ## 要解决什么问题
        Body of B.
    """), encoding="utf-8")

    return kb
