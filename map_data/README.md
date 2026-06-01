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

**1F B 区已做完**：见 `map_data/id_map_f1_b.json`，重跑：

```bash
python node_nav/scripts/apply_layout_coords.py
```

其他层：复制 `id_map_f1_b.json` 为 `id_map_f2_b.json` …，改对照后执行：

```bash
python node_nav/scripts/apply_layout_coords.py id_map_f2_b.json f2_b_graph.json
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
| `map_data/id_map_f1_b.json` | FLOORS[1] ↔ `f1_b_graph.json` 节点 id 对照（含 direct / inferred） |
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

## 启动

```bash
cd PanoramaProject
python server_main.py
# 打开 http://localhost:8000/map.html
```

`map.html` 依赖同目录下的 `js/pathfind.browser.js`（与 `node_nav/src/pathfind.js` 算法一致）。
