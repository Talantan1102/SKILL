"""Tests for reindex.py."""
import pathlib
import subprocess
import sys

SCRIPT = pathlib.Path(__file__).parent.parent / "reindex.py"


def test_reindex_writes_all_three_indexes(kb_dir: pathlib.Path):
    res = subprocess.run([sys.executable, str(SCRIPT), "--kb", str(kb_dir)],
                         capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 0, res.stderr
    assert (kb_dir / "INDEX.md").exists()
    assert (kb_dir / "INDEX-by-tag.md").exists()
    assert (kb_dir / "INDEX-by-date.md").exists()


def test_reindex_overwrites_stale_index(kb_dir: pathlib.Path):
    (kb_dir / "INDEX.md").write_text("STALE CONTENT", encoding="utf-8")
    subprocess.run([sys.executable, str(SCRIPT), "--kb", str(kb_dir)],
                   capture_output=True, text=True, encoding="utf-8")
    text = (kb_dir / "INDEX.md").read_text(encoding="utf-8")
    assert "STALE CONTENT" not in text
    assert "Knowledge Base Index" in text
