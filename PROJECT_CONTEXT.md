# PROJECT_CONTEXT · B7 校园导览与信息导航系统

> 供新对话 / 新 agent 快速接手。仓库路径：`c:\Users\yoimi\indoor_navigator\PanoramaProject`  
> GitHub：[linyi2134/PanoramaProject](https://github.com/linyi2134/PanoramaProject)

---

## 1. 项目是什么

**课程项目「知途」**：B7 教学楼室内导览与导航。

- **主产品方向**：二维地图 + 用户选起点/终点 + Dijkstra 最短路径 + 路径展示  
- **辅助**：360° 全景漫游（Pannellum），可选进入  
- **不做**：Qt/OpenGL、BLE/WiFi 自动室内定位（用手动选点/搜索，可选二维码）

---

## 2. 技术栈（已定型）

| 组件 | 技术 |
|------|------|
| 本地服务 | Python 3.10+ `http.server`（`server_main.py`，端口 **8000**） |
| 二维地图 UI | `map.html`（组员贡献，已接入） |
| 全景 | `panorama.html` + Pannellum CDN |
| 算路 | Dijkstra，三处同逻辑：`indoor_nav/`、`node_nav/src/pathfind.js`、`js/pathfind.browser.js` |
| 路网数据 | JSON：`nodes` / `edges` / `facilities` |
| 打包 | `build_exe.py` + PyInstaller（含 map + panorama） |

---

## 3. 如何运行（必读）

```powershell
cd C:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py
```

- **地图导航（默认打开）**：http://localhost:8000/map.html（13 层 + 跨楼）  
- **全景完整版**：http://localhost:8000/panorama_full.html（52 场景）  
- **全景 demo**：http://localhost:8000/panorama.html  

⚠️ 必须在 `PanoramaProject` 目录下启动；**不要**在 `indoor_navigator` 根目录跑 `server_main.py`。  
⚠️ 不要 `file://` 直接打开 HTML，否则 `js/pathfind.browser.js` 等相对路径会失败。

**命令行试算（Python）：**

```powershell
python -m indoor_nav route node_nav/data/f1_b_graph.json room137_front washroom
python -m indoor_nav nearest node_nav/data/f1_b_graph.json 洗手间 room137_front
```

---

## 4. 目录结构（关键文件）

```
PanoramaProject/
├── server_main.py              # 入口；默认打开 map.html
├── map.html                    # 二维导航主入口（13 层 + PNG/JSON 试点）
├── panorama_full.html          # 全景完整版（52 场景，panoramas/）
├── panorama.html               # 全景 demo（5 场景）
├── panoramas/                  # 完整版全景 jpg
├── js/pathfind.browser.js      # 浏览器 Dijkstra（无 export）
├── indoor_nav/                 # Python 算路包
├── node_nav/
│   ├── data/
│   │   ├── index.json          # 10 层图索引
│   │   ├── f1_a_graph.json … f5_b_graph.json
│   │   ├── README.md           # JSON 字段规范
│   │   └── _archive/           # 整理前旧文件名
│   ├── src/pathfind.js
│   └── scripts/normalize_graphs.py
├── map_data/README.md          # 两套数据并存说明
├── plans/                      # （待建）PNG 平面图
├── 1F(1).dwg, 1F(1).pdf        # CAD/PDF 源图（根目录）
├── 3F(1).dwg, 3F(3).pdf
├── README.md
├── 二维地图主导-分阶段推进方案.md
├── 扩展方案与技术栈建议.md
└── build_exe.py
```

---

## 5. 两套「地图/路网」数据（重要）

当前 **并存、未合并**：

| 来源 | 位置 | 特点 |
|------|------|------|
| **示意图 H5** | `map.html` → `FLOORS` | SVG viewBox **760×520**；节点 id 如 `f1_wash`；含 x,y；可点击、画路径、跨层 |
| **实地路网 JSON** | `node_nav/data/f*_graph.json` | 命名 `f{层}_{a\|b}_graph.json`；id 如 `washroom`、`room137_front`；**多数无 x_px/y_px**；`isFinished: false` |

- 演示/交互：**优先 `map.html`**  
- 课程数据、Python 校验、未来 PNG 底图：**以 JSON 为准**  
- 合并需 **id 对照表** + 坐标迁移（见第 7 节）

---

## 6. JSON 数据规范（摘要）

见 `node_nav/data/README.md`。

- 顶层：`description`, `isFinished`, `meta`, `nodes`, `edges`, `facilities`  
- `meta`：`building`（B7）, `floor`, `zone`（A/B）, `units`（meter）  
- 节点 `id`：**snake_case**，无空格  
- 边：无向，`weight` 为步行距离（米）  
- **计划增加**（PNG 方案）：`meta.planImage`, `planWidth`, `planHeight`, 节点 `x_px`, `y_px`

整理脚本：`python node_nav/scripts/normalize_graphs.py`

---

## 7. 已确认的坐标方案（组内决议）

1. **底图**：各层导出 **PNG**（来自 DWG/PDF，或暂用组员 SVG 示意导出）  
2. **坐标**：节点上 **`x_px` / `y_px`**（相对 PNG 左上角像素）  
3. **若 PNG 与 `map.html` 示意图同为 760×520 且内容一致** → 可直接把 `FLOORS` 里的 `x,y` 抄为 `x_px,y_px`  
4. **若 PNG 来自真实 CAD 平面图** → **不能**照搬 H5 坐标，需重新标点（或 pick-coords 工具）  
5. 交互也可继续用 **HTML 按钮/点击 SVG 节点**，坐标不必全进 JSON，但画路径仍需节点有位置

---

## 8. 已完成 vs 待办

### 已完成

- [x] 全景多场景 + 热点（`panorama.html`）  
- [x] 10 份 A/B 分层 JSON + `index.json` + 规范化脚本  
- [x] Python `indoor_nav` + JS `pathfind.js` + 命令行/Node 示例  
- [x] `map.html` 接入：`pathfind.browser.js`、修复文件损坏、3F/4F 数据合并、与 panorama 互链  
- [x] `server_main` 默认 map 入口；README、方案文档、GitHub 推送  

### 进行中 / 待办

- [x] 合并 final_map → `map.html`（13 层 + 跨楼）  
- [x] 全景完整版 → `panorama_full.html` + `panoramas/`  
- [ ] 2F–5F：`id_map` + `x_px/y_px` + `JSON_GRAPHS` 逐层启用  
- [ ] 校验各层 `edges` 连通性与 `isFinished`  
- [ ] 可选：`pick-coords.html`（CAD 底图标点）  
- [ ] 可选：二维房间 ↔ 全景场景绑点  

---

## 9. 已知问题 / 陷阱

1. **`map.html` 曾出现 `</html>` 后重复 JS 块** — 已截断；改文件时注意只保留一份 `FLOORS`  
2. **跨层边** — 仅 `stN`/`stS` 楼梯对；曾误引 `f*_elev`（无节点）已删  
3. **1F-A 等 JSON 边较少** — 连通性未校完，算路可能失败  
4. **`3F(1).dwg` 与 `3F(3).pdf` 文件名不一致** — 需确认是否同一版  
5. **README 功能表** 中「二维地图页」状态可能滞后 — 实际已有 `map.html` MVP  

---

## 10. 文档索引

| 文件 | 内容 |
|------|------|
| `README.md` | GitHub 风格项目说明 |
| `node_nav/data/README.md` | 路网 JSON 规范 |
| `map_data/README.md` | map.html vs JSON 双轨说明 |
| `二维地图主导-分阶段推进方案.md` | 分阶段产品路线 |
| `扩展方案与技术栈建议.md` | 技术选型 |
| `下周工作可行性方案-平面图与地图MVP.docx` | PNG / map / 坐标可行性（Word） |

---

## 11. Git 与协作

- 远程：`https://github.com/linyi2134/PanoramaProject.git`，分支 `main`  
- 近期 commit 含：graph 规范化、README、可行性 docx；**map 接入改动可能尚未 push**（接手后 `git status` 确认）  
- 用户要求：**不要未经询问就 commit/push**

---

## 12. 组员与分工背景

- 用户（洪泽杰侧）集中整理仓库、JSON 规范、Python 算路、GitHub  
- 组员提供 `map.html`（SVG 示意 + 交互）  
- 组内会议结论：主入口二维地图；坐标用 PNG+xy；可不批量标 JSON 若用 H5 按钮选点，但画线仍需位置信息  

---

*最后更新：对话交接前。修改本文件时请同步 README 中过时的「二维地图状态」。*
