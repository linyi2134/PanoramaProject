"""
一次性整理 node_nav/data 下图谱 JSON：统一文件名、meta、字段名，并修正 id 引用。
运行（在 PanoramaProject 目录）: python node_nav/scripts/normalize_graphs.py
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
ARCHIVE = DATA / "_archive"

# 旧文件名 -> (新文件名, zone, floor)
FILE_MAP: list[tuple[str, str, str, int]] = [
    ("1F A座（1）(1).json", "f1_a_graph.json", "A", 1),
    ("1F B座(1).json", "f1_b_graph.json", "B", 1),
    ("2F-A座.json", "f2_a_graph.json", "A", 2),
    ("2F-B座(1).json", "f2_b_graph.json", "B", 2),
    ("3F-A座_graph(1).json", "f3_a_graph.json", "A", 3),
    ("3F_B座_graph(1).json", "f3_b_graph.json", "B", 3),
    ("4F-A座(1).json", "f4_a_graph.json", "A", 4),
    ("4F-B座(1).json", "f4_b_graph.json", "B", 4),
    ("5F-A座(1).json", "f5_a_graph.json", "A", 5),
    ("5F-B座(1).json", "f5_b_graph.json", "B", 5),
]

# 全局 id 替换（含空格、中文括号等）
GLOBAL_ID_REPLACEMENTS: dict[str, str] = {
    "washeoom": "washroom",
    "A-door": "a_door",
    "A_door": "a_door",
    "B door": "b_door",
    "AI room": "ai_room",
    "ws_floor": "fork_sw",
    "link_to_B": "link_to_b",
    "link_to_A": "link_to_a",
    "lab436_front(lab437_back)": "lab436_front_lab437_back",
    "room446（lab447_back）": "room446_lab447_back",
    "lab535(lab540)_back": "lab535_lab540_back",
    "room537(lab538_back)": "room537_lab538_back",
}


def sanitize_id(raw: str) -> str:
    s = raw.strip()
    if s in GLOBAL_ID_REPLACEMENTS:
        s = GLOBAL_ID_REPLACEMENTS[s]
    s = s.replace("（", "(").replace("）", ")")
    s = re.sub(r"[()（）]", "_", s)
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_").lower()
    return s or "node_unknown"


def apply_id_map(obj: dict, id_map: dict[str, str]) -> None:
    for n in obj.get("nodes", []):
        old = n["id"]
        new = id_map.get(old, sanitize_id(old))
        if old != new:
            id_map[old] = new
        n["id"] = new
    for e in obj.get("edges", []):
        e["from"] = id_map.get(e["from"], sanitize_id(e["from"]))
        e["to"] = id_map.get(e["to"], sanitize_id(e["to"]))
    for f in obj.get("facilities", []):
        if "nodeId" in f:
            f["nodeId"] = id_map.get(f["nodeId"], sanitize_id(f["nodeId"]))


def patch_graph(data: dict, zone: str, floor: int) -> dict:
    desc = data.pop("explain", None) or data.pop("description", "")
    finished = data.pop("isfinish", data.pop("isFinished", False))
    meta = data.get("meta") or {}
    meta["building"] = meta.get("building") or meta.pop("area", "B7")
    meta.pop("area", None)
    meta["floor"] = floor
    meta["zone"] = zone
    meta["units"] = meta.pop("units", None) or meta.pop("unit", "meter")
    meta.setdefault(
        "note",
        "边权与连通性请按实地核对；x_px/y_px 可在节点上后续补充供地图 UI 使用。",
    )

    data["description"] = desc or f"B7 · {floor}F · {zone}座"
    data["isFinished"] = bool(finished)
    data["meta"] = meta

    id_map: dict[str, str] = dict(GLOBAL_ID_REPLACEMENTS)
    apply_id_map(data, id_map)

    # 各层专项修补
    if floor == 1 and zone == "A":
        for n in data["nodes"]:
            if n["id"] == "washroom" and n.get("label") == "洗手间":
                pass
    if floor == 2 and zone == "A":
        for e in data.get("edges", []):
            if e.get("from") == "washroom" and e.get("to") == "link_to_b":
                e["from"] = "washroom_nw"
    if floor == 3 and zone == "A":
        for n in data["nodes"]:
            if n.get("role") == "corridor" and n.get("floor") == 1:
                n["floor"] = 3
        has_hub = any(n["id"] == "corridor_3f" for n in data["nodes"])
        if not has_hub:
            data["nodes"].append(
                {
                    "id": "corridor_3f",
                    "label": "三层走廊中枢（待对齐平面图坐标）",
                    "floor": 3,
                    "role": "corridor",
                }
            )
            data["edges"].append({"from": "corridor_3f", "to": "fork_sw", "weight": 1})
    if floor == 4 and zone == "A":
        for n in data["nodes"]:
            if n["id"] == "water":
                n["floor"] = 4

    return data


def load_lenient(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    # 修复漏逗号：} 换行后直接 { "from"
    text = re.sub(r"\}\s*\n\s*(\{\s*\"from\")", r"},\n        \1", text)
    return json.loads(text)


def main() -> None:
    ARCHIVE.mkdir(exist_ok=True)
    index: list[dict] = []

    for old_name, new_name, zone, floor in FILE_MAP:
        new_path = DATA / new_name
        old_path = DATA / old_name
        if not old_path.exists():
            archived = ARCHIVE / old_name
            if new_path.exists():
                print("skip already:", new_name)
                continue
            if archived.exists():
                old_path = archived
            else:
                print("skip missing:", old_name)
                continue
        raw = load_lenient(old_path)
        normalized = patch_graph(raw, zone, floor)
        out_path = DATA / new_name
        ordered = {
            "description": normalized["description"],
            "isFinished": normalized["isFinished"],
            "meta": normalized["meta"],
            "nodes": normalized["nodes"],
            "edges": normalized["edges"],
            "facilities": normalized.get("facilities", []),
        }
        out_path.write_text(
            json.dumps(ordered, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if old_path.parent == DATA:
            shutil.move(str(old_path), str(ARCHIVE / old_name))
        index.append(
            {
                "file": new_name,
                "building": normalized["meta"]["building"],
                "floor": floor,
                "zone": zone,
                "description": normalized["description"],
                "isFinished": normalized["isFinished"],
                "nodeCount": len(normalized.get("nodes", [])),
                "edgeCount": len(normalized.get("edges", [])),
            }
        )
        print("wrote", new_name, "from", old_name)

    for legacy in ("b1_b_zone_graph.json", "building-graph.json"):
        p = DATA / legacy
        if p.exists():
            shutil.move(str(p), str(ARCHIVE / legacy))
            print("archived", legacy)

    # 补全已生成但未在本次循环中的图
    seen = {e["file"] for e in index}
    for p in sorted(DATA.glob("f*_graph.json")):
        if p.name in seen:
            continue
        g = json.loads(p.read_text(encoding="utf-8"))
        m = g.get("meta", {})
        index.append(
            {
                "file": p.name,
                "building": m.get("building", "B7"),
                "floor": m.get("floor", 0),
                "zone": m.get("zone", "?"),
                "description": g.get("description", ""),
                "isFinished": g.get("isFinished", False),
                "nodeCount": len(g.get("nodes", [])),
                "edgeCount": len(g.get("edges", [])),
            }
        )

    (DATA / "index.json").write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "naming": "f{floor}_{zone}_graph.json，zone 为 a|b（小写）",
                "graphs": sorted(index, key=lambda x: (x["floor"], x["zone"])),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("wrote index.json")


if __name__ == "__main__":
    main()
