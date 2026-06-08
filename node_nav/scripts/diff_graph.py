#!/usr/bin/env python3
"""对比两个 graph JSON 的节点/边差异。"""
import json
import sys
from pathlib import Path


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def compare(new_path: Path, old_path: Path) -> None:
    n, o = load(new_path), load(old_path)
    nn = {x["id"]: x for x in n["nodes"]}
    on = {x["id"]: x for x in o["nodes"]}

    def edge_pairs(g):
        s = set()
        for e in g["edges"]:
            a, b = e["from"], e["to"]
            s.add((min(a, b), max(a, b)))
        return s

    ne, oe = edge_pairs(n), edge_pairs(o)
    print(f"=== {new_path.name} vs {old_path.name} ===")
    print(f"  nodes: {len(on)} -> {len(nn)}")
    print(f"  edges: {len(o['edges'])} -> {len(n['edges'])}")
    added = sorted(set(nn) - set(on))
    removed = sorted(set(on) - set(nn))
    if added:
        print("  + nodes:", ", ".join(added))
    if removed:
        print("  - nodes:", ", ".join(removed))
    relabel = [i for i in set(nn) & set(on) if nn[i].get("label") != on[i].get("label")]
    if relabel:
        print("  ~ label:", ", ".join(f"{i}" for i in relabel[:8]) + ("..." if len(relabel) > 8 else ""))
    en = sorted(ne - oe)
    er = sorted(oe - ne)
    if en:
        print(f"  + edges ({len(en)}):", "; ".join(f"{a}-{b}" for a, b in en[:12]) + ("..." if len(en) > 12 else ""))
    if er:
        print(f"  - edges ({len(er)}):", "; ".join(f"{a}-{b}" for a, b in er[:12]) + ("..." if len(er) > 12 else ""))
    nc = sum(1 for x in n["nodes"] if x.get("x_px") is not None)
    oc = sum(1 for x in o["nodes"] if x.get("x_px") is not None)
    print(f"  coords x_px: {oc} -> {nc}")
    print()


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    outer = root.parent
    data = root / "node_nav" / "data"
    for name in ("f4_a_graph.json", "f4_b_graph.json", "f5_a_graph.json", "f5_b_graph.json"):
        compare(outer / name, data / name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
