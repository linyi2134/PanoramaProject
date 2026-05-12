"""
命令行（在 PanoramaProject 目录下）：

  python -m indoor_nav route node_nav/data/b1_b_zone_graph.json room136_front washroom
  python -m indoor_nav nearest node_nav/data/b1_b_zone_graph.json 洗手间 lab133_front
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from .dijkstra import load_graph_json, nearest_facility_by_type, shortest_path


def main() -> None:
    parser = argparse.ArgumentParser(description="楼内图 Dijkstra 最短路径")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_route = sub.add_parser("route", help="两点最短路")
    p_route.add_argument("graph_json", type=Path, help="图 JSON 路径")
    p_route.add_argument("start", help="起点节点 id")
    p_route.add_argument("end", help="终点节点 id")

    p_near = sub.add_parser("nearest", help="到某类设施的最近路径")
    p_near.add_argument("graph_json", type=Path, help="图 JSON 路径")
    p_near.add_argument("facility_type", help="与 facilities[].type 一致，如 洗手间、楼梯")
    p_near.add_argument("start", help="起点节点 id")

    args = parser.parse_args()
    graph = load_graph_json(args.graph_json)

    if args.cmd == "route":
        r = shortest_path(graph, args.start, args.end)
        print("距离:", r["distance"] if not math.isinf(r["distance"]) else "不可达")
        print("路径 id:", " -> ".join(r["path_node_ids"]))
        print("路径名称:", " -> ".join(r["path_labels"]))
    else:
        r = nearest_facility_by_type(graph, args.start, args.facility_type)
        print("设施:", r["facility"])
        print("距离:", r["distance"] if not math.isinf(r["distance"]) else "不可达")
        print("路径 id:", " -> ".join(r["path_node_ids"]))
        print("路径名称:", " -> ".join(r["path_labels"]))


if __name__ == "__main__":
    main()
