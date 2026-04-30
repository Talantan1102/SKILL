"""Tests for update_index.py."""
import pathlib
import re
import subprocess
import sys

SCRIPT = pathlib.Path(__file__).parent.parent / "update_index.py"


def run(kb: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--kb", str(kb)],
        capture_output=True, text=True, encoding="utf-8",
    )


def test_creates_three_index_files(kb_dir: pathlib.Path):
    res = run(kb_dir)
    assert res.returncode == 0, res.stderr
    assert (kb_dir / "INDEX.md").exists()
    assert (kb_dir / "INDEX-by-tag.md").exists()
    assert (kb_dir / "INDEX-by-date.md").exists()


def test_index_md_has_total_count(kb_dir: pathlib.Path):
    run(kb_dir)
    text = (kb_dir / "INDEX.md").read_text(encoding="utf-8")
    assert "4 cards" in text
    assert "0 broken links" in text


def test_index_by_tag_groups_correctly(kb_dir: pathlib.Path):
    run(kb_dir)
    text = (kb_dir / "INDEX-by-tag.md").read_text(encoding="utf-8")
    assert "## grpo (2)" in text
    assert "## sglang (2)" in text
    assert "20260101-grpo-core" in text
    assert "20260201-sglang-cp-overlap" in text


def test_index_by_date_is_reverse_chronological(kb_dir: pathlib.Path):
    run(kb_dir)
    text = (kb_dir / "INDEX-by-date.md").read_text(encoding="utf-8")
    sglang_pos = text.index("20260201-sglang-cp-overlap")
    grpo_pos = text.index("20260101-grpo-core")
    assert sglang_pos < grpo_pos, "newer should appear before older"


def test_card_metadata_in_tag_index(kb_dir: pathlib.Path):
    run(kb_dir)
    text = (kb_dir / "INDEX-by-tag.md").read_text(encoding="utf-8")
    assert re.search(r"grpo-core.*?paper.*?conf:high", text, re.DOTALL) or \
           re.search(r"\[grpo-core.*paper.*high", text)


def test_broken_link_detection(kb_with_broken_link: pathlib.Path):
    res = run(kb_with_broken_link)
    assert res.returncode == 0
    text = (kb_with_broken_link / "INDEX.md").read_text(encoding="utf-8")
    assert "broken" in text.lower()
    assert "99999999-does-not-exist" in text


def test_bad_yaml_card_skipped_not_fatal(kb_with_bad_yaml: pathlib.Path):
    res = run(kb_with_bad_yaml)
    assert res.returncode == 0
    text = (kb_with_bad_yaml / "INDEX-by-tag.md").read_text(encoding="utf-8")
    assert "20260101-grpo-core" in text
    assert "20260201-sglang-cp-overlap" in text
    assert "20260101-grpo-clip" not in text
    assert "20260101-grpo-clip" in (res.stderr + res.stdout)


def test_empty_kb(tmp_path: pathlib.Path):
    kb = tmp_path / "empty-kb"
    kb.mkdir()
    res = run(kb)
    assert res.returncode == 0
    assert (kb / "INDEX.md").exists()
    assert "0 cards" in (kb / "INDEX.md").read_text(encoding="utf-8")


def test_structured_links_no_false_broken(kb_with_structured_links: pathlib.Path):
    """links: [{id, rel}] form must not be misread as broken.

    Only `20260101-missing` should be flagged broken; the two real cards
    that exist (card-a, card-b) must not appear as the broken target.
    """
    res = run(kb_with_structured_links)
    assert res.returncode == 0, res.stderr
    idx = (kb_with_structured_links / "INDEX.md").read_text(encoding="utf-8")
    assert "1 broken links" in idx, idx
    assert "broken: `20260101-missing`" in idx
    assert "broken: `20260101-card-a`" not in idx
    assert "broken: `20260101-card-b`" not in idx


def test_mixed_legacy_and_structured(kb_dir: pathlib.Path,
                                     kb_with_structured_links: pathlib.Path):
    """KB with both list-of-str (legacy) and list-of-dict (new) cards: INDEX still works."""
    import shutil
    src = kb_with_structured_links / "grpo" / "20260101-card-a.md"
    shutil.copy(src, kb_dir / "grpo" / "20260101-card-a.md")
    res = run(kb_dir)
    assert res.returncode == 0, res.stderr
    by_tag = (kb_dir / "INDEX-by-tag.md").read_text(encoding="utf-8")
    assert "20260101-card-a" in by_tag
    assert "20260101-grpo-core" in by_tag


def test_index_md_tag_names_are_clickable(kb_dir: pathlib.Path):
    """Tag overview list in INDEX.md should link to per-tag README."""
    res = run(kb_dir)
    assert res.returncode == 0, res.stderr
    idx = (kb_dir / "INDEX.md").read_text(encoding="utf-8")
    # Old plain-text form must be gone
    assert "- `grpo` (2 cards)" not in idx
    # New clickable form: link target is the per-tag README path
    assert "[grpo](grpo/README.md)" in idx
    assert "[sglang](sglang/README.md)" in idx


def test_readme_files_are_skipped(kb_dir: pathlib.Path):
    """Per-tag README.md is a navigation primer, not a card.
    Even when README has valid frontmatter, it must not be counted or indexed.
    """
    import textwrap
    (kb_dir / "grpo" / "README.md").write_text(textwrap.dedent("""\
        ---
        id: grpo-readme
        title: GRPO 导览
        source: code
        primary_tag: grpo
        tags: [grpo, readme]
        created: 2026-01-01
        confidence: medium
        status: draft
        links: []
        ---

        # GRPO 导览

        primer, not a card.
    """), encoding="utf-8")
    res = run(kb_dir)
    assert res.returncode == 0, res.stderr
    idx = (kb_dir / "INDEX.md").read_text(encoding="utf-8")
    assert "4 cards" in idx, f"README.md must not bump card count from 4: {idx}"
    by_tag = (kb_dir / "INDEX-by-tag.md").read_text(encoding="utf-8")
    assert "grpo-readme" not in by_tag
    assert "GRPO 导览" not in by_tag


def test_structured_broken_link_id_extracted(kb_with_structured_links: pathlib.Path):
    """Broken link reported as the .id string, not as the dict repr."""
    run(kb_with_structured_links)
    idx = (kb_with_structured_links / "INDEX.md").read_text(encoding="utf-8")
    assert "20260101-missing" in idx
    assert "{'id'" not in idx
    assert "{id:" not in idx
