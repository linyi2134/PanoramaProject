#!/usr/bin/env python3
"""从 map.html 同款 renderBuild() 几何导出示意 PNG（760×520）。

用法：
  python node_nav/scripts/export_map_png.py           # 默认 1F → plans/f1_b.png
  python node_nav/scripts/export_map_png.py --floor 3
  python node_nav/scripts/export_map_png.py --all     # 1F–5F → plans/f1_b.png … f5_b.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PLANS = ROOT / "plans"

W, H = 760, 520

BG = (8, 12, 18)
BUILDING = (22, 32, 46)
COURTYARD_C = (6, 10, 16)
CORRIDOR = (36, 53, 80)
STROKE = (37, 53, 80)
CORRIDOR_STROKE = (58, 85, 117)
TEXT_DIM = (42, 64, 96)
TEXT_YELLOW = (247, 247, 79)
OFFICE = (25, 34, 51)

BUILDINGS = [
    (20, 20, 195, 480),
    (215, 20, 520, 110),
    (640, 130, 100, 260),
    (215, 390, 520, 110),
]
COURTYARD = (215, 130, 425, 260)
CORRIDORS = [
    (100, 25, 26, 470),
    (20, 62, 640, 26),
    (634, 75, 26, 372),
    (20, 432, 640, 26),
]

FLOOR_TITLES = {
    1: "1F · 软件学院",
    2: "2F · 软件学院",
    3: "3F · 软件学院",
    4: "4F · 软件学院",
    5: "5F · 软件学院",
}


def _fonts():
    try:
        return ImageFont.truetype("segoeui.ttf", 12), ImageFont.truetype("segoeui.ttf", 11)
    except OSError:
        f = ImageFont.load_default()
        return f, f


def draw_floor_34_overlay(draw: ImageDraw.ImageDraw) -> None:
    """3F/4F 左翼缩窄 + 办公室带（与 map.html renderBuild 一致）。"""
    draw.rounded_rectangle([20, 20, 145, 500], radius=2, fill=BUILDING, outline=STROKE)
    draw.rectangle([145, 20, 215, 130], fill=COURTYARD_C)
    draw.rectangle([145, 390, 215, 500], fill=COURTYARD_C)
    draw.rectangle([145, 130, 215, 390], fill=OFFICE, outline=STROKE)
    draw.rounded_rectangle([195, 130, 215, 390], radius=1, fill=CORRIDOR, outline=CORRIDOR_STROKE)
    draw.rounded_rectangle([78, 25, 98, 495], radius=1, fill=CORRIDOR, outline=CORRIDOR_STROKE)


def render_floor_png(floor: int, out_path: Path) -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    font, font_sm = _fonts()

    for x, y, w, h in BUILDINGS:
        draw.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=BUILDING, outline=STROKE)

    cx, cy, cw, ch = COURTYARD
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=COURTYARD_C, outline=STROKE)

    for x, y, w, h in CORRIDORS:
        draw.rounded_rectangle([x, y, x + w, y + h], radius=1, fill=CORRIDOR, outline=CORRIDOR_STROKE)

    if floor in (3, 4):
        draw_floor_34_overlay(draw)

    title = FLOOR_TITLES.get(floor, f"{floor}F · 软件学院")
    draw.text((420, 268), "庭 院 上 空", fill=TEXT_DIM, anchor="mm", font=font)
    draw.text((22, 514), title, fill=TEXT_DIM, anchor="ls", font=font_sm)
    draw.text((750, 493), "→A区", fill=TEXT_YELLOW, anchor="mm", font=font_sm)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG")


def render_floor_svg(floor: int, out_path: Path) -> None:
    """导出与 map.html 同结构的 SVG 文件（仅建筑层，无节点）。"""
    title = FLOOR_TITLES.get(floor, f"{floor}F · 软件学院")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        f'<rect width="{W}" height="{H}" fill="#080c12"/>',
    ]
    for x, y, w, h in BUILDINGS:
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#16202e" stroke="#253550" stroke-width="1"/>'
        )
    cx, cy, cw, ch = COURTYARD
    parts.append(
        f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="#060a10" stroke="#253550" stroke-width="1"/>'
    )
    for x, y, w, h in CORRIDORS:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1" fill="#243550"/>')
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1" fill="none" stroke="#3a5575" stroke-width="0.8"/>'
        )
    if floor in (3, 4):
        parts.extend([
            '<rect x="20" y="20" width="125" height="480" rx="2" fill="#16202e" stroke="#253550" stroke-width="1"/>',
            '<rect x="145" y="20" width="70" height="110" fill="#060a10"/>',
            '<rect x="145" y="390" width="70" height="110" fill="#060a10"/>',
            '<rect x="145" y="130" width="70" height="260" fill="#192233" stroke="#253550" stroke-width="0.8"/>',
            '<rect x="195" y="130" width="20" height="260" rx="1" fill="#243550"/>',
            '<rect x="78" y="25" width="20" height="470" rx="1" fill="#243550"/>',
        ])
    parts.extend([
        f'<text x="420" y="268" text-anchor="middle" fill="#1a2d45" font-size="12" font-family="Segoe UI,sans-serif" letter-spacing="2">庭 院 上 空</text>',
        f'<text x="22" y="514" fill="#2a4060" font-size="11" font-family="Segoe UI,sans-serif" font-weight="bold">{title}</text>',
        f'<text x="750" y="493" text-anchor="middle" fill="#f7f74f" font-size="11" font-family="Segoe UI,sans-serif">→A区</text>',
        "</svg>",
    ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="导出 map.html 示意 SVG/PNG")
    parser.add_argument("--floor", type=int, default=1, help="楼层 1–5")
    parser.add_argument("--all", action="store_true", help="导出全部 1F–5F")
    parser.add_argument("--svg", action="store_true", help="同时导出 .svg")
    args = parser.parse_args()

    floors = range(1, 6) if args.all else [args.floor]
    for f in floors:
        png = PLANS / f"f{f}_b.png"
        render_floor_png(f, png)
        print(f"PNG  {png.relative_to(ROOT)}")
        if args.svg:
            svg = PLANS / f"f{f}_b.svg"
            render_floor_svg(f, svg)
            print(f"SVG  {svg.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
