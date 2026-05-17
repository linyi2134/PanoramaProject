"""
无向带权图上的 Dijkstra 最短路径，与 node_nav/data/*.json 结构兼容。

图 JSON 至少包含：
  - "nodes": [ { "id": str, "label": str, ... }, ... ]
  - "edges": [ { "from": str, "to": str, "weight": number }, ... ]
可选：
  - "facilities": [ { "id", "type", "nodeId", "label" }, ... ]

其它字段（如 meta、description、isFinished；旧版 explain、isfinish 仍可读）会被忽略。
"""

from __future__ import annotations

import json
import math
from heapq import heappop, heappush
from pathlib import Path
from typing import Any, TypedDict


class RouteResult(TypedDict):
    distance: float
    path_node_ids: list[str]
    path_labels: list[str]


class NearestFacilityResult(TypedDict):
    facility: dict[str, Any] | None
    distance: float
    path_node_ids: list[str]
    path_labels: list[str]


def load_graph_json(path: str | Path) -> dict[str, Any]:
    """从 JSON 文件加载图；缺省 facilities 时视为空列表。"""
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if "nodes" not in data or "edges" not in data:
        raise ValueError("JSON 须包含 nodes 与 edges 字段")
    if "facilities" not in data:
        data["facilities"] = []
    return data


def _node_labels(graph: dict[str, Any]) -> dict[str, str]:
    return {n["id"]: n.get("label", n["id"]) for n in graph["nodes"]}


def _build_adjacency(graph: dict[str, Any]) -> dict[str, list[tuple[str, float]]]:
    nodes = {n["id"] for n in graph["nodes"]}
    adj: dict[str, list[tuple[str, float]]] = {nid: [] for nid in nodes}
    for e in graph["edges"]:
        u, v = e["from"], e["to"]
        w = float(e["weight"])
        if u not in adj or v not in adj:
            raise ValueError(f"边的端点不在 nodes 中: {u!r} -> {v!r}")
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def shortest_path(graph: dict[str, Any], start_id: str, end_id: str) -> RouteResult:
    """
    Dijkstra：返回最短距离、节点 id 序列、对应中文 label 序列。
    不可达时 distance 为 inf，路径为空列表。
    """
    nodes = {n["id"] for n in graph["nodes"]}
    if start_id not in nodes or end_id not in nodes:
        raise ValueError("起点或终点 id 不在 nodes 中")

    adj = _build_adjacency(graph)
    dist: dict[str, float] = {nid: math.inf for nid in nodes}
    prev: dict[str, str | None] = {nid: None for nid in nodes}
    dist[start_id] = 0.0

    pq: list[tuple[float, str]] = [(0.0, start_id)]

    while pq:
        d, u = heappop(pq)
        if d > dist[u]:
            continue
        if u == end_id:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heappush(pq, (nd, v))

    if math.isinf(dist[end_id]):
        return {
            "distance": math.inf,
            "path_node_ids": [],
            "path_labels": [],
        }

    path_ids: list[str] = []
    cur: str | None = end_id
    while cur is not None:
        path_ids.append(cur)
        cur = prev[cur]
    path_ids.reverse()

    labels_map = _node_labels(graph)
    return {
        "distance": dist[end_id],
        "path_node_ids": path_ids,
        "path_labels": [labels_map.get(i, i) for i in path_ids],
    }


def nearest_facility_by_type(
    graph: dict[str, Any], start_id: str, facility_type: str
) -> NearestFacilityResult:
    """在所有 type 与 facility_type 相同的设施中，选最短路径的一个。"""
    facilities = graph.get("facilities") or []
    candidates = [f for f in facilities if f.get("type") == facility_type]
    if not candidates:
        return {
            "facility": None,
            "distance": math.inf,
            "path_node_ids": [],
            "path_labels": [],
        }

    best_f: dict[str, Any] | None = None
    best_route: RouteResult | None = None

    for f in candidates:
        nid = f.get("nodeId")
        if not isinstance(nid, str) or not nid:
            continue
        route = shortest_path(graph, start_id, nid)
        if best_route is None or route["distance"] < best_route["distance"]:
            best_f = f
            best_route = route

    if best_route is None or best_f is None:
        return {
            "facility": None,
            "distance": math.inf,
            "path_node_ids": [],
            "path_labels": [],
        }

    return {
        "facility": best_f,
        "distance": best_route["distance"],
        "path_node_ids": best_route["path_node_ids"],
        "path_labels": best_route["path_labels"],
    }
