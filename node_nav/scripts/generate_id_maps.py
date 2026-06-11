#!/usr/bin/env python3
"""生成 map_data/id_map_*.json（搜索别名 + 节点对照文档）。

注意：各层 graph 已用 CAD 坐标，本脚本不会改写 *_graph.json。
      请勿对非示意层运行 apply_layout_coords.py。
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP_DATA = ROOT / "map_data"
GRAPH_DIR = ROOT / "node_nav" / "data"

# tab → (id_map 文件名, graph 文件名, zone, FLOORS key 或 None)
FLOOR_SPECS: list[tuple[int, str, str, str, int | None]] = [
    (1, "id_map_f1_b.json", "f1_b_graph.json", "b", 1),
    (2, "id_map_f2_b.json", "f2_b_graph.json", "b", 2),
    (3, "id_map_f3_b.json", "f3_b_graph.json", "b", 3),
    (4, "id_map_f4_b.json", "f4_b_graph.json", "b", 4),
    (5, "id_map_f5_b.json", "f5_b_graph.json", "b", 5),
    (8, "id_map_f1_a.json", "f1_a_graph.json", "a", 8),
    (9, "id_map_f2_a.json", "f2_a_graph.json", "a", 9),
    (10, "id_map_f3_a.json", "f3_a_graph.json", "a", 10),
    (11, "id_map_f4_a.json", "f4_a_graph.json", "a", 11),
    (12, "id_map_f5_a.json", "f5_a_graph.json", "a", 12),
    (14, "id_map_link_f1.json", "link_f1_graph.json", "link", None),
    (15, "id_map_link_f2.json", "link_f2_graph.json", "link", None),
    (16, "id_map_link_f3.json", "link_f3_graph.json", "link", None),
    (17, "id_map_link_f4.json", "link_f4_graph.json", "link", None),
    (18, "id_map_link_f5.json", "link_f5_graph.json", "link", None),
]

B_CORRIDOR_FLOORS: dict[str, str] = {
    "fork_nw": "jnw",
    "fork_ne": "jne",
    "fork_se": "jse",
    "fork_sw": "jsw",
    "washroom": "wash",
    "elevator": "stN",
    "stair_east": "stN",
    "stair_west": "stS",
    "weak": "util",
    "strong": "util",
    "weak_elec": "util",
    "strong_elec": "util",
    "elec_room": "util",
    "st_elec": "util",
    "water": "wash",
    "north_cctv": "monitor",
    "storage": "util",
}

B_END_FLOORS: dict[str, str] = {
    "end_sww": "lw_s",
    "end_nww": "lw_n",
    "end_nen": "top",
    "end_nee": "top",
    "end_see": "jrt_s",
    "end_sws": "bot",
    "end_nw": "lw_n",
    "end_ne": "top",
    "end_se": "jrt_s",
    "end_sw": "lw_s",
    "end_nwn": "lw_n",
}

# (floor, jsonId) → 补充 note（含房号别名）
B_NOTE_OVERRIDES: dict[tuple[int, str], str] = {
    (1, "mobile_room"): "133 移动计算与软件实验室",
    (1, "lab_door"): "133 实验室门",
    (1, "room137_front"): "137 微机室前门",
    (1, "room137_back"): "137 微机室后门",
    (1, "restarea"): "135 休息区",
    (1, "desk"): "136 座椅/值班室",
    (1, "teacher_room"): "教师办公室门",
    (1, "ai_room"): "131 人工智能与机器学习工作室",
    (2, "232"): "232 监控室门",
    (2, "237"): "237 监控室门",
    (3, "room335"): "335 教师办公室门",
    (3, "room332"): "332 服务器室门",
    (3, "director340"): "340 主任室门",
    (3, "expert341"): "341 专家室门",
    (3, "deputy347"): "347 副主任室门",
}

A_SCHEMATIC: dict[str, str] = {
    "fork_nw": "nw",
    "fork_ne": "ne",
    "fork_se": "se",
    "fork_sw": "sw",
    "link_to_b": "entry",
}

LINK_SCHEMATIC: dict[str, str] = {
    "entrance": "entry",
}

CORRIDOR_FLOOR = {14: 1, 15: 2, 16: 3, 17: 4, 18: 5}


def load_graph(name: str) -> dict:
    return json.loads((GRAPH_DIR / name).read_text(encoding="utf-8"))


def room_from_id(json_id: str) -> str | None:
    patterns = [
        r"^room[_]?(\d{2,4})",
        r"^lab(\d{2,4})",
        r"^office(\d{2,4})",
        r"^room(\d{2,4})",
        r"^(\d{2,4})$",
        r"^(\d{2,4})_",
        r"room_(\d{2,4})",
        r"conf(\d{2,4})",
        r"meeting(\d{2,4})",
        r"director(\d{2,4})",
        r"expert(\d{2,4})",
        r"deputy(\d{2,4})",
        r"teacher(\d{2,4})",
    ]
    for pat in patterns:
        m = re.search(pat, json_id, re.I)
        if m:
            return m.group(1)
    return None


def b_floors_room_id(floor: int, json_id: str) -> str | None:
    fp = f"f{floor}_"
    num = room_from_id(json_id)
    if num:
        return f"{fp}rm{num}"
    overrides = {
        (2, "232"): f"{fp}monitor_l",
        (2, "237"): f"{fp}jrt_n",
        (2, "230"): f"{fp}util",
        (3, "north_cctv"): f"{fp}monitor",
        (3, "storage"): f"{fp}rm349",
        (3, "weak_elec"): f"{fp}rm349",
        (3, "strong_elec"): f"{fp}rm349",
        (4, "weak_elec"): f"{fp}offices",
        (4, "strong_elec"): f"{fp}offices",
        (4, "room430"): f"{fp}link_a",
    }
    key = (floor, json_id)
    if key in overrides:
        return overrides[key]
    if json_id.startswith("teacher3"):
        return f"{fp}offices"
    if json_id.startswith("office4") and floor == 4:
        return f"{fp}offices"
    if json_id.startswith("lab53") or json_id.startswith("room53"):
        return f"{fp}rm{room_from_id(json_id) or ''}"
    return None


def build_note(floor: int, zone: str, json_id: str, label: str) -> str:
    override = B_NOTE_OVERRIDES.get((floor, json_id))
    if override:
        return override
    num = room_from_id(json_id)
    if num and num not in label:
        return f"{num} {label}"
    return label


def map_b_node(floor: int, node: dict) -> dict:
    jid = node["id"]
    label = node.get("label", jid)
    fp = f"f{floor}_"
    note = build_note(floor, "b", jid, label)
    entry: dict = {"jsonId": jid, "match": "inferred", "note": note}

    if jid == "link_to_a":
        fid = "link" if floor == 5 else "link_a"
        entry.update({"floorsId": f"{fp}{fid}", "match": "direct", "note": "连廊（接A区）"})
        return entry

    if jid in B_CORRIDOR_FLOORS:
        suffix = B_CORRIDOR_FLOORS[jid]
        entry.update({"floorsId": f"{fp}{suffix}", "match": "direct"})
        return entry

    if jid in B_END_FLOORS:
        entry.update({"floorsId": f"{fp}{B_END_FLOORS[jid]}", "match": "inferred"})
        return entry

    if jid in ("b_door", "en_door", "wn_door"):
        entry.update({"floorsId": f"{fp}lw_s" if jid == "b_door" else f"{fp}jne", "match": "inferred"})
        return entry

    if jid in ("desk", "restarea", "teacher_room", "ai_room", "mobile_room", "lab_door"):
        room_map = {
            "desk": "rm136",
            "restarea": "rm135",
            "teacher_room": "monitor_r",
            "ai_room": "rm131",
            "mobile_room": "rm133",
            "lab_door": "rm133",
        }
        entry.update({"floorsId": f"{fp}{room_map[jid]}", "match": "inferred"})
        return entry

    if jid.startswith("room137"):
        entry.update({"floorsId": f"{fp}rm138", "match": "direct" if jid.endswith("front") else "inferred"})
        return entry

    floors_room = b_floors_room_id(floor, jid)
    if floors_room:
        entry.update({"floorsId": floors_room, "match": "direct"})
        return entry

    if "x_px" in node and "y_px" in node:
        entry["x_px"] = node["x_px"]
        entry["y_px"] = node["y_px"]
    return entry


def map_a_node(floor: int, floors_key: int, node: dict) -> dict:
    jid = node["id"]
    label = node.get("label", jid)
    af = floors_key - 7
    note = build_note(af, "a", jid, label)
    entry: dict = {"jsonId": jid, "match": "cad", "note": note}

    if jid in A_SCHEMATIC:
        entry.update(
            {
                "floorsId": f"a{af}_{A_SCHEMATIC[jid]}",
                "match": "inferred",
                "note": f"{label} ↔ 示意图走廊",
            }
        )
    else:
        entry["floorsId"] = jid

    if "x_px" in node and "y_px" in node:
        entry["x_px"] = node["x_px"]
        entry["y_px"] = node["y_px"]
    return entry


def map_link_node(link_floor: int, node: dict) -> dict:
    jid = node["id"]
    label = node.get("label", jid)
    entry: dict = {
        "jsonId": jid,
        "floorsId": jid,
        "match": "cad",
        "note": label,
    }
    if jid in LINK_SCHEMATIC:
        entry["note"] = f"{label} ↔ 连廊示意图入口"
    if "x_px" in node and "y_px" in node:
        entry["x_px"] = node["x_px"]
        entry["y_px"] = node["y_px"]
    return entry


def zone_label(zone: str, floor: int, link_floor: int | None = None) -> str:
    if zone == "b":
        return f"{floor}F B座"
    if zone == "a":
        return f"{floor}F A座"
    return f"连廊{link_floor}F"


def build_id_map(tab: int, id_map_name: str, graph_name: str, zone: str, floors_key: int | None) -> dict:
    graph = load_graph(graph_name)
    meta = graph.get("meta", {})
    floor = int(meta.get("floor", tab if tab <= 5 else (tab - 7 if tab >= 8 else CORRIDOR_FLOOR.get(tab, 1))))
    link_floor = CORRIDOR_FLOOR.get(tab)

    mappings: list[dict] = []
    for node in graph["nodes"]:
        if zone == "b":
            mappings.append(map_b_node(floor, node))
        elif zone == "a":
            mappings.append(map_a_node(floor, floors_key or tab, node))
        else:
            mappings.append(map_link_node(link_floor or floor, node))

    zl = zone_label(zone, floor, link_floor)
    return {
        "description": f"{zl}：map.html tab {tab} ↔ {graph_name} 节点对照",
        "floor": tab,
        "planImage": meta.get("planImage", ""),
        "planWidth": meta.get("planWidth"),
        "planHeight": meta.get("planHeight"),
        "source": f"node_nav/data/{graph_name} + map.html tab {tab}",
        "note": "坐标取自 CAD graph（x_px/y_px）；仅用于搜索别名与文档对照，勿对 CAD 层运行 apply_layout_coords.py",
        "mappings": mappings,
        "floorsOnly": [],
    }


def main() -> int:
    MAP_DATA.mkdir(parents=True, exist_ok=True)
    for tab, id_map_name, graph_name, zone, floors_key in FLOOR_SPECS:
        doc = build_id_map(tab, id_map_name, graph_name, zone, floors_key)
        out = MAP_DATA / id_map_name
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)} ({len(doc['mappings'])} mappings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
