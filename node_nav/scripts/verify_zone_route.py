#!/usr/bin/env python3
"""验证 B ↔ 连廊 ↔ A 跨区算路（模拟 map.html 合并图 + zoneLinks）。"""
from __future__ import annotations

import json
import heapq
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "node_nav" / "data"
SPEC = ROOT / "map_data" / "cross_floor_links.json"

JSON_GRAPHS = {
    1: "f1_b_graph.json",
    2: "f2_b_graph.json",
    3: "f3_b_graph.json",
    4: "f4_b_graph.json",
    5: "f5_b_graph.json",
    8: "f1_a_graph.json",
    9: "f2_a_graph.json",
    10: "f3_a_graph.json",
    11: "f4_a_graph.json",
    12: "f5_a_graph.json",
    14: "link_f1_graph.json",
    15: "link_f2_graph.json",
    16: "link_f3_graph.json",
    17: "link_f4_graph.json",
    18: "link_f5_graph.json",
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


def load_graphs() -> dict:
    out = {}
    for tab, fn in JSON_GRAPHS.items():
        out[tab] = json.loads((DATA / fn).read_text(encoding="utf-8"))
    return out


def build_adj(graphs: dict, spec: dict) -> dict[str, list[tuple[str, float]]]:
    adj: dict[str, list[tuple[str, float]]] = {}

    def add(a: str, b: str, w: float) -> None:
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, []).append((a, w))

    for tab, g in graphs.items():
        for e in g["edges"]:
            a, b = nav_id(tab, e["from"]), nav_id(tab, e["to"])
            add(a, b, float(e["weight"]))

    w0 = float(spec.get("crossFloorWeight", 0))
    lc = spec.get("linkCorridor", {})
    tabs = lc.get("tabs", [])
    nid = lc.get("nodeId", "outdoor_stair")
    for i in range(len(tabs) - 1):
        add(nav_id(tabs[i], nid), nav_id(tabs[i + 1], nid), w0)

    zw = float(spec.get("zoneLinks", {}).get("crossZoneWeight", 15))
    for z in spec.get("zoneLinks", {}).get("pairs", []):
        add(nav_id(z["bTab"], z["bNode"]), nav_id(z["linkTab"], z["linkNode"]), zw)
        add(nav_id(z["aTab"], z["aNode"]), nav_id(z["linkTab"], "link_to_a"), zw)

    for node_id, vert in spec.get("bZone", {}).get("unifiedVertical", {}).items():
        tabs = vert.get("tabs", [])
        for i in range(len(tabs) - 1):
            a, b = nav_id(tabs[i], node_id), nav_id(tabs[i + 1], node_id)
            if a != b:
                add(a, b, w0)

    for node_id, vert in spec.get("aZone", {}).get("unifiedVertical", {}).items():
        tabs = vert.get("tabs", [])
        for i in range(len(tabs) - 1):
            a, b = nav_id(tabs[i], node_id), nav_id(tabs[i + 1], node_id)
            if a != b:
                add(a, b, w0)

    return adj


def dijkstra(adj: dict[str, list[tuple[str, float]]], start: str, end: str) -> tuple[float, list[str]] | None:
    if start not in adj or end not in adj:
        return None
    dist = {start: 0.0}
    prev: dict[str, str | None] = {start: None}
    pq = [(0.0, start)]
    seen: set[str] = set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in seen:
            continue
        seen.add(u)
        if u == end:
            path = []
            at: str | None = u
            while at is not None:
                path.append(at)
                at = prev[at]
            path.reverse()
            return d, path
        for v, w in adj.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return None


def main() -> int:
    graphs = load_graphs()
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    adj = build_adj(graphs, spec)

    tests = [
        ("B1 link_to_a → lk1 link_to_b", "b1_link_to_a", "lk1_link_to_b"),
        ("A1 link_to_b → lk1 link_to_a", "a1_link_to_b", "lk1_link_to_a"),
        ("B1 room137 → A1 office101（须经连廊）", "b1_room137_front", "a1_office101_front"),
        ("B3 link_to_a → A3 washroom", "b3_link_to_a", "a3_washroom"),
    ]
    ok = True
    for title, s, e in tests:
        r = dijkstra(adj, s, e)
        if not r:
            print(f"FAIL  {title}: {s} → {e}")
            ok = False
            continue
        d, path = r
        print(f"OK    {title}: dist={d:.1f} hops={len(path)}")
        print(f"      {' → '.join(path[:8])}{'…' if len(path) > 8 else ''}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
