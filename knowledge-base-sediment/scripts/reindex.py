#!/usr/bin/env python3
"""强制从零重建所有 KB 索引(委托给 update_index.py)。"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

UPDATE = pathlib.Path(__file__).parent / "update_index.py"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", required=True, type=pathlib.Path)
    args = ap.parse_args()
    for name in ("INDEX.md", "INDEX-by-tag.md", "INDEX-by-date.md"):
        p = args.kb / name
        if p.exists():
            p.unlink()
    res = subprocess.run([sys.executable, str(UPDATE), "--kb", str(args.kb)])
    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
