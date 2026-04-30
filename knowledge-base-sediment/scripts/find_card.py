#!/usr/bin/env python3
"""Search KB cards by keyword, ranked title > tag > body. Output JSON.

Usage:
    python find_card.py --kb <path> --query <q> [--tag <t>]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import yaml

# Force stdout to UTF-8 so non-ASCII (e.g. Chinese) JSON output round-trips
# through subprocess pipes regardless of the Windows console codepage.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def parse_frontmatter(path: pathlib.Path) -> tuple[dict, str] | None:
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


def search(kb: pathlib.Path, query: str, tag_filter: str | None) -> list[dict]:
    q = query.lower()
    hits: list[tuple[int, dict]] = []
    for md in sorted(kb.glob("*/*.md")):
        if md.parent.name.startswith(".") or md.parent.name == "_render":
            continue
        parsed = parse_frontmatter(md)
        if not parsed:
            continue
        fm, body = parsed
        if tag_filter and fm.get("primary_tag") != tag_filter:
            continue
        title = str(fm.get("title", "")).lower()
        tags = [str(t).lower() for t in (fm.get("tags") or [])]
        body_l = body.lower()

        if q in title:
            match_type, rank = "title", 0
        elif any(q in t for t in tags):
            match_type, rank = "tag", 1
        elif q in body_l:
            match_type, rank = "body", 2
        else:
            continue

        match_line = ""
        for line in body.splitlines():
            if q in line.lower():
                match_line = line.strip()[:200]
                break

        hits.append((rank, {
            "id": str(fm.get("id", md.stem)),
            "path": md.relative_to(kb).as_posix(),
            "title": str(fm.get("title", "")),
            "primary_tag": str(fm.get("primary_tag", "")),
            "tags": list(fm.get("tags") or []),
            "match_type": match_type,
            "match_line": match_line,
        }))
    hits.sort(key=lambda x: x[0])
    return [h for _, h in hits[:10]]


def list_tags(kb: pathlib.Path) -> list[str]:
    return sorted(p.name for p in kb.iterdir()
                  if p.is_dir() and not p.name.startswith(".") and p.name != "_render")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", required=True, type=pathlib.Path)
    ap.add_argument("--query", required=True)
    ap.add_argument("--tag", default=None)
    args = ap.parse_args()
    if not args.kb.exists():
        print(json.dumps({"hits": [], "error": f"kb dir not found: {args.kb}"}))
        return 0
    hits = search(args.kb, args.query, args.tag)
    out = {"hits": hits}
    if not hits:
        out["available_tags"] = list_tags(args.kb)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
