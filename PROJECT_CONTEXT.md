# PROJECT_CONTEXT · B7 校园导览与信息导航系统

> 供新对话 / 新 agent 快速接手。  
> 路径：`c:\Users\yoimi\indoor_navigator\PanoramaProject`  
> GitHub：[linyi2134/PanoramaProject](https://github.com/linyi2134/PanoramaProject)  
> **交接 Prompt**：复制 [AGENT_HANDOFF.md](./AGENT_HANDOFF.md) 中「Prompt 正文」到新对话。

---

## 1. 项目是什么

**课程项目「知途」**：B7 教学楼室内导览与导航，**以手机扫码用户为主**。

| 模块 | 说明 |
|------|------|
| **主产品** | `index.html` → `map.html`：CAD + 选起终点 + Dijkstra + 路径指引 |
| **公网** | GitHub Pages：`https://linyi2134.github.io/PanoramaProject/` |
| **辅助** | `panorama_full.html`：52 场景 360°，3 场景 LRU 缓存 |
| **联动** | `js/panorama_map_bridge.js`：B/A/连廊/三栋 走廊节点 ↔ 全景场景 |
| **不做** | Qt 客户端、BLE/WiFi 定位 |

工作区：`indoor_navigator/` 下**仅有** `PanoramaProject/`；原外层散落文件已归档到 `backup/indoor_navigator_misc/`。

---

## 2. 如何运行

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py
```

| URL | 用途 |
|-----|------|
| https://linyi2134.github.io/PanoramaProject/ | **公网**（扫码推荐） |
| http://localhost:8000/map.html | 本地二维导航 |
| http://localhost:8000/panorama_full.html | 本地全景 |
| http://localhost:8000/tools/pick-coords.html | CAD 取点 |

禁止 `file://`；禁止在上级目录启动服务。Pages 更新约 1–3 分钟，手机需强刷。

---

## 3. map.html 架构

### Tab 与底图

| tab | 标签 | JSON | 前缀 |
|-----|------|------|------|
| 1–5 | B1F–B5F | `f{n}_b_graph.json` | `b{n}_` |
| 14–18 | 连廊1F–5F | `link_f{n}_graph.json` | `lk{n}_` |
| 8–12 | A1F–A5F | `f{n}_a_graph.json` | `a{n}_` |

15 层 CAD：`plans/*_cad.png`。首屏只载 B1F，其余 `loadJsonGraphsBackground()` + `floorJsonReady()`。

### 算路

- `buildGraph()`：合并 15 层 nodes/edges
- `crossEdges()`：读 `map_data/cross_floor_links.json`
  - **竖向**：B 三井、A stair_south / stair_small、连廊 outdoor_stair
  - **跨层 weight**：6；**跨区 zoneLinks**：15
- `js/pathfind.browser.js`：Dijkstra（`?v=20260609`）
- `sameFloorVerticalPolicy`：同 tab 禁竖向边（A1F 翼/主楼例外）

### 交互（桌面 + 手机共通）

1. 右侧选「起点/终点」→ 地图点节点（可换 tab）
2. 顶栏「⬡ 路网线」默认关；**导航橙色路径始终显示**
3. 房间标注**默认隐藏**，点击节点后显示（`revealedLabels`）；起终点始终显示
4. 有全景对照的节点（蓝虚线圈）→ 弹窗进全景或继续选点

### 手机端布局（≤768px，`@media` 专用）

| 区域 | 行为 |
|------|------|
| 顶栏 | 高度约减 1/4；字号缩小；楼层 tab 可横滑 |
| 地图 | 占满 `.main` 宽度 |
| 侧栏 | **浮层**叠在地图右缘；默认 **折叠 48px**（仅起点/终点） |
| 侧栏展开 | **160px** 宽，显示图例/房间/路径；**不挤压**地图 |
| 缩放 | Panzoom（unpkg CDN）：pinch / 滚轮；右下角 ＋－⟳；`switchFloor` 时 reset |

桌面（>768px）：侧栏固定 **320px**，无折叠，较大字号。

### 二维 ↔ 全景

详见 [map_data/panorama_map_bridge.md](./map_data/panorama_map_bridge.md)。

| 区域 | 全景 | 二维节点要点 |
|------|------|----------------|
| B 二栋 | `二栋-{n}f-1`…`4` | 西南/西北/东南/东北分叉 |
| A 一栋 | `一栋-{n}f-*` | 1F 仅 2 场景；2–5F 南侧楼梯+四分叉 |
| 连廊 | `连廊-{n}f` | `outdoor_stair` |
| 三栋 | `三栋-1f`…`3f` | `a{n}_stair_small` |

---

## 4. panorama_full.html 要点

- **LRU**：最多缓存 3 个场景 DOM；`switchToScene()` 管理 destroy/load
- **场景热点**：`buildSceneHotspots()` → `type:"scene"` + `clickHandlerFunc`（**不设 sceneId、不用 cssClass**）
- **CSS**：`.pnlm-hotspot-base.pnlm-scene` 雪碧图放大 5×（130px）
- **房间蓝点**：`cssClass:"room-info-hotspot"`，42px 自绘圆点
- **陷阱**：对场景热点用 `cssClass` 会去掉 `pnlm-sprite`，图标变 info「i」或消失

---

## 5. A 座东侧翼

- 1F 主楼与东侧翼 **层内不互通** → 须经 **A2F** + `stair_small`
- `f1_a` 单层 `check_graph` 可能 FAIL；以 map 合并图为准

---

## 6. 目录要点

```
PanoramaProject/
├── index.html, map.html, panorama_full.html, server_main.py
├── js/pathfind.browser.js, js/panorama_map_bridge.js, js/room_labels_all.js
├── plans/*_cad.png
├── node_nav/data/*.json
├── map_data/cross_floor_links.json, panorama_map_bridge.md
├── tools/pick-coords.html
├── indoor_nav/
├── backup/
├── AGENT_HANDOFF.md          ← 交接 Prompt（复制用）
├── PROJECT_CONTEXT.md        ← 本文件
└── README.md
```

---

## 7. 已完成 vs 待办

### 已完成

- [x] 15 层 CAD + JSON；跨层/跨区算路；二维↔全景深链
- [x] GitHub Pages + index.html 扫码入口
- [x] map 懒加载；浅蓝 UI；Panzoom 缩放
- [x] map 手机端：折叠侧栏浮层、顶栏压缩、点击显示房间名
- [x] 全景 LRU + 场景/房间热点修复

### 待办

- [ ] 边权实地丈量
- [ ] 清理 `cross_floor_links.json` 废弃字段
- [ ] 2F-B 东侧动线（backup 草稿）
- [ ] 可选：全景压缩；Panzoom 本地化

---

## 8. 陷阱

1. `map.html` 只在 `</html>` 前保留**一份** `<script>`
2. JSON id **无前缀**；map 合并图 **有** `b1_`/`a1_`/`lk1_` 前缀
3. 改 graph → bump **`GRAPH_CACHE_VER`**（`20260610-fix-load`）+ Ctrl+F5
4. 手机 CSS 仅写在 `@media (max-width:768px)` 内
5. 全景场景热点勿 `cssClass`；房间热点才用 `room-info-hotspot`
6. 不主动 git commit/push

---

## 9. 验证

```powershell
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
```

**map**：B1→A1 经连廊；A1 主楼→room_104 经 A2F。  
**手机**：≤768px 侧栏折叠、地图全宽、缩放可用。  
**全景**：场景箭头热点可点；房间蓝点 42px。

---

*最后更新：2026-06-10*
