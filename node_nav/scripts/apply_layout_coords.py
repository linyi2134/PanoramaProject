#!/usr/bin/env python3
"""将 map_data/id_map_*.json 中的坐标写入 node_nav/data/*_graph.json 的 x_px/y_px。"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP_HTML = ROOT / "map.html"
MAP_DATA = ROOT / "map_data"
GRAPH_DIR = ROOT / "node_nav" / "data"


def parse_backbone_coords(map_html: str, prefix: str) -> dict[str, dict[str, int]]:
    """从 map.html 的 bn() 提取骨干节点坐标（id 为 p+'jnw' 形式，需加前缀）。"""
    m = re.search(r"function bn\(f,p\)\{return\[([\s\S]*?)\];", map_html)
    if not m:
        raise RuntimeError("无法在 map.html 中找到 bn()")
    nodes: dict[str, dict[str, int]] = {}
    for suffix, x, y in re.findall(
        r"\{id:p\+'([^']+)'[^}]*?x:(\d+),\s*y:(\d+)", m.group(1)
    ):
        nodes[f"{prefix}{suffix}"] = {"x": int(x), "y": int(y)}
    return nodes


def parse_floor_room_coords(map_html: str, floor: int) -> dict[str, dict[str, int]]:
    """从 FLOORS 某层块提取显式 nodes 的 id/x/y。"""
    m = re.search(rf"{floor}:\{{title:'[^']*',[\s\S]*?nodes:\[\.\.\.bn\({floor},'f{floor}_'\),([\s\S]*?)\],", map_html)
    if not m:
        raise RuntimeError(f"无法在 map.html 中找到 FLOORS[{floor}]")
    nodes: dict[str, dict[str, int]] = {}
    for nid, x, y in re.findall(
        r"\{id:'([^']+)'[^}]*?x:(\d+),\s*y:(\d+)", m.group(1)
    ):
        nodes[nid] = {"x": int(x), "y": int(y)}
    return nodes


def parse_floors_coords(map_html: str, floor: int = 1) -> dict[str, dict[str, int]]:
    prefix = f"f{floor}_"
    coords = parse_backbone_coords(map_html, prefix)
    coords.update(parse_floor_room_coords(map_html, floor))
    return coords


def load_id_map(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_coords(id_map: dict, floors: dict[str, dict]) -> dict[str, tuple[int, int]]:
    out: dict[str, tuple[int, int]] = {}
    for entry in id_map["mappings"]:
        jid = entry["jsonId"]
        if "x_px" in entry and "y_px" in entry:
            out[jid] = (int(entry["x_px"]), int(entry["y_px"]))
            continue
        fid = entry.get("floorsId")
        if not fid or fid not in floors:
            raise KeyError(f"缺少坐标：jsonId={jid}, floorsId={fid}")
        out[jid] = (floors[fid]["x"], floors[fid]["y"])
    return out


def apply_to_graph(graph_path: Path, coords: dict[str, tuple[int, int]], id_map: dict) -> None:
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    meta = graph.setdefault("meta", {})
    meta["planImage"] = id_map.get("planImage", "plans/f1_b.png")
    meta["planWidth"] = id_map.get("planWidth", 760)
    meta["planHeight"] = id_map.get("planHeight", 520)
    note = meta.get("note", "")
    layout_note = "坐标基于示意 PNG 760×520（map.html FLOORS），CAD 底图待替换。"
    if layout_note not in note:
        meta["note"] = f"{note} {layout_note}".strip()

    missing = []
    for node in graph["nodes"]:
        cid = node["id"]
        if cid in coords:
            node["x_px"], node["y_px"] = coords[cid]
        else:
            missing.append(cid)

    if missing:
        raise RuntimeError(f"对照表未覆盖节点：{', '.join(missing)}")

    graph_path.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    id_map_name = sys.argv[1] if len(sys.argv) > 1 else "id_map_f1_b.json"
    graph_name = sys.argv[2] if len(sys.argv) > 2 else "f1_b_graph.json"

    id_map_path = MAP_DATA / id_map_name
    graph_path = GRAPH_DIR / graph_name

    id_map = load_id_map(id_map_path)
    id_map.setdefault("planImage", "plans/f1_b.png")
    html = MAP_HTML.read_text(encoding="utf-8")
    floor = int(id_map.get("floor", 1))
    floors = parse_floors_coords(html, floor)
    coords = resolve_coords(id_map, floors)
    apply_to_graph(graph_path, coords, id_map)

    print(f"已写入 {len(coords)} 个节点坐标 → {graph_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
