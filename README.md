# PanoramaProject · 校园导览与信息导航系统

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Course%20Project-lightgrey)]()
[![GitHub](https://img.shields.io/badge/GitHub-linyi2134%2FPanoramaProject-181717?logo=github)](https://github.com/linyi2134/PanoramaProject)

B7 教学楼室内导航课程项目 **「知途」**：**二维 CAD 地图 + Dijkstra 路径规划**为主，**360° 全景漫游**为辅。

> 仓库：[github.com/linyi2134/PanoramaProject](https://github.com/linyi2134/PanoramaProject)  
> 本地路径：`c:\Users\yoimi\indoor_navigator\PanoramaProject`（**仅在此目录启动服务**）

---

## 功能一览

| 模块 | 状态 | 说明 |
|------|------|------|
| **二维地图导航** | ✅ | `index.html`→`map.html`：15 层 tab、浅蓝 UI、懒加载、跨层/跨区算路 |
| **地点搜索** | ✅ | 侧栏 🔍：房号/名称模糊匹配 → 跳层设终点并算路 |
| **手机端优化** | ✅ | 折叠侧栏 52px（含搜索图标）、Panzoom、设施常显标注 |
| **跨区跳转** | ✅ | 连廊口/楼梯/电梯：琥珀圈常显 → 弹窗跳转对应区域或上/下楼 |
| **资源预取** | ✅ | 先 15 张 CAD → 当前层全景 → 其余层；切 tab 取消旧全景下载 |
| **GitHub Pages** | ✅ | 自定义 Actions 部署；https://linyi2134.github.io/PanoramaProject/ |
| **二维↔全景深链** | ✅ | `js/panorama_map_bridge.js`：走廊节点对照 + 双向 URL 跳转 |
| 全景完整版 | ✅ | `panorama_full.html`：52 场景、LRU×5、已压缩 JPG（~32 MB 合计） |
| 全景 demo | ✅ | `panorama.html`：5 场景入门 |
| CAD 取点 | ✅ | `tools/pick-coords.html` + `apply_cad_coords.py` |
| 路网校验 | ✅ | `check_graph.py`、`verify_zone_route.py` |
| 竖向边审计 | ✅ | `audit_vertical_links.py`（楼梯/电梯分组） |
| 边权 | ✅ | 跨层 **每层 +6**；同层/跨区边权已实地走查 |
| 自动定位 | ⏸ | 不做 BLE/WiFi；公网扫码或局域网演示 |

### map.html 要点（2026-06-11）

- **Tab 标签**：B1F–B5F、连廊1F–5F、A1F–A5F
- **地点搜索**：侧栏 🔍 → 房号/名称 → 跳层设终点并算路
- **可跳转节点**：连廊口、电梯、各楼梯 — **琥珀色外圈 + 常显标签**；点击可选跳转到 B/连廊/A 或上/下楼，也可进全景或继续选点
- **设施标注**：洗手间等 **默认显示**（橙色）；普通房间点击后显示
- **资源预取**：先缓存 15 张 CAD 底图，再拉当前层全景，最后依次其它层；切换 tab 会取消进行中的全景下载
- **顶栏全景**：红色「🌐 全景」；对照节点另有蓝虚线圈
- **路网边线**：默认隐藏；**导航路径始终高亮**
- **跨层/跨区**：`crossFloorWeight: 6`；`zoneLinks: 15`；无 B-A 直连
- **手机端（≤768px）**：折叠侧栏 52px + Panzoom

---

## 技术栈

| 层次 | 技术 |
|------|------|
| 地图 UI | HTML + SVG + `js/pathfind.browser.js` |
| 地图缩放 | [@panzoom/panzoom](https://github.com/timmywil/panzoom) 4.5.1（`js/panzoom.min.js`） |
| 全景 | Pannellum 2.5.6（CDN） |
| 服务 | Python `http.server`（`server_main.py`，端口 8000） |
| 单层算路 CLI | `indoor_nav/`（Dijkstra） |
| 数据 | JSON（`nodes` / `edges` / `facilities` / `x_px` / `y_px`） |
| 打包 | PyInstaller（可选） |

---

## 项目结构

```
PanoramaProject/
├── server_main.py              # 本地 HTTP 服务（默认打开 map.html）
├── index.html                  # 扫码入口 → 跳转 map.html
├── map.html                    # ★ 二维导航主页面
├── panorama_full.html          # 全景 52 场景
├── panorama.html               # 全景 5 场景 demo
├── js/
│   ├── pathfind.browser.js     # 浏览器 Dijkstra（与 indoor_nav 同逻辑）
│   ├── panorama_map_bridge.js  # 二维节点 ↔ 全景场景对照
│   ├── panzoom.min.js          # 手机端地图缩放（4.5.1）
│   └── room_labels_all.js      # 全景房间标注
├── plans/                      # 15 张 *_cad.png（map 底图）
│   └── _archive/               # 旧示意 PNG/SVG（已不用）
├── .github/workflows/deploy-pages.yml  # GitHub Pages 发布
├── .nojekyll                   # 静态站（不走 Jekyll）
├── map_data/
│   ├── cross_floor_links.json  # 跨层/跨区定义（已无 campusCrossFloor）
│   ├── panorama_map_bridge.md  # 二维↔全景对照表（权威）
│   ├── id_map_*.json           # 15 层节点对照 + 搜索别名
│   ├── cad_pick_*.json         # pick-coords 导出归档
│   └── README.md
├── node_nav/
│   ├── data/                   # f*_graph.json、link_f*_graph.json（15 层）
│   └── scripts/                # check_graph、verify_zone_route、compress_panoramas.py…
├── panoramas/                  # 52 张全景 JPG（已压缩 ~32 MB；原图 backup/panoramas_original/）
├── indoor_nav/                 # python -m indoor_nav route …
├── tools/pick-coords.html      # CAD 拖点取坐标
├── backup/                     # 归档（外层杂物、旧 graph、备份 JS）→ 见 backup/README.md
├── AGENT_HANDOFF.md            # Agent 交接 Prompt（新对话复制用）
├── PROJECT_CONTEXT.md          # 项目上下文速览
└── README.md                   # 本文件
```

---

## 快速开始

### 环境

- Python **3.10+**
- 现代浏览器（Chrome / Edge / Firefox）

### 启动

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py
```

| URL | 用途 |
|-----|------|
| https://linyi2134.github.io/PanoramaProject/ | **公网扫码（推荐）** |
| http://localhost:8000/map.html | 本地二维导航 |
| http://localhost:8000/panorama_full.html | 全景完整版 |
| http://localhost:8000/tools/pick-coords.html | CAD 取点 |

⚠️ 勿用 `file://` 打开 HTML；勿在上级 `indoor_navigator/` 目录启动服务。

### 命令行试算（单层，JSON 内无前缀 id）

```powershell
python -m indoor_nav route node_nav/data/f1_b_graph.json room137_front washroom
python -m indoor_nav nearest node_nav/data/f1_b_graph.json 洗手间 room137_front
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/check_graph.py node_nav/data/f3_b_graph.json
```

跨层/跨区仅在 **map.html** 或 **verify_zone_route.py** 中验证（运行时带 `b`/`a`/`lk` 前缀）。

---

## 路网与算路

- **单层文件**：`node_nav/data/f{1..5}_{a|b}_graph.json`、`link_f{1..5}_graph.json`
- **map 合并图**：15 层加载 → `buildGraph()` + `crossEdges()` → Dijkstra
- **前缀规则**（仅 map 运行时）：B `b{n}_`、A `a{n}_`、连廊 `lk{n}_`；JSON 文件内 id **无前缀**
- **规范**：见 [node_nav/data/README.md](node_nav/data/README.md)
- **跨层/跨区**：见 [map_data/cross_floor_links.md](map_data/cross_floor_links.md)

### 重要设计约束 · A 座东侧翼

- 无独立「小楼」建筑；东侧翼属 A 座一部分
- **A1F 主楼 ↔ 东侧翼 1F 不互通**；须 **A2F** 通道 + `stair_small` 竖井
- `stair_small` 仅跨 A1F–A3F；`stair_south` 跨 A1F–A5F

---

## 修改后记得

1. 改 graph 或 `cross_floor_links.json` → bump `map.html` 的 **`GRAPH_CACHE_VER`**（当前 `20260610-clean-cf`）
2. 改 `panorama_map_bridge.js` → bump bridge **`?v=`**（当前 `20260610-prefetch`）
3. 改 `panoramas/*.jpg` → bump `PANORAMA_CACHE_VER`（`20260610-compress`）+ 强刷
4. 浏览器 **Ctrl+F5** 强刷

---

## 公网扫码与本地演示

**推荐（永久）**：GitHub Pages 已开启。二维码用**静态网址码**，内容填：

```
https://linyi2134.github.io/PanoramaProject/map.html
```

项目更新后同一二维码自动生效。推送后 Actions 跑 **Deploy GitHub Pages**（约 1–3 分钟），手机请强刷或无痕打开。若内置 `pages-build-deployment` 失败/卡 Queued，以 `.github/workflows/deploy-pages.yml` 为准。

**本地局域网**：`python server_main.py` 后用手机访问 `http://<电脑局域网IP>:8000/map.html`（勿用 localhost）。

**打包 exe**（可选）：`pip install pyinstaller` → `python build_exe.py`

---

## 文档索引

| 文档 | 说明 |
|------|------|
| [AGENT_HANDOFF.md](AGENT_HANDOFF.md) | **Agent 交接 Prompt + 进度 + 验证** |
| [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) | 架构与陷阱速览 |
| [map_data/README.md](map_data/README.md) | CAD / pick-coords / apply 流程 |
| [map_data/cross_floor_links.md](map_data/cross_floor_links.md) | 竖向井分组、跨区 |
| [map_data/panorama_map_bridge.md](map_data/panorama_map_bridge.md) | **二维↔全景对照表** |
| [panorama_data/README.md](panorama_data/README.md) | 全景房间标注 |
| [backup/README.md](backup/README.md) | 归档目录说明 |

---

## 参与贡献

1. 改路网：编辑 `node_nav/data/*.json`，勿动 `backup/graph_archive/` 内历史文件
2. 改 map 交互：只改 `map.html` 内 **一份** `<script>`，勿在 `</html>` 后再加 JS
3. 提交 PR 前：`check_graph.py` + `verify_zone_route.py` + map 手动测例

---

## 许可证

课程实践项目，全景与楼内数据仅供教学演示。第三方库遵循各自许可证。

<p align="center"><sub>知途 · IT创新实践导论 · B7 软件学院</sub></p>
