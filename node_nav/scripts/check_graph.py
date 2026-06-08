#!/usr/bin/env python3
"""校验楼层 graph JSON：节点边覆盖、端点合法、全图连通。"""

from __future__ import annotations

import json
import sys
from collections import defaultdict, deque
from pathlib import Path


def validate(graph: dict) -> int:
    nodes = {n["id"]: n for n in graph["nodes"]}
    node_ids = set(nodes)
    edges = graph["edges"]

    bad_endpoints: list[tuple[int, str, dict]] = []
    for i, e in enumerate(edges):
        for key in ("from", "to"):
            if e[key] not in node_ids:
                bad_endpoints.append((i, e[key], e))

    in_edge: set[str] = set()
    adj: dict[str, set[str]] = defaultdict(set)
    seen_pairs: set[tuple[str, str]] = set()
    dup_edges: list[dict] = []

    for e in edges:
        a, b = e["from"], e["to"]
        in_edge.add(a)
        in_edge.add(b)
        adj[a].add(b)
        adj[b].add(a)
        pair = tuple(sorted((a, b)))
        if pair in seen_pairs:
            dup_edges.append(e)
        else:
            seen_pairs.add(pair)

    isolated = sorted(node_ids - in_edge)

    start = sorted(node_ids)[0] if node_ids else ""
    seen: set[str] = set()
    if start:
        q = deque([start])
        seen.add(start)
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    q.append(v)

    extra_components: list[list[str]] = []
    rem = node_ids - seen
    while rem:
        s = min(rem)
        comp: set[str] = set()
        q = deque([s])
        while q:
            u = q.popleft()
            if u in comp:
                continue
            comp.add(u)
            for v in adj[u]:
                if v not in comp:
                    q.append(v)
        extra_components.append(sorted(comp))
        rem -= comp

    fac_issues: list[tuple[str, str, str]] = []
    for f in graph.get("facilities", []):
        nid = f.get("nodeId")
        if nid not in node_ids:
            fac_issues.append((f.get("id", "?"), nid or "?", "unknown node"))

    ok = not isolated and not bad_endpoints and len(seen) == len(node_ids)

    print(f"nodes: {len(node_ids)}  edges: {len(edges)}")
    print()
    print("[1] 未出现在任何 edge 中的节点:")
    if isolated:
        for nid in isolated:
            n = nodes[nid]
            print(f"  FAIL  {nid}  ({n.get('label', '')})  role={n.get('role')}")
    else:
        print("  OK  全部节点至少连一条边")

    print()
    print("[2] edge 端点引用不存在的节点:")
    if bad_endpoints:
        for i, nid, e in bad_endpoints:
            print(f"  FAIL  edge#{i}  {nid}  {e}")
    else:
        print("  OK")

    print()
    print("[3] 重复的无向边:")
    if dup_edges:
        for e in dup_edges:
            print(f"  WARN  {e['from']} <-> {e['to']}  weight={e.get('weight')}")
    else:
        print("  OK  无重复")

    print()
    print("[4] 全图连通性:")
    if len(seen) == len(node_ids):
        print(f"  OK  从 {start} 可达 {len(seen)}/{len(node_ids)}，图全通")
    else:
        print(f"  FAIL  主连通分量 {len(seen)}/{len(node_ids)}")
        for i, comp in enumerate(extra_components):
            print(f"    分量 #{i + 1} ({len(comp)} 节点): {', '.join(comp)}")

    print()
    print("[5] facilities.nodeId:")
    if fac_issues:
        for item in fac_issues:
            print(f"  FAIL  {item}")
    else:
        print("  OK")

    print()
    print("RESULT:", "PASS" if ok and not dup_edges else ("WARN (有重复边)" if ok else "FAIL"))
    return 0 if ok else 1


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python check_graph.py <graph.json>", file=sys.stderr)
        return 1
    path = Path(sys.argv[1])
    graph = json.loads(path.read_text(encoding="utf-8"))
    print(f"=== {path.name} ===")
    return validate(graph)


if __name__ == "__main__":
    raise SystemExit(main())
