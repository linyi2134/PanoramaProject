#!/usr/bin/env python3
"""将指定楼层 CAD 底图与节点坐标统一到参考层尺寸。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLANS = ROOT / "plans"
MAP_DATA = ROOT / "map_data"
GRAPH_DIR = ROOT / "node_nav" / "data"
ARCHIVE = PLANS / "_archive"

# (graph/cad 文件名前缀, 参考层, [(待缩放层, 原宽, 原高), ...])
JOBS: list[tuple[str, str, int, int, list[tuple[str, int, int]]]] = [
    (
        "link_f",
        "link_f1",
        205,
        624,
        [
            ("link_f2", 138, 407),
            ("link_f3", 138, 407),
            ("link_f4", 138, 407),
            ("link_f5", 138, 407),
        ],
    ),
    (
        "f",
        "f2_a",
        933,
        918,
        [
            ("f3_a", 603, 593),
            ("f4_a", 537, 529),
        ],
    ),
]


def scale_coord(x: int | float, y: int | float, old_w: int, old_h: int, tw: int, th: int) -> tuple[int, int]:
    return round(x * tw / old_w), round(y * th / old_h)


def scale_graph(name: str, old_w: int, old_h: int, tw: int, th: int) -> int:
    path = GRAPH_DIR / f"{name}_graph.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    meta = data.setdefault("meta", {})
    meta["planWidth"] = tw
    meta["planHeight"] = th
    note = meta.get("note", "")
    tag = f"已统一缩放到 {tw}×{th}（原 {old_w}×{old_h}）。"
    if tag not in note:
        meta["note"] = f"{note} {tag}".strip()
    count = 0
    for node in data["nodes"]:
        if "x_px" not in node or "y_px" not in node:
            continue
        node["x_px"], node["y_px"] = scale_coord(node["x_px"], node["y_px"], old_w, old_h, tw, th)
        count += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return count


def scale_cad_pick(name: str, old_w: int, old_h: int, tw: int, th: int) -> int:
    # link_f2 -> cad_pick_link_f2.json ; f3_a -> cad_pick_f3_a.json
    if name.startswith("link_f"):
        pick_name = f"cad_pick_{name}.json"
    else:
        pick_name = f"cad_pick_{name}.json"
    path = MAP_DATA / pick_name
    if not path.exists():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    data["planWidth"] = tw
    data["planHeight"] = th
    count = 0
    for c in (data.get("coords") or {}).values():
        c["x_px"], c["y_px"] = scale_coord(c["x_px"], c["y_px"], old_w, old_h, tw, th)
        count += 1
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return count


def scale_png(name: str, old_w: int, old_h: int, tw: int, th: int) -> None:
    from PIL import Image

    src = PLANS / f"{name}_cad.png"
    if not src.exists():
        raise FileNotFoundError(src)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    backup = ARCHIVE / f"{name}_cad_{old_w}x{old_h}.png"
    if not backup.exists():
        Image.open(src).save(backup)
    Image.open(src).resize((tw, th), Image.Resampling.LANCZOS).save(src)


def main() -> int:
    for _prefix, ref, tw, th, items in JOBS:
        print(f"参考 {ref}: {tw}×{th}")
        for name, old_w, old_h in items:
            if old_w == tw and old_h == th:
                print(f"  {name}: already {tw}×{th}, skip")
                continue
            print(f"  {name}: {old_w}×{old_h} → {tw}×{th}")
            scale_png(name, old_w, old_h, tw, th)
            n = scale_graph(name, old_w, old_h, tw, th)
            p = scale_cad_pick(name, old_w, old_h, tw, th)
            print(f"    PNG; graph {n} nodes; cad_pick {p} coords")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
