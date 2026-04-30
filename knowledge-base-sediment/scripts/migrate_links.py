#!/usr/bin/env python3
"""Migrate `links` frontmatter from list-of-str to list-of-dict {id, rel}.

In-place rewrite. Idempotent. Only modifies the `links:` block; other
frontmatter and body bytes are preserved verbatim.

Usage:
    python migrate_links.py --kb <path-to-kb>
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys


LIST_ITEM_STR_RE = re.compile(r"^\s*-\s+(\S+)\s*$")


def _is_already_new(block_lines: list[str]) -> bool:
    return any(("id:" in l) or l.strip().startswith("{id") for l in block_lines)


def _migrate_block(fm_text: str) -> tuple[str, str]:
    """Returns (new_fm_text, status).
    status ∈ {migrated, no-links, empty, already-new, unhandled}.
    """
    lines = fm_text.split("\n")

    start = None
    for i, line in enumerate(lines):
        if line.startswith("links:"):
            start = i
            break
    if start is None:
        return fm_text, "no-links"

    rest = lines[start][len("links:"):].strip()
    if rest:
        if rest in ("[]", "{}"):
            return fm_text, "empty"
        return fm_text, "unhandled"

    end = start
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line == "" or line.startswith(" ") or line.startswith("\t"):
            end = i
            continue
        break
    # Don't consume trailing empty lines — they belong to fm_text's trailing
    # newline, not to the links block. Without this trim, the closing `---`
    # gets glued to the last link.
    while end > start and lines[end] == "":
        end -= 1

    block_lines = [l for l in lines[start + 1:end + 1] if l.strip()]
    if not block_lines:
        return fm_text, "empty"

    if _is_already_new(block_lines):
        return fm_text, "already-new"

    new_block = ["links:"]
    for l in block_lines:
        m = LIST_ITEM_STR_RE.match(l)
        if not m:
            return fm_text, "unhandled"
        link_id = m.group(1)
        new_block.append(f"  - id: {link_id}")
        new_block.append(f"    rel: see-also")

    new_lines = lines[:start] + new_block + lines[end + 1:]
    return "\n".join(new_lines), "migrated"


def migrate_card(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return "no-frontmatter"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "no-frontmatter"
    fm_text = parts[1]
    body = parts[2]
    new_fm, status = _migrate_block(fm_text)
    if status == "migrated":
        path.write_text(f"---{new_fm}---{body}", encoding="utf-8")
    return status


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", required=True, type=pathlib.Path)
    args = ap.parse_args(argv)
    kb: pathlib.Path = args.kb
    if not kb.exists():
        print(f"ERROR: kb dir does not exist: {kb}", file=sys.stderr)
        return 2
    counts: dict[str, int] = {}
    for md in sorted(kb.glob("*/*.md")):
        if md.parent.name.startswith(".") or md.parent.name == "_render":
            continue
        st = migrate_card(md)
        counts[st] = counts.get(st, 0) + 1
    for k in sorted(counts):
        print(f"{k}: {counts[k]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
