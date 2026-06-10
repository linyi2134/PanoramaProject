# PROJECT_CONTEXT · B7 校园导览与信息导航系统

> 供新对话 / 新 agent 快速接手。  
> 路径：`c:\Users\yoimi\indoor_navigator\PanoramaProject`  
> GitHub：[linyi2134/PanoramaProject](https://github.com/linyi2134/PanoramaProject)  
> **交接 Prompt**：复制 [AGENT_HANDOFF.md](./AGENT_HANDOFF.md) 中「Prompt 正文」到新对话。

---

## 1. 项目是什么

**课程项目「知途」**：B7 教学楼室内导览与导航。

| 模块 | 说明 |
|------|------|
| **主产品** | `map.html`：CAD + 选起终点 + Dijkstra + 路径指引 |
| **辅助** | `panorama_full.html`：52 场景 360°，与二维深链互通 |
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
| http://localhost:8000/map.html | 二维导航 |
| http://localhost:8000/panorama_full.html | 全景 |
| http://localhost:8000/tools/pick-coords.html | CAD 取点 |

禁止 `file://`；禁止在上级目录启动服务。

---

## 3. map.html 架构（2026-06-10）

### Tab 与底图

| tab | 标签 | JSON | 前缀 |
|-----|------|------|------|
| 1–5 | B1F–B5F | `f{n}_b_graph.json` | `b{n}_` |
| 14–18 | 连廊1F–5F | `link_f{n}_graph.json` | `lk{n}_` |
| 8–12 | A1F–A5F | `f{n}_a_graph.json` | `a{n}_` |

15 层 CAD：`plans/*_cad.png`，经 `JSON_GRAPHS` 全部启用。

### 算路

- `buildGraph()`：合并 15 层 nodes/edges
- `crossEdges()`：读 `map_data/cross_floor_links.json`
  - **竖向**：B 三井（elevator / stair_east / stair_west 各 5 层）、A stair_south（5 层）、stair_small（3 层）、连廊 outdoor_stair（5 层）
  - **跨层 weight**：`crossFloorWeight = 6`（每上下一层）
  - **跨区**：`zoneLinks`，weight 15；**已移除** 示意 `CROSS_CAMPUS` 直连
- `js/pathfind.browser.js`：Dijkstra（`?v=20260609`）
- `buildGraph(startN,endN)`：同 tab 起终点时过滤竖向边（A1F 翼/主楼例外见 `sameFloorVerticalPolicy`）

### 交互

1. 右侧选「起点/终点」→ 地图点节点（可换 tab）
2. 选起点后自动切终点模式；仅选起点时侧栏提示「已选起点…」，**不**报「未找到路径」
3. 顶栏「⬡ 路网线」：默认隐藏灰色边；**导航橙色路径始终显示**
4. 起终点：`gMarkers` 层（绿起/红终）
5. 有全景对照的节点（蓝虚线圈）→ 弹窗进全景或继续选点

### 二维 ↔ 全景

详见 [map_data/panorama_map_bridge.md](./map_data/panorama_map_bridge.md)。

| 区域 | 全景 | 二维节点要点 |
|------|------|----------------|
| B 二栋 | `二栋-{n}f-1`…`4` | 西南/西北/东南/东北分叉 |
| A 一栋 | `一栋-{n}f-*` | 1F 仅 2 场景；2–5F 南侧楼梯+四分叉 |
| 连廊 | `连廊-{n}f` | `outdoor_stair` |
| 三栋 | `三栋-1f`…`3f` | `a{n}_stair_small`（A 座 tab 上） |

### 竖向井（JSON 内 id → 勿跨井串线）

| 区域 | nodeId | 跨层 |
|------|--------|------|
| B | `elevator`, `stair_east`, `stair_west` | 各 5 层独立链；同层仅 elevator↔stair_east |
| A | `stair_south` | 5 层 |
| A | `stair_small` | **仅** 3 层（A1–A3） |
| 连廊 | `outdoor_stair` | 5 层 |

---

## 4. A 座东侧翼

- 1F 主楼与东侧翼 **层内不互通** → 须经 **A2F** + `stair_small`
- `f1_a`：有 `room_104A/B` ↔ `stair_small`；**无** 主楼直连 104
- 单层 `check_graph` 对 f1_a 可能 FAIL（翼内孤立子图）；以 map 合并图为准

---

## 5. 目录要点

```
PanoramaProject/
├── map.html, panorama_full.html, server_main.py
├── js/pathfind.browser.js, js/panorama_map_bridge.js
├── js/room_labels_all.js
├── plans/*_cad.png          # 15 张正式底图
├── node_nav/data/*.json     # 15 层路网
├── map_data/cross_floor_links.json, panorama_map_bridge.md
├── tools/pick-coords.html
├── indoor_nav/              # CLI 单层算路
├── backup/                  # 归档（见 backup/README.md）
├── AGENT_HANDOFF.md
└── PROJECT_CONTEXT.md       # 本文件
```

---

## 6. 已完成 vs 待办

### 已完成

- [x] 15 层 CAD + JSON 全启用；B/A/lk 前缀合并图
- [x] 跨层 weight=6；跨区 zoneLinks；移除 CROSS_CAMPUS 直连
- [x] 起终点 UI、路径高亮、路网线可选显示
- [x] pathfind.browser.js 语法修复；换层指引（电梯/楼梯/连廊）
- [x] verify_zone_route.py PASS
- [x] 同层算路禁竖向边（A1F 翼例外）
- [x] 二维↔全景对照 + 双向深链（B/A/连廊/三栋）
- [x] 仓库清理：外层杂物 → `backup/`

### 待办

- [ ] 同层边权、zoneLinks weight 实地丈量
- [ ] 清理 `cross_floor_links.json` 内 `campusCrossFloor` 废弃字段（map 已不再读）
- [ ] 2F-B 东侧动线（237/234/236）— 草稿在 `backup/indoor_navigator_misc/2F-B座.json`
- [ ] 可选：0.0.0.0 + 二维码；二栋 `-5` 电梯区全景对照

---

## 7. 陷阱

1. `map.html` 只在 `</html>` 前保留**一份** `<script>`
2. JSON id **无前缀**；map 合并图 **有** `b1_`/`a1_`/`lk1_` 前缀
3. 改 graph / cross_floor_links → bump **`GRAPH_CACHE_VER`**（当前 `20260609-same-floor-vert`）+ Ctrl+F5
4. 改 `panorama_map_bridge.js` → bump bridge 的 `?v=`（当前 `20260609-san`）
5. `pathfind.browser.js` 若缓存旧版会导致「未找到路径」— 强刷或改 `?v=` 参数
6. 三栋全景 ↔ `stair_small`，不是独立地图 tab
7. 不主动 git commit/push

---

## 8. 验证

```powershell
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
python node_nav/scripts/check_graph.py node_nav/data/f1_a_graph.json
```

**map 手动**：B1 `room137_front` → A1 `office101_front`（经连廊）；A1 主楼 → `room_104A`（经 A2F）。

---

*最后更新：2026-06-10*
