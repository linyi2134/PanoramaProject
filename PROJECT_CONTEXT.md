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
| **主产品** | `index.html` → `map.html`：CAD + 起终点 + Dijkstra + **地点搜索** |
| **公网** | GitHub Pages：`https://linyi2134.github.io/PanoramaProject/` |
| **辅助** | `panorama_full.html`：52 场景（JPG 已压缩 ~32 MB） |
| **联动** | `panorama_map_bridge.js`：走廊节点 ↔ 全景；map 浏览时 **预取全景 JPG** |
| **不做** | Qt 客户端、BLE/WiFi 定位 |

---

## 2. 如何运行

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py
```

| URL | 用途 |
|-----|------|
| https://linyi2134.github.io/PanoramaProject/map.html | **公网扫码（推荐）** |
| http://localhost:8000/map.html | 本地二维 |
| http://localhost:8000/panorama_full.html | 本地全景 |

禁止 `file://`。push 推荐 SSH：`git push git@github.com:linyi2134/PanoramaProject.git main`

**Pages 部署**：`.github/workflows/deploy-pages.yml` + `.nojekyll`；Settings → Pages → GitHub Actions → Deploy GitHub Pages。

---

## 3. map.html 架构

### Tab 与底图

| tab | 标签 | JSON | 前缀 |
|-----|------|------|------|
| 1–5 | B1F–B5F | `f{n}_b_graph.json` | `b{n}_` |
| 14–18 | 连廊1F–5F | `link_f{n}_graph.json` | `lk{n}_` |
| 8–12 | A1F–A5F | `f{n}_a_graph.json` | `a{n}_` |

15 层 CAD：`plans/*_cad.png`。首屏只载 B1F，其余后台懒加载。

### 算路

- `buildGraph()` + `crossEdges()` + `pathfind.browser.js`
- 跨层 weight **6**；跨区 zoneLinks **15**
- `sameFloorVerticalPolicy`：同 tab 禁竖向边（A1F 翼/主楼例外）

### 交互要点

1. 侧栏选起点/终点 → 地图点节点
2. **🔍 地点搜索**：弹窗 → 跳层 + 设终点 + 算路
3. **可跳转节点**（琥珀圈 `#e8912d`、常显标签）：连廊口 / 电梯 / 楼梯 → `portalModal` 跳 B·连廊·A 或上/下楼
4. **设施（facility）**：标注默认显示；房间点击后 `revealedLabels`
5. 对照节点蓝虚线圈 → 弹窗可进全景
6. **预取**：`prefetchAllCadImages` → `runPanoramaPrefetch`（当前层优先，再 FLOOR_ORDER 其余层；切 tab abort）

### 搜索房号说明

- JSON 节点 label 常无房号（如「移动计算与软件实验室」）
- 15 层 `map_data/id_map_*.json` → `loadRoomSearchAliases()`
- 其他楼层：从节点 `id` / label 内数字匹配（如 `room331_front` → 331）

### 手机端（≤768px）

| 区域 | 行为 |
|------|------|
| 侧栏折叠 | **52px**：◀ + **🔍** + 起/终点竖排 |
| 侧栏展开 | 160px 浮层，不挤地图 |
| 缩放 | Panzoom 本地 js/panzoom.min.js；切层 reset |

桌面（>768px）：侧栏 320px；搜索在「路径规划」标题旁 🔍。

---

## 4. panorama_full.html 要点

- JPG：**3000px q80**，52 张 ~32 MB；`?v=20260610-compress`
- **无全屏 loader**（已删除半黑转圈）
- LRU **5 场景**：`addScene` / `loadScene` / `removeScene`（**勿 destroy 整 viewer**）
- 场景热点 **35px**（`.pnlm-scene`）；房间蓝点 **14px**
- 底部「二维地图」链接：**下划线**
- 场景热点：`type:"scene"` + `clickHandlerFunc`；**禁止 cssClass / sceneId**

压缩脚本：`python node_nav/scripts/compress_panoramas.py`（原图 `backup/panoramas_original/`）

---

## 5. 二维 ↔ 全景

见 [map_data/panorama_map_bridge.md](./map_data/panorama_map_bridge.md)。Bridge `?v=20260610-prefetch`，含 `panoramaImageUrl(sceneId)`。

---

## 6. A 座东侧翼

A1F 主楼 ↔ 翼内 **不互通** → 须 A2F + `stair_small`。`f1_a` 单层 check_graph 可能 FAIL。

---

## 7. 目录要点

```
PanoramaProject/
├── .github/workflows/deploy-pages.yml
├── map.html, panorama_full.html, index.html, server_main.py
├── js/panorama_map_bridge.js, js/pathfind.browser.js, js/room_labels_all.js
├── panoramas/*.jpg
├── map_data/id_map_*.json, cross_floor_links.json
├── node_nav/data/*.json, node_nav/scripts/compress_panoramas.py
├── AGENT_HANDOFF.md, README.md, PROJECT_CONTEXT.md
└── backup/（含 panoramas_original/，gitignore）
```

---

## 8. 功能完成度

- [x] 15 层 CAD + 跨层/跨区算路 + 二维↔全景深链
- [x] GitHub Pages（deploy-pages.yml）；map 搜索；跨区跳转 portalModal
- [x] CAD/全景分级预取；设施与跳转节点常显标注
- [x] 全景压缩与 LRU；cross_floor 废弃字段清理
- [x] 边权实地走查（同层/跨区/跨层）
- [x] 2F-B 东侧动线（237/234/236 等）
- [x] 15 层 id_map 搜索别名；Panzoom 本地化

---

## 9. 陷阱

1. `map.html` 仅一份 `<script>`，勿在 `</html>` 后再加 JS
2. JSON id 无前缀；map 运行时 b1_/a1_/lk1_
3. bump `GRAPH_CACHE_VER` / bridge `?v=` / `PANORAMA_CACHE_VER`
4. 全景场景热点勿 cssClass
5. 不主动 commit/push

---

## 10. 验证

```powershell
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
```

- map 点连廊口/电梯 → 琥珀圈弹窗跳转
- 手机折叠侧栏见 🔍
- Network：先 CAD 再 panoramas；切层 canceled

---

*最后更新：2026-06-11（待办已清空）*
