#!/usr/bin/env python3
"""将 B 座各层 CAD 底图与节点坐标统一为 B1F 尺寸（844×925）。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLANS = ROOT / "plans"
MAP_DATA = ROOT / "map_data"
GRAPH_DIR = ROOT / "node_nav" / "data"
ARCHIVE = PLANS / "_archive"

TARGET_W, TARGET_H = 844, 925

B_FLOORS: dict[int, tuple[int, int]] = {
    1: (844, 925),
    2: (844, 925),
    3: (1027, 1125),
    4: (795, 871),
    5: (844, 925),
}


def scale_coord(x: int | float, y: int | float, old_w: int, old_h: int) -> tuple[int, int]:
    return round(x * TARGET_W / old_w), round(y * TARGET_H / old_h)


def scale_graph(floor: int, old_w: int, old_h: int) -> int:
    path = GRAPH_DIR / f"f{floor}_b_graph.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    meta = data.setdefault("meta", {})
    meta["planWidth"] = TARGET_W
    meta["planHeight"] = TARGET_H
    note = meta.get("note", "")
    tag = f"已统一缩放到 B1F 尺寸 {TARGET_W}×{TARGET_H}（原 {old_w}×{old_h}）。"
    if tag not in note:
        meta["note"] = f"{note} {tag}".strip()
    count = 0
    for node in data["nodes"]:
        if "x_px" not in node or "y_px" not in node:
            continue
        node["x_px"], node["y_px"] = scale_coord(node["x_px"], node["y_px"], old_w, old_h)
        count += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return count


def scale_cad_pick(floor: int, old_w: int, old_h: int) -> int:
    path = MAP_DATA / f"cad_pick_f{floor}_b.json"
    if not path.exists():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    data["planWidth"] = TARGET_W
    data["planHeight"] = TARGET_H
    count = 0
    for nid, c in (data.get("coords") or {}).items():
        c["x_px"], c["y_px"] = scale_coord(c["x_px"], c["y_px"], old_w, old_h)
        count += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return count


def scale_png(floor: int, old_w: int, old_h: int) -> None:
    from PIL import Image

    src = PLANS / f"f{floor}_b_cad.png"
    if not src.exists():
        raise FileNotFoundError(src)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    backup = ARCHIVE / f"f{floor}_b_cad_{old_w}x{old_h}.png"
    if not backup.exists():
        img = Image.open(src)
        img.save(backup)
    Image.open(src).resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS).save(src)


def main() -> int:
    for floor, (old_w, old_h) in B_FLOORS.items():
        if old_w == TARGET_W and old_h == TARGET_H:
            print(f"B{floor}F: already {TARGET_W}×{TARGET_H}, skip")
            continue
        print(f"B{floor}F: {old_w}×{old_h} → {TARGET_W}×{TARGET_H}")
        scale_png(floor, old_w, old_h)
        n = scale_graph(floor, old_w, old_h)
        p = scale_cad_pick(floor, old_w, old_h)
        print(f"  PNG resized; graph {n} nodes; cad_pick {p} coords")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
