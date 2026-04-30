#!/usr/bin/env python3
"""Convert an .excalidraw JSON file to a clean SVG.

Drops the rough.js hand-drawn feel (would need a rough.js renderer),
keeps geometry / colors / labels. Output is a self-contained <svg> that
can be inlined in HTML or saved to disk.

Usage:
    python excalidraw_to_svg.py <input.excalidraw> [<output.svg>]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from html import escape

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def _bbox(elements):
    xs, ys, xe, ye = [], [], [], []
    for el in elements:
        if el.get("isDeleted"):
            continue
        if el["type"] == "arrow":
            base_x, base_y = el["x"], el["y"]
            for px, py in el.get("points", [[0, 0]]):
                xs.append(base_x + px)
                ys.append(base_y + py)
                xe.append(base_x + px)
                ye.append(base_y + py)
            continue
        x, y = el["x"], el["y"]
        w, h = el.get("width", 0), el.get("height", 0)
        xs.append(x); ys.append(y)
        xe.append(x + w); ye.append(y + h)
    pad = 30
    return min(xs) - pad, min(ys) - pad, max(xe) + pad, max(ye) + pad


def _attr(stroke, fill, sw, dashed=False):
    parts = [f'stroke="{stroke}"', f'fill="{fill}"', f'stroke-width="{sw}"']
    if dashed:
        parts.append('stroke-dasharray="6 4"')
    parts.append('stroke-linejoin="round"')
    parts.append('stroke-linecap="round"')
    return " ".join(parts)


def _font(family_id):
    if family_id == 5:
        return "Excalifont, 'Comic Sans MS', cursive"
    if family_id == 1:
        return "'Virgil', 'Comic Sans MS', cursive"
    if family_id == 2:
        return "Helvetica, Arial, sans-serif"
    if family_id == 3:
        return "Cascadia, Consolas, 'Courier New', monospace"
    return "Excalifont, 'Comic Sans MS', cursive"


def _emit_rect(el):
    rx = 8 if (el.get("roundness") or {}).get("type") == 3 else 0
    sw = el.get("strokeWidth", 1)
    stroke = el.get("strokeColor", "#000000")
    fill = el.get("backgroundColor", "transparent") or "transparent"
    dashed = el.get("strokeStyle") == "dashed"
    return (
        f'<rect x="{el["x"]}" y="{el["y"]}" '
        f'width="{el["width"]}" height="{el["height"]}" '
        f'rx="{rx}" ry="{rx}" {_attr(stroke, fill, sw, dashed)} />'
    )


def _emit_ellipse(el):
    cx = el["x"] + el["width"] / 2
    cy = el["y"] + el["height"] / 2
    rx = el["width"] / 2
    ry = el["height"] / 2
    sw = el.get("strokeWidth", 1)
    stroke = el.get("strokeColor", "#000000")
    fill = el.get("backgroundColor", "transparent") or "transparent"
    dashed = el.get("strokeStyle") == "dashed"
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'{_attr(stroke, fill, sw, dashed)} />'
    )


def _emit_arrow(el):
    base_x, base_y = el["x"], el["y"]
    pts = el.get("points", [[0, 0]])
    abs_pts = [(base_x + px, base_y + py) for px, py in pts]
    sw = el.get("strokeWidth", 1)
    stroke = el.get("strokeColor", "#000000")
    dashed = el.get("strokeStyle") == "dashed"

    poly_pts = " ".join(f"{x},{y}" for x, y in abs_pts)
    parts = [
        f'<polyline points="{poly_pts}" fill="none" '
        f'{_attr(stroke, "none", sw, dashed)} marker-end="url(#arrowhead)" />'
    ]
    return "\n  ".join(parts)


def _emit_text(el):
    text = el.get("text", "")
    fs = el.get("fontSize", 16)
    family = _font(el.get("fontFamily", 5))
    color = el.get("strokeColor", "#000000")
    align = el.get("textAlign", "left")
    text_anchor = {"left": "start", "center": "middle", "right": "end"}.get(align, "start")
    if text_anchor == "middle":
        x = el["x"] + el["width"] / 2
    elif text_anchor == "end":
        x = el["x"] + el["width"]
    else:
        x = el["x"]
    lines = text.split("\n")
    line_h = fs * 1.25
    total_h = line_h * len(lines)
    y_start = el["y"] + (el.get("height", total_h) - total_h) / 2 + fs
    out = [f'<g font-family="{family}" font-size="{fs}" fill="{color}">']
    for i, line in enumerate(lines):
        out.append(
            f'  <text x="{x}" y="{y_start + i * line_h}" '
            f'text-anchor="{text_anchor}">{escape(line)}</text>'
        )
    out.append("</g>")
    return "\n  ".join(out)


def excalidraw_to_svg(doc: dict) -> str:
    elements = [e for e in doc.get("elements", []) if not e.get("isDeleted")]
    if not elements:
        return '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="40"></svg>'

    x0, y0, x1, y1 = _bbox(elements)
    width, height = x1 - x0, y1 - y0
    bg = doc.get("appState", {}).get("viewBackgroundColor", "#ffffff")

    # Render layer order: rectangles/ellipses, arrows, then text on top.
    shapes, arrows, texts = [], [], []
    for el in elements:
        if el["type"] == "rectangle":
            shapes.append(_emit_rect(el))
        elif el["type"] == "ellipse":
            shapes.append(_emit_ellipse(el))
        elif el["type"] == "arrow":
            arrows.append(_emit_arrow(el))
        elif el["type"] == "text":
            texts.append(_emit_text(el))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{x0} {y0} {width} {height}" '
        f'width="100%" preserveAspectRatio="xMidYMid meet">',
        '  <defs>',
        '    <marker id="arrowhead" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto-start-reverse">',
        '      <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke" />',
        '    </marker>',
        '  </defs>',
        f'  <rect x="{x0}" y="{y0}" width="{width}" height="{height}" '
        f'fill="{bg}" stroke="none" />',
    ]
    parts.extend(f"  {s}" for s in shapes)
    parts.extend(f"  {a}" for a in arrows)
    parts.extend(f"  {t}" for t in texts)
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=pathlib.Path)
    ap.add_argument("output", nargs="?", type=pathlib.Path, default=None)
    args = ap.parse_args()

    if not args.input.exists():
        print(f"ERROR: {args.input} not found", file=sys.stderr)
        return 1

    doc = json.loads(args.input.read_text(encoding="utf-8"))
    svg = excalidraw_to_svg(doc)
    out = args.output or args.input.with_suffix(".svg")
    out.write_text(svg, encoding="utf-8")
    print(f"wrote {out}: {len(svg)} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
