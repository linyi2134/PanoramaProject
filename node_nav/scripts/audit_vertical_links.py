#!/usr/bin/env python3
"""审计竖向/跨区边：分组、电梯楼梯是否串线、遗留 CROSS_CAMPUS 直连。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "node_nav" / "data"
SPEC = json.loads((ROOT / "map_data" / "cross_floor_links.json").read_text(encoding="utf-8"))

JSON_GRAPHS = {
    1: "f1_b_graph.json", 2: "f2_b_graph.json", 3: "f3_b_graph.json",
    4: "f4_b_graph.json", 5: "f5_b_graph.json",
    8: "f1_a_graph.json", 9: "f2_a_graph.json", 10: "f3_a_graph.json",
    11: "f4_a_graph.json", 12: "f5_a_graph.json",
    14: "link_f1_graph.json", 15: "link_f2_graph.json", 16: "link_f3_graph.json",
    17: "link_f4_graph.json", 18: "link_f5_graph.json",
}
CORRIDOR_FLOOR = {14: 1, 15: 2, 16: 3, 17: 4, 18: 5}


def nav_id(tab: int, node: str) -> str:
    if 1 <= tab <= 5:
        return f"b{tab}_{node}"
    lk = CORRIDOR_FLOOR.get(tab)
    if lk:
        return f"lk{lk}_{node}"
    if 8 <= tab <= 12:
        return f"a{tab - 7}_{node}"
    return node


def cross_edges() -> list[tuple[str, str, float, str]]:
    out: list[tuple[str, str, float, str]] = []
    w0 = float(SPEC.get("crossFloorWeight", 0))

    for node_id, vert in SPEC.get("bZone", {}).get("unifiedVertical", {}).items():
        tabs = vert.get("tabs", [])
        for i in range(len(tabs) - 1):
            a, b = nav_id(tabs[i], node_id), nav_id(tabs[i + 1], node_id)
            out.append((a, b, w0, f"B.{node_id}"))

    for node_id, vert in SPEC.get("aZone", {}).get("unifiedVertical", {}).items():
        tabs = vert.get("tabs", [])
        for i in range(len(tabs) - 1):
            a, b = nav_id(tabs[i], node_id), nav_id(tabs[i + 1], node_id)
            out.append((a, b, w0, f"A.{node_id}"))

    lc = SPEC.get("linkCorridor", {})
    tabs, nid = lc.get("tabs", []), lc.get("nodeId", "outdoor_stair")
    for i in range(len(tabs) - 1):
        a, b = nav_id(tabs[i], nid), nav_id(tabs[i + 1], nid)
        out.append((a, b, w0, "LINK.outdoor_stair"))

    for a, b in SPEC.get("campusCrossFloor", {}).get("pairs", []):
        out.append((a, b, w0, "LEGACY.campusCrossFloor"))

    zw = float(SPEC.get("zoneLinks", {}).get("crossZoneWeight", 15))
    for z in SPEC.get("zoneLinks", {}).get("pairs", []):
        out.append((nav_id(z["bTab"], z["bNode"]), nav_id(z["linkTab"], z["linkNode"]), zw, "zoneLinks"))
        out.append((nav_id(z["aTab"], z["aNode"]), nav_id(z["linkTab"], "link_to_a"), zw, "zoneLinks"))

    # map.html CROSS_CAMPUS legacy
    for f in range(1, 5):
        out.append((f"b{f}_link_to_a", f"a{f}_link_to_b", 30.0, "LEGACY.CROSS_CAMPUS"))
    out.append(("b5_link_to_a", "a5_link_to_b", 30.0, "LEGACY.CROSS_CAMPUS"))

    return out


def load_node_ids() -> set[str]:
    ids: set[str] = set()
    for tab, fn in JSON_GRAPHS.items():
        g = json.loads((DATA / fn).read_text(encoding="utf-8"))
        p = nav_id(tab, "")
        prefix = p  # e.g. b1_
        for n in g["nodes"]:
            ids.add(prefix + n["id"])
    return ids


def main() -> None:
    ids = load_node_ids()
    edges = cross_edges()

    print("=== 竖向分组（unifiedVertical / linkCorridor）===\n")
    groups: dict[str, list[tuple[str, str]]] = {}
    for a, b, w, tag in edges:
        if tag.startswith("LEGACY") or tag == "zoneLinks":
            continue
        groups.setdefault(tag, []).append((a, b))

    for tag, pairs in sorted(groups.items()):
        print(f"【{tag}】 {len(pairs) + 1} 层 / {len(pairs)} 条跨层边")
        for a, b in pairs:
            print(f"  {a} <-> {b}  (weight=0)")
        print()

    print("=== 遗留边是否进图（应跳过 campusCrossFloor；CROSS_CAMPUS 直连需关注）===\n")
    for a, b, w, tag in edges:
        if not tag.startswith("LEGACY"):
            continue
        ok_a, ok_b = a in ids, b in ids
        status = "ACTIVE (bad)" if ok_a and ok_b else "skipped (node missing)"
        print(f"{tag}: {a} <-> {b} w={w}  -> {status}")

    print("\n=== 同层 B 座：elevator ↔ stair_east 是否独立（不应与 stair_west 跨层串）===\n")
    for tab in range(1, 6):
        fn = JSON_GRAPHS[tab]
        g = json.loads((DATA / fn).read_text(encoding="utf-8"))
        elv, east, west = f"b{tab}_elevator", f"b{tab}_stair_east", f"b{tab}_stair_west"
        same_floor = []
        for e in g["edges"]:
            f, t = nav_id(tab, e["from"]), nav_id(tab, e["to"])
            if {f, t} == {elv, east}:
                same_floor.append(f"elevator<->stair_east w={e['weight']}")
            if {f, t} == {elv, west}:
                same_floor.append(f"WARN elevator<->stair_west w={e['weight']}")
            if {f, t} == {east, west}:
                same_floor.append(f"WARN stair_east<->stair_west w={e['weight']}")
        print(f"B{tab}F: {', '.join(same_floor) or '仅各自连走廊'}")

    print("\n=== A 座 stair_south / stair_small 分组层数 ===\n")
    for node_id, vert in SPEC.get("aZone", {}).get("unifiedVertical", {}).items():
        tabs = vert.get("tabs", [])
        floors = [f"A{t - 7}F" for t in tabs]
        print(f"{node_id}: tabs={tabs} -> {', '.join(floors)} ({len(tabs)} floors)")


if __name__ == "__main__":
    main()
