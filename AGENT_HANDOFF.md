# Agent 交接 Prompt

将下面 **「Prompt 正文」** 整段复制到新对话的第一条消息，并按任务改 **「本次请你」** 一节。

---

## Prompt 正文（复制起点）

```
你正在接手 B7 教学楼「校园导览与信息导航系统」（课程项目「知途」）。

【产品形态】
- Web 应用（HTML + JS + Python 静态服务），不是 Qt 客户端
- 主入口：index.html → 自动跳转 map.html（二维 CAD + Dijkstra + 路径高亮）
- 辅助：panorama_full.html（52 场景全景 + 与二维深链互通）
- 公网演示：GitHub Pages（见下）；局域网演示仍可用 python server_main.py
- 目标用户以手机扫码为主；桌面端布局与手机端分离（CSS 媒体查询 ≤768px）

【工作区】
- 唯一运行目录：c:\Users\yoimi\indoor_navigator\PanoramaProject
- 上级 indoor_navigator/ 下仅含 PanoramaProject/；旧杂物在 PanoramaProject/backup/
- GitHub：https://github.com/linyi2134/PanoramaProject
- 勿用 file://；不要未经用户要求 commit / push

【公网 / 扫码】
- Pages 根址：https://linyi2134.github.io/PanoramaProject/
- 推荐二维码内容（静态网址码）：
  · 二维导航：https://linyi2134.github.io/PanoramaProject/map.html
  · 或根目录（经 index.html 跳转）：https://linyi2134.github.io/PanoramaProject/
- 全景入口勿做默认扫码（单图 ~8MB 较慢）；从 map 顶栏「全景（可选）」进入
- Pages 推送后约 1–3 分钟生效；手机需强刷或无痕窗口验证

【map.html · 2026-06-10 现状】
- 15 tab：B1F–B5F（1–5）、连廊1F–5F（14–18）、A1F–A5F（8–12）
- JSON_GRAPHS：15 层 CAD + node_nav/data/*_graph.json 全部启用
- 合并图前缀：B b{n}_、A a{n}_、连廊 lk{n}_（JSON 内仍无前缀原 id）
- 加载策略：首屏仅 B1F JSON；其余分批后台 loadJsonGraphsBackground()；floorJsonReady() 控制未加载层不参与算路
- UI：浅蓝浅色主题；路网边线默认隐藏；导航橙色路径始终显示；起终点绿/红标记
- 竖向/跨区：crossFloorWeight=6；zoneLinks=15；同层禁竖向边（A1F 翼/主楼例外）

【map.html · 手机端（@media max-width:768px，桌面不受影响）】
- 顶栏高度约减 1/4（min-height 66px）；标题/按钮/tab 字号缩小
- 右侧栏改为浮层（position:absolute），不挤压地图宽度
- 侧栏默认折叠（48px）：仅显示「起点」「终点」；点 ◀/▶ 展开
- 展开宽 160px（原 320px 的 50%）：图例、房间列表、路径结果；仍叠在地图上
- 房间标注默认隐藏；点击节点后永久显示（revealedLabels Set）；起终点自动显示
- 缩放：@panzoom/panzoom 4.5.1（CDN）；双指 pinch / 滚轮；右下角 ＋－⟳；切层 resetMapZoom()
- 关键函数：initMobileSide()、initMapPanzoom()、revealNodeLabel()、resetMapZoom()

【panorama_full.html · 近期已改】
- 最近 3 场景 LRU 缓存（非每次 destroy 单图）；切换加载提示；快速连点防抖
- 右上导航面板可拖动、可折叠（位置存 localStorage）
- 场景跳转热点：buildSceneHotspots() 用 type:"scene" + clickHandlerFunc→switchToScene（LRU）
  · 禁止对场景热点用 cssClass（会去掉 pnlm-sprite，图标消失或变 info「i」）
  · 禁止设 sceneId 于 config（会绕过 LRU）；CSS .pnlm-hotspot-base.pnlm-scene 放大雪碧图 5×（130px）
- 房间蓝点：cssClass room-info-hotspot，42px 自绘（不用 Pannellum info 图标）

【二维 ↔ 全景 · 已打通】
- 对照表：js/panorama_map_bridge.js + map_data/panorama_map_bridge.md
- 二维：有对照节点 → 弹窗 → panorama_full.html?scene=…
- 全景：侧栏「二维地图（…）」→ map.html?start=…
- 三栋 1–3F → a{n}_stair_small；房间蓝点与走廊对照独立

【A 座东侧翼】
- A1F 主楼与翼内不互通，须 A2F + stair_small；f1_a 单层 check_graph 可能 FAIL

【必读】
- AGENT_HANDOFF.md、PROJECT_CONTEXT.md、README.md
- map_data/panorama_map_bridge.md、cross_floor_links.md
- map_data/README.md、node_nav/data/README.md、panorama_data/README.md

【运行】
cd PanoramaProject
python server_main.py
→ http://localhost:8000/map.html
→ http://localhost:8000/panorama_full.html

【改 graph / map / 对照后】
- 改 graph 或 cross_floor_links → bump map.html GRAPH_CACHE_VER（当前 20260610-fix-load）
- 改 panorama_map_bridge.js → bump bridge ?v=（当前 20260609-san）
- pathfind.browser.js ?v=20260609；改 map 纯 UI 可不 bump；改后 Ctrl+F5

【验证】
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
# map 桌面：B1 room137 → A1 office101（经连廊）；A1 主楼 → room_104（经 A2F）
# map 手机：首屏地图占满宽；侧栏默认窄条；展开不挤地图；双指缩放可用
# 全景：场景热点为白圈绿箭头（非 i）；点击可切场景；房间蓝点 42px

【待办 · 建议优先级】
1. 边权实地丈量（同层边、zoneLinks 等）
2. 清理 cross_floor_links.json 内 campusCrossFloor 废弃字段
3. 2F-B 东侧动线（237/234/236，草稿 backup/indoor_navigator_misc/2F-B座.json）
4. 可选：全景图压缩；Panzoom 改本地 js/ 离线包；二栋-xf-5 电梯区全景对照

不做：BLE、Qt 客户端、恢复独立「小楼」tab

【约束】
- 中文；最小改动；改 map.html 勿在 </html> 后再加 JS 块
- 手机布局只写在 @media (max-width:768px) 内，勿破坏桌面 320px 侧栏
- 全景场景热点勿用 cssClass 替代 pnlm-scene 雪碧图

【本次请你】


完成后说明：改了哪些文件、如何验证、对应哪条待办。
```

---

## 当前进度摘要（2026-06-10）

### 已完成

| 项 | 说明 |
|----|------|
| 二维导航 MVP | 15 tab、CAD、Dijkstra、跨层/跨区、路径高亮 |
| **GitHub Pages** | 已推送；index.html 直达 map；静态码可扫码 |
| **map 体验** | 浅蓝主题；懒加载；首屏不卡死 |
| **map 手机端** | 顶栏压缩；侧栏默认折叠浮层；Panzoom 缩放；点击显示房间名 |
| **map 桌面端** | 320px 固定侧栏；较大字号与顶栏（>768px 不受影响） |
| **A1F 路网** | a_door  reposition；f1_a 主楼边重画 |
| **全景性能** | 3 场景 LRU；可拖动/折叠导航面板 |
| **全景热点** | 场景 type:scene + LRU 跳转；房间蓝点 42px；雪碧图箭头 5× |
| 二维↔全景 | bridge + 双向深链（B/A/连廊/三栋） |
| 同层算路 | 同 tab 禁竖向边；A1F 翼/主楼例外 |

### 待办

1. 同层与跨区边权实地丈量
2. 清理 `cross_floor_links.json` 内 `campusCrossFloor` 废弃字段
3. 2F-B 东侧动线合并（草稿在 backup）
4. 可选：全景 JPG 压缩；Panzoom 本地化；二栋 `-5` 电梯全景对照

### map.html 关键符号

| 符号/函数 | 作用 |
|-----------|------|
| `floorJsonReady` / `loadJsonGraph` | 分层懒加载；未就绪层不参与算路 |
| `buildGraph` + `sameFloorVerticalPolicy` | 合并图；同层竖向边过滤 |
| `crossEdges` | 跨层/跨区边 |
| `revealedLabels` / `revealNodeLabel` | 点击节点后显示房间标注 |
| `initMapPanzoom` / `resetMapZoom` | SVG 缩放平移；切层重置 |
| `initMobileSide` | 手机侧栏折叠/展开（≤768px） |
| `GRAPH_CACHE_VER` | 强刷 JSON / cross_floor_links |

### panorama_full.html 关键符号

| 符号/函数 | 作用 |
|-----------|------|
| `buildSceneHotspots` | 场景热点；type scene + clickHandlerFunc，**无 cssClass** |
| `switchToScene` | LRU 切场景；含 destroy/recreate |
| `addRoomHotspotsForScene` | 房间蓝点；cssClass room-info-hotspot |

### 文件对照

| 用途 | 路径 |
|------|------|
| 扫码入口 | `index.html` → `map.html` |
| 二维导航 | `map.html` |
| 全景 | `panorama_full.html`（非 panorama.html demo） |
| 二维↔全景 | `js/panorama_map_bridge.js`、`map_data/panorama_map_bridge.md` |
| 路网 | `node_nav/data/*.json` |
| 校验 | `verify_zone_route.py`、`audit_vertical_links.py`、`check_graph.py` |

---

## 常见任务模板

### A. 补拓扑 / 改边权

改 `node_nav/data/*.json` → 校验脚本 → bump `GRAPH_CACHE_VER` → map Ctrl+F5。

### B. 新楼层坐标

pick-coords 导出 → `apply_cad_coords.py` → 确认 `JSON_GRAPHS` 含该 tab。

### C. 改 map 交互 / 手机布局

只改 `map.html` 内一份 `<script>` 与 `<style>`；手机样式放 `@media (max-width:768px)`；测桌面侧栏 320px 未被破坏。

### D. 改全景热点

场景跳转改 `buildSceneHotspots`（勿 cssClass）；房间改 `addRoomHotspotsForScene`；勿动 hundreds 条 scenesConfig 坐标除非必要。

### E. 增删二维↔全景对照

改 `panorama_map_bridge.js` → bump bridge `?v=` → 按 `panorama_map_bridge.md` 测深链。

---

## 验证命令速查

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
```

**map / Pages 手动测例**

1. 打开根址或 map.html：数秒内出现 B1F，不卡在「正在加载地图…」
2. B1 `room137_front` → A1 `office101_front`（经连廊）
3. A1 主楼 → `room_104A`（经 A2F + stair_small）
4. **手机**：Chrome 设备模拟 ≤768px — 地图全宽；侧栏 48px 仅起终点；展开 160px 浮层；双指/滚轮缩放
5. **全景**：场景热点白圈绿箭头；点击切场景；房间蓝点可见

---

## 给 Agent 的提醒

1. Windows + PowerShell；`&&` 不可用，用 `;`
2. `panorama_full.html` 才是完整版（`panorama.html` 仅 5 场景 demo）
3. JSON 无前缀 / map 有前缀 — 改 zoneLinks 时注意 tab 与 nodeId
4. f1_a 单层 check_graph 可能 FAIL — 预期（翼内子图孤立）
5. 连廊 tab 14–18 无 FLOORS 回退，必须等 JSON 加载
6. 全景场景热点：**cssClass 与 pnlm-sprite 互斥** — 场景用 type:scene，房间用 room-info-hotspot
7. Panzoom 依赖 unpkg CDN；离线环境需改本地 `js/panzoom.min.js`
8. 不主动 commit/push

---

*最后更新：2026-06-10*
