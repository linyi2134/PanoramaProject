#!/usr/bin/env python3
"""按项目统一命名，将根目录 PDF 批量转为 plans/*_cad.png。

PDF 对照（2026-06）：
  1F-A.pdf … 5F-A.pdf     → plans/f1_a_cad.png … f5_a_cad.png
  1_2_5F-B.pdf            → plans/f1_b_cad.png, f2_b_cad.png, f5_b_cad.png
  3_4F-B.pdf              → plans/f3_b_cad.png, f4_b_cad.png

用法（在 PanoramaProject 目录）：
  python node_nav/scripts/export_all_cad_plans.py
  python node_nav/scripts/export_all_cad_plans.py --dpi 400
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).resolve().parent / "dwg_or_pdf_to_png.py"

# (源 PDF 相对 ROOT, 输出 PNG 相对 ROOT)
JOBS: list[tuple[str, str]] = [
    ("1F-A.pdf", "plans/f1_a_cad.png"),
    ("2F-A.pdf", "plans/f2_a_cad.png"),
    ("3F-A.pdf", "plans/f3_a_cad.png"),
    ("4F-A.pdf", "plans/f4_a_cad.png"),
    ("5F-A.pdf", "plans/f5_a_cad.png"),
    ("1_2_5F-B.pdf", "plans/f1_b_cad.png"),
    ("1_2_5F-B.pdf", "plans/f2_b_cad.png"),
    ("1_2_5F-B.pdf", "plans/f5_b_cad.png"),
    ("3_4F-B.pdf", "plans/f3_b_cad.png"),
    ("3_4F-B.pdf", "plans/f4_b_cad.png"),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dpi", type=int, default=400, help="PDF 渲染 DPI（默认 400）")
    args = parser.parse_args()

    done: dict[str, Path] = {}
    ok, fail = 0, 0

    for pdf_rel, out_rel in JOBS:
        pdf = ROOT / pdf_rel
        out = ROOT / out_rel
        if not pdf.is_file():
            print(f"跳过（缺 PDF）: {pdf_rel}", file=sys.stderr)
            fail += 1
            continue

        cache_key = f"{pdf_rel}|{args.dpi}"
        if cache_key in done:
            import shutil

            shutil.copy2(done[cache_key], out)
            print(f"复制 {out_rel} ← {done[cache_key].name}")
            ok += 1
            continue

        cmd = [
            sys.executable,
            str(SCRIPT),
            str(pdf),
            "-o",
            str(out),
            "--dpi",
            str(args.dpi),
        ]
        print(f"\n>>> {' '.join(cmd)}")
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode != 0:
            fail += 1
        else:
            done[cache_key] = out
            ok += 1

    print(f"\n完成: 成功 {ok}, 失败 {fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
