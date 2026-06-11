# 二维地图数据说明

## 两套数据并存（当前阶段）

| 来源 | 文件 | 用途 |
|------|------|------|
| **示意图地图** | `map.html` 内 `FLOORS` | B 区 1–5F 交互导航：SVG 示意图 + 内嵌 x/y + 点击选点 |
| **实地路网 JSON** | `node_nav/data/f*_graph.json` | A/B 分区详细节点与边；供 Python `indoor_nav`、后续真实平面图对接 |

二者 **节点 id 不同**（如 `f1_wash` vs `washroom`），**尚未自动同步**。演示优先用 `map.html`；课程数据与校验以 JSON 为准。

## 如何把 PNG、id、主页面连起来

整体链路：

```
PNG 底图 (plans/f1_b.png)
    ↕ 同尺寸 760×520
JSON 节点 x_px / y_px  ←── id 对照表 ←── map.html FLOORS 的 x,y
    ↕
map.html 读取 JSON + 贴 PNG → 点击节点算路
```

### 第一步：PNG 放进 `plans/`

文件名与 JSON 里 `meta.planImage` 一致，例如：

| 文件 | 说明 |
|------|------|
| `plans/f1_b.png` | 1F B 区示意（760×520） |
| `plans/f2_b.png` … | 其他层同理 |

若从导出页下载，请**复制到** `PanoramaProject/plans/`，不要只留在「下载」文件夹。

### 第二步：JSON 里写坐标（联系 id 与图）

每个节点要有 **`x_px` / `y_px`**（相对 PNG 左上角像素），`meta` 要有：

```json
"meta": {
  "planImage": "plans/f1_b.png",
  "planWidth": 760,
  "planHeight": 520
}
```

**15 层 id_map 已生成**：`map_data/id_map_*.json`（B/A/连廊），供 map 搜索别名与文档对照。

重新生成（改 graph 节点 id 后）：

```bash
python node_nav/scripts/generate_id_maps.py
```

**注意**：各层 graph 已用 CAD 坐标，勿对 B2+ / A / 连廊运行 `apply_layout_coords.py`（仅 B1 示意层历史用途）。B1 示意坐标：

```bash
python node_nav/scripts/apply_layout_coords.py
```

### 第三步：在 map.html 里启用

`map.html` 已支持：

- **所有楼层**：有 `plans/f{n}_b.png` 则显示 PNG 底图
- **已合并 JSON 的楼层**（目前 **1F**）：读 `node_nav/data/f1_b_graph.json`，节点 id / 算路以 JSON 为准；标题栏显示「JSON路网」

在 `map.html` 的 `JSON_GRAPHS` 里增加一行即可启用下一层，例如：

```javascript
const JSON_GRAPHS={
  1:'node_nav/data/f1_b_graph.json',
  2:'node_nav/data/f2_b_graph.json',  // f2 坐标写好后取消注释
};
```

### 验证

```bash
python server_main.py
# 打开 http://localhost:8000/map.html
# 1F 应看到 PNG 底图 + 节点；可试 room137_front → washroom
```

---

| 文件 | 说明 |
|------|------|
| `map_data/id_map_*.json` | 15 层节点对照 + 搜索房号别名（`generate_id_maps.py` 维护） |
| `node_nav/data/f1_b_graph.json` | 已写入 `x_px/y_px` 及 `meta.planImage/planWidth/planHeight` |
| `plans/f1_b.png` | 760×520 示意底图（与 map.html 建筑几何一致） |

重新应用坐标（改对照表或 map.html 后）：

```bash
python node_nav/scripts/apply_layout_coords.py
```

导出示意底图（与 map.html `renderBuild()` 一致，760×520）：

```bash
# 命令行批量：plans/f1_b.png … f5_b.png（加 --svg 同时出 .svg）
python node_nav/scripts/export_map_png.py --all --svg

# 浏览器单张导出（选楼层 → 下载 SVG/PNG）
# http://localhost:8000/tools/export_floor_png.html
```

## 后续合并方向

1. 从 DWG/PDF 导出 `plans/f1.png` 等底图  
2. 建立 `id` 对照表（`f1_rm138` ↔ `room137_front` 等）  
3. 或将 `FLOORS` 抽离为 `map_data/schematic_b.json`，与 `pathfind.browser.js` 共用

## CAD 底图（PDF 统一命名，见 `cad_sources.json`）

| 根目录 PDF | 用途 | 导出 PNG |
|------------|------|----------|
| `1F-A.pdf` … `5F-A.pdf` | A 座各层 | `plans/f1_a_cad.png` … `f5_a_cad.png` |
| `1_2_5F-B.pdf` | B 座 1/2/5 层 | `plans/f1_b_cad.png`（导出时**顺时针 90°**，北向上；2F/5F 同图复制） |
| `3F-B.pdf` | B 座 3/4 层（修订 CAD，同图） | `plans/f3_b_cad.png`、`f4_b_cad.png` |
| `A-B连廊_1F.pdf` | 连廊 1F | `plans/link_f1_cad.png` |
| `A-B连廊_1-5F共享.pdf` | 连廊 2–5F（同图） | `plans/link_f2_cad.png` … `link_f5_cad.png` |

批量转 PNG：

```bash
python node_nav/scripts/export_all_cad_plans.py --dpi 400
```

上级 PDF 单张转 PNG 示例：

```bash
python node_nav/scripts/dwg_or_pdf_to_png.py ../F4_A.pdf -o plans/f4_a_cad.png --dpi 400 --target-size 537x529
python node_nav/scripts/dwg_or_pdf_to_png.py ../A-B连廊_1F.pdf -o ../cad_preview_ab_link_1f.png --dpi 400
```

## CAD 重新标点（A/B 座 + 连廊 1–5F）

1. `python server_main.py` → http://localhost:8000/tools/pick-coords.html（**用 `.html`，非 `.htm`**）  
2. 选 **A 座 / B 座 / 连廊（A-B）** 与楼层，拖点  
3. 导出 `cad_pick_f{n}_{a|b}.json` 或 `cad_pick_link_f{n}.json` → 放入 `map_data/` 或上级暂存  
4. 写回：

```bash
python node_nav/scripts/apply_cad_coords.py map_data/cad_pick_f1_a.json
python node_nav/scripts/apply_cad_coords.py map_data/cad_pick_link_f1.json
```

**注意：** 只改坐标用 cad_pick + apply；改节点/边只改 `node_nav/data/*_graph.json`。改 graph 后 pick-coords 须点 **「重新加载 JSON」**（清 localStorage + `GRAPH_CACHE_VER`）。

`map.html`：B/A 座与 **连廊1F–5F** tab 已可贴 CAD 底图；**JSON 算路**目前启用 1F B + 连廊（见 `JSON_GRAPHS`），其余层 apply 坐标后再加。

## 启动

```bash
cd PanoramaProject
python server_main.py
# 打开 http://localhost:8000/map.html
```

`map.html` 依赖 `js/pathfind.browser.js`（算路）与 `js/panorama_map_bridge.js`（全景深链）。

## 相关文档

| 文档 | 说明 |
|------|------|
| [cross_floor_links.md](./cross_floor_links.md) | 竖向井、跨区 zoneLinks |
| [panorama_map_bridge.md](./panorama_map_bridge.md) | **二维走廊节点 ↔ 全景场景** 对照表 |
| [../panorama_data/README.md](../panorama_data/README.md) | 全景房间蓝点（与走廊对照分离） |
