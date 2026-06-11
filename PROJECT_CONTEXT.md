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
| **公网** | GitHub Pages：`https://linyi2134.github.io/PanoramaProject/map.html` |
| **辅助** | `panorama_full.html`：52 场景（JPG ~32 MB） |
| **联动** | `panorama_map_bridge.js`：走廊节点 ↔ 全景；map 浏览时预取全景 JPG |
| **不做** | Qt 客户端、BLE/WiFi 定位、访问统计 |

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
3. **可跳转节点**（琥珀圈）：连廊口 / 电梯 / 楼梯 → `portalModal`
4. **设施（facility）**：标注默认显示；房间点击后 `revealedLabels`
5. 对照节点蓝虚线圈 → 弹窗可进全景
6. **预取**：CAD → 全景（当前层优先；切 tab abort）

### 双界面模式（2026-06-11）

| 模式 | localStorage | 说明 |
|------|--------------|------|
| **经典** | `map_ui_mode=classic` | 顶栏全景/路网/刷新/厕所 + 楼层 tab + 侧栏 320px（手机折叠 52px） |
| **功能球** | `map_ui_mode=fab` | 精简顶栏 + 左下角校徽球；次要操作收入菜单 |

功能球特性：

- **拖动 / 惯性 / 旋转 / 边界反弹**（`initFabPhysics`）
- 手机球 52px；桌面 104px
- 选功能球后选校徽：`map_fab_logo` → `xidian`（华南理工，推荐）或 `sysu`（中山大学）
- 资源：`assets/xidian-logo-512.png`、`assets/sysu-logo-512.png`
- 菜单含：选层、厕所、刷新、路网线、全景、清除、切换校徽、切换界面

### 搜索房号

- JSON label 常无房号 → 15 层 `map_data/id_map_*.json`
- 其他楼层从节点 id / label 内数字匹配

### 手机端（≤768px）

| 区域 | 经典模式 | 功能球模式 |
|------|----------|------------|
| 路径面板 | 地图**上方**折叠条；▼ 展开路线浮层；图例/房间用 bottom sheet | 同左（侧栏无 🔍） |
| 顶栏 | logo + 按钮行 + 楼层 tab | 知途 + 楼层 chip + 🔍 |
| 缩放 | Panzoom 本地 | 同左 |

桌面（>768px）：经典侧栏 320px；功能球模式保留完整顶栏 + 左下大球（104px）。

---

## 4. panorama_full.html 要点

- JPG 3000px q80，52 张 ~32 MB；`PANORAMA_CACHE_VER=20260610-compress`
- 无全屏 loader；LRU **5 场景**
- 场景热点 **35px**；房间蓝点 **14px**
- 场景热点禁止 cssClass 替代 `pnlm-scene`

---

## 5. 二维 ↔ 全景

见 [map_data/panorama_map_bridge.md](./map_data/panorama_map_bridge.md)。Bridge `?v=20260610-prefetch`。

---

## 6. A 座东侧翼

A1F 主楼 ↔ 翼内 **不互通** → 须 A2F + `stair_small`。

---

## 7. 目录要点

```
PanoramaProject/
├── .github/workflows/deploy-pages.yml
├── map.html, panorama_full.html, index.html, server_main.py
├── assets/                     # 校徽等功能球 PNG（须在此目录才能被 HTTP 服务）
├── js/panorama_map_bridge.js, js/pathfind.browser.js, js/panzoom.min.js
├── panoramas/*.jpg
├── map_data/id_map_*.json, cross_floor_links.json
├── node_nav/data/*.json
├── AGENT_HANDOFF.md, README.md, PROJECT_CONTEXT.md
└── backup/
```

外层 `indoor_navigator/` 下的 PNG 不会自动进站，需复制到 `assets/`。

---

## 8. 功能完成度

- [x] 15 层 CAD + 跨层/跨区算路 + 二维↔全景深链
- [x] GitHub Pages；map 搜索；跨区 portalModal
- [x] CAD/全景分级预取；设施与跳转节点常显
- [x] **经典 / 功能球双 UI**；校徽皮肤；可拖动功能球
- [x] 全景压缩与 LRU；边权实地走查
- [x] B1F 南侧三门路网连线（2026-06-11 修补）

---

## 9. 陷阱

1. `map.html` 仅一份 `<script>`，勿在 `</html>` 后再加 JS
2. JSON id 无前缀；map 运行时 `b1_` / `a1_` / `lk1_`
3. bump `GRAPH_CACHE_VER`（当前 `20260611-f1b-south-door-line`）、`PLAN_CACHE_VER`、bridge `?v=`、`PANORAMA_CACHE_VER`
4. 全景场景热点勿 cssClass
5. 不主动 commit/push
6. 改 graph 后跑 `verify_zone_route.py`

---

## 10. 验证

```powershell
python node_nav/scripts/verify_zone_route.py
```

- 功能球：选 fab → 校徽 → 拖动反弹；菜单切换校徽/界面
- B1F 路网线：南侧三门一线
- 手机折叠侧栏见 🔍

---

*最后更新：2026-06-11（功能球 UI + 校徽选择 + B1F graph 修补）*
