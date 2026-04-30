"""Tests for migrate_links.py."""
from __future__ import annotations
import pathlib
import textwrap
from importlib import util as imputil


def _load():
    p = pathlib.Path(__file__).resolve().parent.parent / "migrate_links.py"
    spec = imputil.spec_from_file_location("migrate_links", p)
    mod = imputil.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


migrate_links = _load()


def _write(p, body):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(body), encoding="utf-8")


def test_migrate_legacy_list_of_str(tmp_path):
    card = tmp_path / "kb" / "grpo" / "card.md"
    _write(card, """\
        ---
        id: card
        title: T
        primary_tag: grpo
        created: 2026-04-29
        links:
          - 20260101-other
          - 20260102-another
        ---

        Body.
    """)
    rc = migrate_links.main(["--kb", str(tmp_path / "kb")])
    assert rc == 0
    text = card.read_text(encoding="utf-8")
    assert "- id: 20260101-other" in text
    assert "rel: see-also" in text
    assert "- id: 20260102-another" in text
    assert "Body." in text


def test_migrate_idempotent(tmp_path):
    card = tmp_path / "kb" / "grpo" / "card.md"
    _write(card, """\
        ---
        id: card
        title: T
        primary_tag: grpo
        created: 2026-04-29
        links:
          - 20260101-other
        ---

        Body.
    """)
    migrate_links.main(["--kb", str(tmp_path / "kb")])
    first = card.read_text(encoding="utf-8")
    migrate_links.main(["--kb", str(tmp_path / "kb")])
    second = card.read_text(encoding="utf-8")
    assert first == second


def test_migrate_skip_already_new(tmp_path):
    card = tmp_path / "kb" / "grpo" / "card.md"
    _write(card, """\
        ---
        id: card
        title: T
        primary_tag: grpo
        created: 2026-04-29
        links:
          - id: 20260101-other
            rel: see-also
        ---

        Body.
    """)
    before = card.read_text(encoding="utf-8")
    migrate_links.main(["--kb", str(tmp_path / "kb")])
    after = card.read_text(encoding="utf-8")
    assert before == after


def test_migrate_skip_empty_links(tmp_path):
    card = tmp_path / "kb" / "grpo" / "card.md"
    _write(card, """\
        ---
        id: card
        title: T
        primary_tag: grpo
        created: 2026-04-29
        links: []
        ---

        Body.
    """)
    before = card.read_text(encoding="utf-8")
    migrate_links.main(["--kb", str(tmp_path / "kb")])
    after = card.read_text(encoding="utf-8")
    assert before == after


def test_migrate_preserves_frontmatter_terminator(tmp_path):
    """The closing `---` must remain on its own line, not glued to the last link."""
    import yaml
    card = tmp_path / "kb" / "grpo" / "card.md"
    _write(card, """\
        ---
        id: card
        title: T
        primary_tag: grpo
        created: 2026-04-29
        links:
          - 20260101-other
          - 20260102-another
        ---

        Body.
    """)
    migrate_links.main(["--kb", str(tmp_path / "kb")])
    text = card.read_text(encoding="utf-8")
    # the closing --- must be on its own line
    assert "\n---\n" in text, f"closing --- not on own line: {text!r}"
    # frontmatter must still parse as YAML
    fm_text = text.split("---", 2)[1]
    fm = yaml.safe_load(fm_text)
    assert fm["links"] == [
        {"id": "20260101-other", "rel": "see-also"},
        {"id": "20260102-another", "rel": "see-also"},
    ]


def test_migrate_preserves_other_frontmatter(tmp_path):
    card = tmp_path / "kb" / "grpo" / "card.md"
    _write(card, """\
        ---
        id: card-x
        title: ABC and special things
        source: paper
        source_ref: D:\\papers\\A.pdf
        primary_tag: grpo
        tags: [grpo, ppo, a-b]
        created: 2026-04-29
        updated: 2026-04-29
        confidence: medium
        status: draft
        links:
          - 20260101-other
        ---

        Body with content.
    """)
    migrate_links.main(["--kb", str(tmp_path / "kb")])
    text = card.read_text(encoding="utf-8")
    assert "title: ABC and special things" in text
    assert "source_ref: D:\\papers\\A.pdf" in text
    assert "tags: [grpo, ppo, a-b]" in text
    assert "Body with content." in text
