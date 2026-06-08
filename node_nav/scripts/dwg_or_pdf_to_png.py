#!/usr/bin/env python3
"""将 DWG / 同名 PDF 转为 PNG（供 plans/ 底图使用）。

优先级：
  1. 若已安装 ODA File Converter → DWG 直接转 PNG
  2. 否则若存在同名 .pdf（如 1F(1).pdf）→ PyMuPDF 渲染并裁掉白边
  3. 否则报错并提示安装 ODA

用法：
  python node_nav/scripts/dwg_or_pdf_to_png.py "1F-A.pdf" -o plans/f1_a_cad.png --dpi 400
  python node_nav/scripts/export_all_cad_plans.py   # 批量，见 map_data/cad_sources.json
"""

from __future__ import annotations

import argparse
import glob
import shutil
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path

import fitz
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]

ODA_GLOB = [
    r"C:\Program Files\ODA\*\ODAFileConverter.exe",
    r"C:\Program Files (x86)\ODA\*\ODAFileConverter.exe",
]


def find_oda() -> Path | None:
    for pattern in ODA_GLOB:
        hits = glob.glob(pattern)
        if hits:
            return Path(sorted(hits)[-1])
    return None


def convert_dwg_oda(dwg: Path, out_png: Path, oda: Path) -> None:
    """ODA File Converter: 输入/输出均为文件夹。"""
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "in"
        outp = Path(tmp) / "out"
        inp.mkdir()
        outp.mkdir()
        shutil.copy2(dwg, inp / dwg.name)
        # ACAD2018 与 AC1032 DWG 兼容；输出 PNG
        cmd = [
            str(oda),
            str(inp),
            str(outp),
            "ACAD2018",
            "PNG",
            "0",
            "1",
            dwg.name,
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        pngs = list(outp.rglob("*.png"))
        if not pngs:
            raise RuntimeError("ODA 未生成 PNG 文件")
        out_png.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pngs[0], out_png)


def render_pdf(pdf: Path, dpi: int = 300) -> Image.Image:
    doc = fitz.open(pdf)
    page = doc[0]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    doc.close()
    return img


def crop_white(
    img: Image.Image,
    margin: int = 8,
    threshold: int = 250,
    min_component: int = 40,
) -> Image.Image:
    """裁掉四周白边；忽略孤立小噪点（如 PDF 角落脏点），避免裁切框被撑大。"""
    arr = np.array(img.convert("L"))
    ink = arr < threshold
    h, w = ink.shape
    visited = np.zeros_like(ink, dtype=bool)
    min_x, min_y, max_x, max_y = w, h, 0, 0
    found = False

    for sy in range(h):
        for sx in range(w):
            if not ink[sy, sx] or visited[sy, sx]:
                continue
            q: deque[tuple[int, int]] = deque([(sx, sy)])
            visited[sy, sx] = True
            comp: list[tuple[int, int]] = []
            while q:
                x, y = q.popleft()
                comp.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < w
                        and 0 <= ny < h
                        and ink[ny, nx]
                        and not visited[ny, nx]
                    ):
                        visited[ny, nx] = True
                        q.append((nx, ny))
            if len(comp) < min_component:
                continue
            found = True
            for x, y in comp:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    if not found:
        return img
    min_x = max(0, min_x - margin)
    min_y = max(0, min_y - margin)
    max_x = min(w - 1, max_x + margin)
    max_y = min(h - 1, max_y + margin)
    return img.crop((min_x, min_y, max_x + 1, max_y + 1))


def resize_to_width(img: Image.Image, width: int | None) -> Image.Image:
    if not width or img.width == width:
        return img
    ratio = width / img.width
    height = max(1, round(img.height * ratio))
    return img.resize((width, height), Image.Resampling.LANCZOS)


def resize_to_box(img: Image.Image, tw: int, th: int) -> Image.Image:
    """裁切后等比缩放，再居中裁剪到 tw×th（铺满画布、不拉伸变形）。"""
    if img.width == tw and img.height == th:
        return img
    scale = max(tw / img.width, th / img.height)
    nw = max(1, round(img.width * scale))
    nh = max(1, round(img.height * scale))
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - tw) // 2)
    top = max(0, (nh - th) // 2)
    return img.crop((left, top, left + tw, top + th))


def rotate_cw(img: Image.Image, degrees: int) -> Image.Image:
    """顺时针旋转 90/180/270 度。"""
    d = degrees % 360
    if d == 0:
        return img
    if d == 90:
        return img.transpose(Image.Transpose.ROTATE_270)
    if d == 180:
        return img.transpose(Image.Transpose.ROTATE_180)
    if d == 270:
        return img.transpose(Image.Transpose.ROTATE_90)
    raise ValueError(f"仅支持 0/90/180/270，收到 {degrees}")


def companion_pdf(dwg: Path) -> Path | None:
    pdf = dwg.with_suffix(".pdf")
    if pdf.is_file():
        return pdf
    # 如 3F(1).dwg ↔ 3F(3).pdf：同目录下按楼层前缀找 PDF
    import re

    m = re.match(r"(\d+F)", dwg.stem, re.I)
    if m:
        hits = sorted(dwg.parent.glob(f"{m.group(1)}*.pdf"))
        if hits:
            return hits[0]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="DWG/PDF → PNG")
    parser.add_argument("input", help="DWG 或 PDF 路径")
    parser.add_argument("-o", "--output", help="输出 PNG（默认 plans/<stem>.png）")
    parser.add_argument("--width", type=int, default=0, help="输出宽度像素，0=不指定（与 --target-size 二选一）")
    parser.add_argument(
        "--target-size",
        metavar="WxH",
        help="裁白边后等比缩放并居中裁剪到精确尺寸，如 587x709",
    )
    parser.add_argument("--dpi", type=int, default=300, help="PDF 渲染 DPI")
    parser.add_argument("--no-crop", action="store_true", help="不裁白边")
    parser.add_argument(
        "--rotate-cw",
        type=int,
        default=0,
        choices=[0, 90, 180, 270],
        help="顺时针旋转角度（如上方为东、要北在上则用 90）",
    )
    args = parser.parse_args()

    src = Path(args.input)
    if not src.is_absolute():
        src = (ROOT / src).resolve()
    if not src.is_file():
        print(f"找不到文件: {src}", file=sys.stderr)
        return 1

    out = Path(args.output) if args.output else ROOT / "plans" / f"{src.stem}.png"
    if not out.is_absolute():
        out = (ROOT / out).resolve()

    oda = find_oda()
    if src.suffix.lower() == ".dwg" and oda:
        print(f"使用 ODA: {oda}")
        convert_dwg_oda(src, out, oda)
        img = Image.open(out)
        if not args.no_crop:
            img = crop_white(img)
        if args.rotate_cw:
            img = rotate_cw(img, args.rotate_cw)
        if args.target_size:
            parts = args.target_size.lower().split("x")
            if len(parts) != 2:
                print("--target-size 格式应为 WxH，如 587x709", file=sys.stderr)
                return 1
            img = resize_to_box(img, int(parts[0]), int(parts[1]))
        else:
            img = resize_to_width(img, args.width or None)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, format="PNG")
        try:
            rel = out.relative_to(ROOT)
        except ValueError:
            rel = out
        print(f"已导出 {rel} ({img.width}x{img.height}) [ODA/DWG]")
        return 0

    pdf = src if src.suffix.lower() == ".pdf" else companion_pdf(src)
    if pdf:
        if src.suffix.lower() == ".dwg":
            print(f"未检测到 ODA，改用同名 PDF: {pdf.name}")
        img = render_pdf(pdf, dpi=args.dpi)
        if not args.no_crop:
            img = crop_white(img)
        if args.rotate_cw:
            img = rotate_cw(img, args.rotate_cw)
        if args.target_size:
            parts = args.target_size.lower().split("x")
            if len(parts) != 2:
                print("--target-size 格式应为 WxH，如 587x709", file=sys.stderr)
                return 1
            img = resize_to_box(img, int(parts[0]), int(parts[1]))
        else:
            img = resize_to_width(img, args.width or None)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, format="PNG")
        rot = f", 顺时针{args.rotate_cw}°" if args.rotate_cw else ""
        try:
            rel = out.relative_to(ROOT)
        except ValueError:
            rel = out
        print(f"已导出 {rel} ({img.width}x{img.height}) [PDF{rot}]")
        if src.suffix.lower() == ".dwg" and not oda:
            print(
                "提示: 安装免费 ODA File Converter 后可直转 DWG →",
                "winget install ODA.ODAFileConverter",
                file=sys.stderr,
            )
        return 0

    print(
        "无法转换: 需要同名 PDF 或安装 ODA File Converter\n"
        "  winget install ODA.ODAFileConverter",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
