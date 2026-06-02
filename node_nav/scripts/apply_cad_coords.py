#!/usr/bin/env python3
"""将 tools/pick-coords.html 导出的 cad_pick JSON 写入 *_graph.json。

用法（在 PanoramaProject 目录）：
  python node_nav/scripts/apply_cad_coords.py map_data/cad_pick_f1_b.json
  python node_nav/scripts/apply_cad_coords.py map_data/cad_pick_f2_b.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH_DIR = ROOT / "node_nav" / "data"
MAP_DATA = ROOT / "map_data"

CAD_NOTE = "坐标基于 CAD 底图（tools/pick-coords.html 标注）。"
OLD_NOTE = "坐标基于示意 PNG 760×520（map.html FLOORS），CAD 底图待替换。"


def load_pick(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def graph_path_from_pick(pick: dict, arg_graph: Path | None) -> Path:
    if arg_graph:
        return arg_graph.resolve()
    gf = pick.get("graphFile")
    if gf:
        p = ROOT / gf
        if p.is_file():
            return p
    floor = int(pick["floor"])
    zone = pick.get("zone", "b").lower()
    return GRAPH_DIR / f"f{floor}_{zone}_graph.json"


def apply(pick_path: Path, graph_path: Path | None = None) -> None:
    pick = load_pick(pick_path)
    coords = pick.get("coords") or {}
    if not coords:
        raise RuntimeError("cad_pick 中 coords 为空")

    gpath = graph_path_from_pick(pick, graph_path)
    graph = json.loads(gpath.read_text(encoding="utf-8"))

    meta = graph.setdefault("meta", {})
    if pick.get("planImage"):
        meta["planImage"] = pick["planImage"]
    if pick.get("planWidth"):
        meta["planWidth"] = int(pick["planWidth"])
    if pick.get("planHeight"):
        meta["planHeight"] = int(pick["planHeight"])

    note = meta.get("note", "")
    if OLD_NOTE in note:
        note = note.replace(OLD_NOTE, "").strip()
    if CAD_NOTE not in note:
        meta["note"] = f"{note} {CAD_NOTE}".strip()

    missing = []
    for node in graph["nodes"]:
        nid = node["id"]
        if nid not in coords:
            missing.append(nid)
            continue
        c = coords[nid]
        node["x_px"] = int(c["x_px"])
        node["y_px"] = int(c["y_px"])

    if missing:
        raise RuntimeError(f"coords 未覆盖节点：{', '.join(missing)}")

    extra = set(coords) - {n["id"] for n in graph["nodes"]}
    if extra:
        print(f"警告: coords 中多余 id（已忽略）：{', '.join(sorted(extra))}")

    gpath.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"已写入 {len(coords)} 个节点 → {gpath.relative_to(ROOT)}\n"
        f"  planImage={meta.get('planImage')} "
        f"{meta.get('planWidth')}×{meta.get('planHeight')}"
    )


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "用法: python node_nav/scripts/apply_cad_coords.py "
            "map_data/cad_pick_f1_b.json [node_nav/data/f1_b_graph.json]",
            file=sys.stderr,
        )
        return 1

    pick_path = Path(sys.argv[1])
    if not pick_path.is_absolute():
        pick_path = (ROOT / pick_path).resolve()
    if not pick_path.is_file():
        pick_path = MAP_DATA / Path(sys.argv[1]).name
    if not pick_path.is_file():
        print(f"找不到: {sys.argv[1]}", file=sys.stderr)
        return 1

    graph_arg = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    apply(pick_path, graph_arg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
