#!/usr/bin/env python3
"""Batch recompress equirectangular panoramas (scheme A: JPEG quality + optional downscale).

Backs up originals to backup/panoramas_original/ before overwriting panoramas/*.jpg.
Requires Pillow: pip install pillow
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PANORAMAS = ROOT / "panoramas"
BACKUP = ROOT / "backup" / "panoramas_original"


def compress_one(src: Path, max_width: int, quality: int) -> tuple[int, int, tuple[int, int], tuple[int, int]]:
    before = src.stat().st_size
    with Image.open(src) as im:
        im = im.convert("RGB")
        orig_size = im.size
        w, h = im.size
        if w > max_width:
            nh = round(h * max_width / w)
            im = im.resize((max_width, nh), Image.Resampling.LANCZOS)
        tmp = src.with_suffix(".jpg.tmp")
        im.save(tmp, "JPEG", quality=quality, optimize=True, progressive=True)
        after = tmp.stat().st_size
        tmp.replace(src)
        return before, after, orig_size, im.size


def main() -> int:
    parser = argparse.ArgumentParser(description="Recompress panoramas/*.jpg in place.")
    parser.add_argument("--max-width", type=int, default=3000, help="Downscale if wider (default 3000)")
    parser.add_argument("--quality", type=int, default=80, help="JPEG quality 1-95 (default 80)")
    parser.add_argument("--dry-run", action="store_true", help="Estimate only, do not write")
    parser.add_argument("--no-backup", action="store_true", help="Skip copying originals to backup/")
    args = parser.parse_args()

    if not PANORAMAS.is_dir():
        print(f"Missing folder: {PANORAMAS}", file=sys.stderr)
        return 1

    files = sorted(p for p in PANORAMAS.glob("*.jpg") if p.stat().st_size > 1000)
    if not files:
        print("No panorama JPGs found.", file=sys.stderr)
        return 1

    print(f"Found {len(files)} panoramas in {PANORAMAS}")
    print(f"Settings: max_width={args.max_width}, quality={args.quality}")

    if args.dry_run:
        import io

        total_before = total_after = 0
        for p in files:
            before = p.stat().st_size
            with Image.open(p) as im:
                im = im.convert("RGB")
                w, h = im.size
                if w > args.max_width:
                    nh = round(h * args.max_width / w)
                    im = im.resize((args.max_width, nh), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=args.quality, optimize=True, progressive=True)
                after = buf.tell()
            total_before += before
            total_after += after
            print(f"  {p.name}: {before/1024/1024:.2f} MB -> {after/1024/1024:.2f} MB")
        pct = 100 * (1 - total_after / total_before) if total_before else 0
        print(f"Total: {total_before/1024/1024:.1f} MB -> {total_after/1024/1024:.1f} MB ({pct:.0f}% saved)")
        return 0

    if not args.no_backup:
        BACKUP.mkdir(parents=True, exist_ok=True)
        for p in files:
            dest = BACKUP / p.name
            if not dest.exists():
                shutil.copy2(p, dest)
        print(f"Backup: {BACKUP} ({len(files)} files)")

    total_before = total_after = 0
    for p in files:
        before, after, orig, new = compress_one(p, args.max_width, args.quality)
        total_before += before
        total_after += after
        dim = f"{orig[0]}x{orig[1]}"
        if orig != new:
            dim += f" -> {new[0]}x{new[1]}"
        print(f"  {p.name}: {before/1024/1024:.2f} MB -> {after/1024/1024:.2f} MB ({dim})")

    pct = 100 * (1 - total_after / total_before) if total_before else 0
    print(f"Done. {total_before/1024/1024:.1f} MB -> {total_after/1024/1024:.1f} MB ({pct:.0f}% saved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
