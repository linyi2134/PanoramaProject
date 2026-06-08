#!/usr/bin/env python3
"""校验 pick-coords 导出的 cad_pick JSON（不写回 graph）。

用法（PanoramaProject 目录）：
  python node_nav/scripts/check_cad_pick.py ../cad_pick_f4_b.json
  python node_nav/scripts/check_cad_pick.py map_data/cad_pick_f5_a.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def check(pick_path: Path) -> int:
    pick = json.loads(pick_path.read_text(encoding="utf-8"))
    coords = pick.get("coords") or {}
    if not coords:
        print("FAIL: coords 为空")
        return 1

    gf = pick.get("graphFile")
    if not gf:
        print("FAIL: 缺少 graphFile")
        return 1
    gpath = (ROOT / gf).resolve()
    if not gpath.is_file():
        print(f"FAIL: graph 不存在: {gf}")
        return 1

    graph = json.loads(gpath.read_text(encoding="utf-8"))
    gids = {n["id"] for n in graph["nodes"]}
    cids = set(coords)
    missing = sorted(gids - cids)
    extra = sorted(cids - gids)

    pw, ph = int(pick.get("planWidth", 0)), int(pick.get("planHeight", 0))
    oob = []
    for nid, c in coords.items():
        x, y = int(c["x_px"]), int(c["y_px"])
        if x < 0 or y < 0 or x > pw or y > ph:
            oob.append(nid)

    pos = [(c["x_px"], c["y_px"]) for c in coords.values()]
    dup_count = len(pos) - len(set(pos))

    plan = pick.get("planImage", "")
    plan_path = ROOT / plan
    img_note = "PNG 未找到"
    if plan_path.is_file():
        try:
            from PIL import Image

            w, h = Image.open(plan_path).size
            img_note = f"{w}×{h}"
            if (w, h) != (pw, ph):
                img_note += f"（与 JSON 中 {pw}×{ph} 不一致）"
            else:
                img_note += " OK"
        except ImportError:
            img_note = "（未安装 Pillow，跳过尺寸校验）"
        except OSError as e:
            img_note = f"无法读取 PNG: {e}"

    ok = not missing and not oob
    print(f"{'OK' if ok else 'WARN'}  {pick_path.name}")
    print(f"  {pick.get('description', '')}  floor={pick.get('floor')} zone={pick.get('zone')}")
    print(f"  graph: {gf}  节点 {len(gids)}，coords {len(cids)}")
    if missing:
        print(f"  缺少节点: {', '.join(missing)}")
    if extra:
        print(f"  多余 id（可忽略）: {', '.join(extra)}")
    if oob:
        print(f"  超出底图范围: {', '.join(oob)}")
    if dup_count:
        print(f"  重复坐标对: {dup_count} 组（可能是同一位置多个节点，需目视确认）")
    print(f"  planImage={plan}  meta={pw}×{ph}  实际={img_note}")
    print(f"  pdfSource={pick.get('pdfSource', '?')}")
    return 0 if ok else 1


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1
    rc = 0
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.is_absolute():
            p = (ROOT / p).resolve()
        if not p.is_file():
            p = Path(arg).resolve()
        if not p.is_file():
            print(f"找不到: {arg}", file=sys.stderr)
            rc = 1
            continue
        rc = max(rc, check(p))
        print()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
