#!/usr/bin/env python3
"""从 map.html 同款几何导出 1F B 区示意 PNG（760×520）。"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "plans" / "f1_b.png"

W, H = 760, 520

# 与 map.html renderBuild() 中 floor 1/2/5 一致
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

BG = (8, 12, 18)
BUILDING = (22, 32, 46)
COURTYARD_C = (6, 10, 16)
CORRIDOR = (36, 53, 80)
STROKE = (37, 53, 80)
TEXT_DIM = (42, 64, 96)
TEXT_TITLE = (42, 64, 96)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    for x, y, w, h in BUILDINGS:
        draw.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=BUILDING, outline=STROKE)

    cx, cy, cw, ch = COURTYARD
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=COURTYARD_C, outline=STROKE)

    for x, y, w, h in CORRIDORS:
        draw.rounded_rectangle([x, y, x + w, y + h], radius=1, fill=CORRIDOR, outline=(58, 85, 117))

    try:
        font = ImageFont.truetype("segoeui.ttf", 12)
        font_sm = ImageFont.truetype("segoeui.ttf", 11)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font

    draw.text((420, 268), "庭 院 上 空", fill=TEXT_DIM, anchor="mm", font=font)
    draw.text((22, 514), "1F · 软件学院 (B座示意)", fill=TEXT_TITLE, anchor="ls", font=font_sm)
    draw.text((750, 493), "→A区", fill=(247, 247, 79), anchor="mm", font=font_sm)

    img.save(OUT, format="PNG")
    print(f"已导出 {OUT.relative_to(ROOT)} ({W}×{H})")


if __name__ == "__main__":
    main()
