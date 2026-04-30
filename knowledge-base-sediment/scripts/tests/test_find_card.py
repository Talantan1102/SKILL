"""Tests for find_card.py."""
import json
import pathlib
import subprocess
import sys

SCRIPT = pathlib.Path(__file__).parent.parent / "find_card.py"


def run(kb: pathlib.Path, query: str, *extra: str) -> dict:
    res = subprocess.run(
        [sys.executable, str(SCRIPT), "--kb", str(kb), "--query", query, *extra],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


def test_title_hit_ranks_highest(kb_dir: pathlib.Path):
    out = run(kb_dir, "GRPO")
    assert out["hits"], "expected hits"
    assert out["hits"][0]["match_type"] == "title"


def test_tag_filter(kb_dir: pathlib.Path):
    out = run(kb_dir, "code", "--tag", "sglang")
    for h in out["hits"]:
        assert h["primary_tag"] == "sglang"


def test_zero_hits_returns_existing_tags(kb_dir: pathlib.Path):
    out = run(kb_dir, "completelynonexistentkeyword12345")
    assert out["hits"] == []
    assert "available_tags" in out
    assert set(out["available_tags"]) == {"grpo", "sglang"}


def test_body_hit_lowest_rank(kb_dir: pathlib.Path):
    out = run(kb_dir, "组内基线")
    assert out["hits"]
    assert out["hits"][0]["match_type"] == "body"
    assert out["hits"][0]["id"] == "20260101-grpo-core"


def test_max_10_hits(tmp_path: pathlib.Path):
    kb = tmp_path / "many-kb"
    (kb / "x").mkdir(parents=True)
    for i in range(15):
        (kb / "x" / f"20260101-foo-{i:02d}.md").write_text(f"""---
id: 20260101-foo-{i:02d}
title: foo card {i}
source: paper
source_ref: x
primary_tag: x
tags: [x]
created: 2026-01-01
updated: 2026-01-01
confidence: medium
status: draft
links: []
---
foo body
""", encoding="utf-8")
    out = run(kb, "foo")
    assert len(out["hits"]) == 10
