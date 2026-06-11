# Agent 交接 Prompt

将下面 **「Prompt 正文」** 整段复制到新对话的第一条消息，并按任务改 **「本次请你」** 一节。

---

## Prompt 正文（复制起点）

```
你正在接手 B7 教学楼「校园导览与信息导航系统」（课程项目「知途」）。

【产品形态】
- Web 应用（HTML + JS + Python 静态服务）
- 主入口：index.html → 自动跳转 map.html（默认 **B1F** tab）
- 辅助：panorama_full.html（52 场景全景 + 与二维深链互通）
- 公网演示：GitHub Pages；局域网：python server_main.py
- 目标用户以手机扫码为主；桌面/手机布局分离（CSS @media max-width:768px）
- **无访问统计 / 路线埋点**（纯静态站无后端）

【工作区】
- 唯一运行目录：c:\Users\yoimi\indoor_navigator\PanoramaProject
- 上级 indoor_navigator/ 下仅含 PanoramaProject/；外层校徽 PNG 需复制进 assets/ 才能被服务
- 旧杂物：PanoramaProject/backup/
- GitHub：https://github.com/linyi2134/PanoramaProject
- 勿用 file://；不要未经用户要求 commit / push
- 国内 push 优先：git push git@github.com:linyi2134/PanoramaProject.git main

【公网 / 扫码 / Pages】
- Pages 根址：https://linyi2134.github.io/PanoramaProject/
- 推荐二维码：https://linyi2134.github.io/PanoramaProject/map.html
- workflow：`.github/workflows/deploy-pages.yml` + `.nojekyll`
- Settings → Pages → Source：**GitHub Actions** → **Deploy GitHub Pages**；Actions **Read and write**
- 推送后约 1–3 分钟生效；手机强刷或无痕

【map.html · 导航核心】
- 15 tab：B1F–B5F（1–5）、连廊1F–5F（14–18）、A1F–A5F（8–12）
- JSON_GRAPHS：15 层 CAD + node_nav/data/*_graph.json 全部启用
- 合并图前缀：B `b{n}_`、A `a{n}_`、连廊 `lk{n}_`（JSON 内 id 仍无前缀）
- 懒加载：首屏仅 B1F；`loadJsonGraphsBackground()`；`floorJsonReady()` 控制未加载层不参与算路
- UI：浅蓝主题；路网边线默认隐藏；导航橙色路径始终高亮；起终点绿/红标记
- 设施节点：role=facility **默认显示橙色标注**（房间点击后 revealedLabels）
- **可跳转节点**（连廊/楼梯/电梯）：琥珀外圈 `#e8912d` + **常显标签** → portalModal
- **地点搜索**：侧栏 🔍；15 层 `map_data/id_map_*.json`
- **A1F 进入提示**：首次切 A1F 且起终点未齐 → 弹窗；localStorage `map_a1f_entry_notice_ack`
- **资源预取**：`prefetchAllCadImages()` → `runPanoramaPrefetch()`；切 tab abort 旧全景 fetch
- 竖向/跨区：`crossFloorWeight=6`；`zoneLinks=15`

【map.html · 双界面模式】（2026-06-11 新增）
- 首次进入弹窗选布局；localStorage `map_ui_mode`：`classic` | `fab`
- **经典布局**：顶栏按钮 + 横向楼层 tab + 右侧侧栏（与早期版本一致）
- **功能球模式**（手机推荐）：
  · 精简顶栏（知途 + 楼层 chip + 🔍）或桌面仍保留完整顶栏
  · 地图左下角 **校徽功能球**（可拖动、松手惯性、旋转、边界反弹）
  · 点球/轻触展开菜单：选层、厕所、刷新、路网线、全景、清除、**切换校徽**、**切换界面**
  · 桌面端功能球直径 **104px**；手机 **52px**
- 选功能球后弹 **校徽选择**；localStorage `map_fab_logo`
  · `assets/xidian-logo-512.png` → 显示名 **华南理工大学**（**推荐使用**）
  · `assets/sysu-logo-512.png` → **中山大学**
- 顶栏 **🎨 界面** 可随时切回经典 / 功能球

【CAD 底图统一尺寸】（PNG + graph x_px/y_px 已缩放；原图 plans/_archive/）
| 区域 | planWidth×Height |
|------|------------------|
| B1–B5 | 844×925 |
| 连廊1–5F | 205×624 |
| A2/A3/A4 | 933×918 |
| A1F / A5F | 816×720 / 587×709 |

重缩放：`node_nav/scripts/scale_b_plans_to_f1.py`、`scale_cad_unify.py`；改节点后 `generate_id_maps.py`

【map.html · 手机端（≤768px）】
- **顶栏选层**：左 `[B座][连廊][A座]` + 右 `[1F–5F]`（`mob-floor-nav`）；替代 15 tab 与旧 floor chip
- **路径面板在地图上方**：折叠 `[🔍] 起点 | 终点 [▼]`；展开浮层显示路线 +「图例」「本层房间」bottom sheet
- 折叠态不挡功能球；展开浮层可盖住球
- 功能球模式：顶栏「知途 + 选层 + 🔍」；侧栏 🔍 隐藏
- Panzoom：`js/panzoom.min.js` 4.5.1；切层 `resetMapZoom()`

【panorama_full.html】
- 全景 JPG ~32 MB；`PANORAMA_CACHE_VER=20260610-compress`；LRU×5；无全屏 loader
- 场景热点禁止用 cssClass 替代 `pnlm-scene`

【二维 ↔ 全景】
- `js/panorama_map_bridge.js?v=20260610-prefetch`

【A 座东侧翼】
- A1F 主楼与翼内不互通，须 A2F + `stair_small`

【必读】
- AGENT_HANDOFF.md、PROJECT_CONTEXT.md、README.md
- map_data/cross_floor_links.md、panorama_map_bridge.md、map_data/id_map_*.json

【运行】
cd PanoramaProject
python server_main.py
→ http://localhost:8000/map.html

【改 graph / map / 对照后】
- graph / cross_floor / id_map → bump `GRAPH_CACHE_VER`（当前 **20260611-f1b-south-door-line**）
- CAD PNG 缩放后 → bump `PLAN_CACHE_VER`（当前 **20260611-cad-unify-all**）
- panorama_map_bridge.js → bump `?v=`（20260610-prefetch）
- panoramas/*.jpg → bump `PANORAMA_CACHE_VER`（20260610-compress）
- 新增静态资源（校徽等）→ 放入 `assets/` 并随仓库 push

【验证】
python node_nav/scripts/verify_zone_route.py
# map：搜「133」「102」；B1 南侧三门一线（实验室门—教师办公室门—移动计算实验室）
# 功能球：选 fab 模式 → 校徽选择 → 拖动与反弹；B1 连廊琥珀圈；A1F 首次提示

【不做】BLE、Qt 客户端、独立「小楼」tab、访问统计（除非用户明确要求）

【约束】
- 中文；最小改动；改 map.html 勿在 `</html>` 后再加 JS 块
- 手机专属样式写在 `@media (max-width:768px)`；桌面功能球尺寸等在 `@media (min-width:769px)`
- 勿对已有 CAD 坐标层误跑 `apply_layout_coords.py`（会覆盖为示意坐标）

【本次请你】



完成后说明：改了哪些文件、如何验证。
```

---

## 当前进度摘要（2026-06-11 晚）

| 项 | 说明 |
|----|------|
| 二维导航 MVP | 15 tab、CAD、Dijkstra、跨层/跨区、路径高亮；默认 B1F |
| GitHub Pages | deploy-pages.yml；index → map |
| map 搜索 | 15 层 id_map + generate_id_maps.py |
| map 跨区跳转 | portalModal；琥珀圈常显 |
| map 预取 | CAD → 全景；切 tab abort |
| **双 UI 模式** | classic / fab；`map_ui_mode` |
| **功能球** | 校徽 PNG、拖动物理、菜单收纳次要操作 |
| **校徽皮肤** | 华南理工（推荐）+ 中山大学；`map_fab_logo` |
| A1F 提示弹窗 | maybeShowA1fEntryNotice |
| CAD 尺寸统一 | B 844×925；连廊 205×624；A2–A4 933×918 |
| B1F 路网修补 | 南侧三门：`teacher_room ↔ mobile_room`（三点一线） |
| 全景 | 压缩 ~32 MB；LRU×5；二维↔全景 bridge |
| 边权 / 2F-B 东侧 | 已实地走查验收 |
| **未做** | 路线热度统计、实时在线人数 |

### map.html 关键符号

| 符号/函数 | 作用 |
|-----------|------|
| `resolveUiMode` / `applyUiMode` | 经典 vs 功能球布局 |
| `initFabPhysics` / `FAB_PHYS` | 功能球拖动、惯性、反弹、旋转 |
| `showFabLogoPicker` / `FAB_LOGOS` | 校徽选择 |
| `switchFloor` / `maybeShowA1fEntryNotice` | 切层；A1F 首次提示 |
| `loadRoomSearchAliases` / `ID_MAP_FILES` | 15 层搜索别名 |
| `offerPortalModal` / `jumpToPortalOption` | 跨区/换层弹窗 |
| `prefetchAllCadImages` / `runPanoramaPrefetch` | 预取队列 |
| `GRAPH_CACHE_VER` / `PLAN_CACHE_VER` | 强刷 JSON / id_map / CAD |

### localStorage 键

| 键 | 含义 |
|----|------|
| `map_ui_mode` | `classic` 或 `fab` |
| `map_fab_logo` | `xidian`（华南理工图）或 `sysu`（中山大学图） |
| `map_a1f_entry_notice_ack` | A1F 进入提示已读 |

### 静态资源

| 路径 | 说明 |
|------|------|
| `assets/xidian-logo-512.png` | 华南理工大学校徽（功能球默认推荐） |
| `assets/sysu-logo-512.png` | 中山大学校徽 |

外层 `indoor_navigator/*.png` 不会直接被 `server_main.py` 提供，需复制到 `assets/`。

### 工具脚本

| 脚本 | 用途 |
|------|------|
| `generate_id_maps.py` | 生成 15 层 id_map |
| `scale_b_plans_to_f1.py` | B 座 CAD 统一 844×925 |
| `scale_cad_unify.py` | 连廊、A3/A4 缩放 |
| `verify_zone_route.py` | 跨区路线 |
| `compress_panoramas.py` | 全景压缩 |

### 部署

```powershell
git push git@github.com:linyi2134/PanoramaProject.git main
```

Actions 看 **Deploy GitHub Pages**。

---

## 验证命令速查

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py
python node_nav/scripts/verify_zone_route.py
```

**手动测例**

1. 默认 B1F；搜「133」「102」跳层算路
2. 选 **功能球模式** → 校徽选择（华南理工推荐）→ 拖动球、松手惯性、撞边反弹
3. 功能球菜单「切换校徽」「切换界面样式」
4. B1F 开启路网线 → 南侧 `实验室门 — 教师办公室门 — 移动计算与软件实验室` 三点一线
5. 切 A1F（起终点未齐）→ 进入提示 →「我已知晓」
6. B1 连廊口琥珀圈 → 连廊1F；电梯上/下楼
7. 公网手机强刷：https://linyi2134.github.io/PanoramaProject/map.html

**清除界面记忆（调试）**

```js
localStorage.removeItem('map_ui_mode');
localStorage.removeItem('map_fab_logo');
location.reload();
```

---

## 给 Agent 的提醒

1. PowerShell 用 `;` 不用 `&&`
2. JSON id 无前缀；map 运行时 `b1_` / `a1_` / `lk1_`
3. 不主动 commit/push
4. 全景热点勿 cssClass 替代 pnlm-scene
5. 功能球物理与校徽列表在 `map.html` 内联 JS，无独立 CSS 文件
6. 改 `node_nav/data/f1_b_graph.json` 等 graph 后务必 bump `GRAPH_CACHE_VER`

---

*最后更新：2026-06-11 · 含功能球 UI、校徽选择、B1F 南门连线修复*
