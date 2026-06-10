# Agent 交接 Prompt

将下面 **「Prompt 正文」** 整段复制到新对话的第一条消息，并按任务改「本次请你」一节。

---

## Prompt 正文（复制起点）

```
你正在接手 B7 教学楼「校园导览与信息导航系统」（课程项目「知途」）。

【产品形态】
- Web 应用（HTML + JS + Python 静态服务），不是 Qt 客户端
- 主入口：index.html → 自动跳转 map.html（二维 CAD + Dijkstra + 路径高亮）
- 辅助：panorama_full.html（52 场景全景 + 与二维深链互通）
- 公网演示：GitHub Pages（见下）；局域网演示仍可用 python server_main.py

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

【map.html · 2026-06-10 现状】
- 15 tab：B1F–B5F（1–5）、连廊1F–5F（14–18）、A1F–A5F（8–12）
- JSON_GRAPHS：15 层 CAD + node_nav/data/*_graph.json 全部启用
- 合并图前缀：B b{n}_、A a{n}_、连廊 lk{n}_（JSON 内仍无前缀原 id）
- 加载策略：首屏仅 B1F JSON；其余分批后台加载；floorJsonReady() 控制未加载层不参与算路
- UI：浅蓝浅色主题；路网边线默认隐藏；导航橙色路径始终显示；起终点绿/红标记
- 竖向/跨区：crossFloorWeight=6；zoneLinks=15；同层禁竖向边（A1F 翼/主楼例外）

【A1F 路网 · 近期已改】
- A区大门 a_door 坐标已下移（相对休息区 + 全图高 1/12）
- f1_a 主楼边已重画（小楼 room_104* / stair_small 子图仍孤立）；权重参照 A2F 缩放

【panorama_full.html · 近期已改】
- 最近 3 场景 LRU 缓存（非每次 destroy 单图）
- 切换时加载提示；快速连点有防抖
- 右上导航面板可拖动、可折叠（位置存 localStorage）

【二维 ↔ 全景 · 已打通】
- 对照表：js/panorama_map_bridge.js + map_data/panorama_map_bridge.md
- 二维：有对照节点 → 弹窗 → panorama_full.html?scene=…
- 全景：侧栏「二维地图（…）」→ map.html?start=…
- 三栋 1–3F → a{n}_stair_small；房间蓝点与走廊对照独立

【A 座东侧翼】
- A1F 主楼与翼内不互通，须 A2F + stair_small；f1_a 单层 check_graph 可能 FAIL

【必读】
- AGENT_HANDOFF.md、PROJECT_CONTEXT.md
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
- pathfind.browser.js ?v=20260609；改后 Ctrl+F5

【验证】
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
# map：B1 room137 → A1 office101（经连廊）；A1 主楼 → room_104（经 A2F）
# 扫码/Pages：根址或 map.html 首屏不卡死、可切层算路

【待办 · 建议优先级】
1. 边权实地丈量（同层边、zoneLinks 等）
2. 清理 cross_floor_links.json 内 campusCrossFloor 废弃字段
3. 2F-B 东侧动线（237/234/236，草稿 backup/indoor_navigator_misc/2F-B座.json）
4. 可选：全景图压缩以改善手机加载；二栋-xf-5 电梯区全景对照

不做：BLE、Qt 客户端、恢复独立「小楼」tab

【约束】中文；最小改动；改 map.html 勿在 </html> 后再加 JS 块

【本次请你】


完成后说明：改了哪些文件、如何验证、对应哪条待办。
```

---

## 当前进度摘要（2026-06-10）

### 已完成

| 项 | 说明 |
|----|------|
| 二维导航 MVP | 15 tab、CAD、Dijkstra、跨层/跨区、路径高亮 |
| **GitHub Pages** | 仓库已推送；index.html 直达 map；静态码可扫码 |
| **map 体验** | 浅蓝主题；懒加载修复（floorJsonReady）；首屏不卡死 |
| **A1F 路网** | a_door  reposition；f1_a 主楼边重画；权重按 A2F 缩放 |
| **全景性能** | 3 场景 LRU；可拖动/折叠导航面板；加载提示 |
| 二维↔全景 | bridge + 双向深链（B/A/连廊/三栋） |
| 同层算路 | 同 tab 禁竖向边；A1F 翼/主楼例外 |

### 待办

1. 同层与跨区边权实地丈量
2. 清理 `cross_floor_links.json` 内 `campusCrossFloor` 废弃字段
3. 2F-B 东侧动线合并（草稿在 backup）
4. 可选：全景 JPG 压缩；二栋 `-5` 电梯全景对照

### map.html 关键符号

| 符号/函数 | 作用 |
|-----------|------|
| `floorJsonReady` / `loadJsonGraph` | 分层懒加载；未就绪层不参与算路 |
| `buildGraph` + `sameFloorVerticalPolicy` | 合并图；同层竖向边过滤 |
| `crossEdges` | 跨层/跨区边 |
| `GRAPH_CACHE_VER` | 强刷 JSON / cross_floor_links |

### 文件对照

| 用途 | 路径 |
|------|------|
| 扫码入口 | `index.html` → `map.html` |
| 二维导航 | `map.html` |
| 全景 | `panorama_full.html` |
| 二维↔全景 | `js/panorama_map_bridge.js`、`map_data/panorama_map_bridge.md` |
| 路网 | `node_nav/data/*.json` |
| 校验 | `verify_zone_route.py`、`audit_vertical_links.py`、`check_graph.py` |

---

## 常见任务模板

### A. 补拓扑 / 改边权

改 `node_nav/data/*.json` → 校验脚本 → bump `GRAPH_CACHE_VER` → map Ctrl+F5。

### B. 新楼层坐标

pick-coords 导出 → `apply_cad_coords.py` → 确认 `JSON_GRAPHS` 含该 tab。

### C. 改 map / 全景交互

只改 `map.html` 或 `panorama_full.html` 内一份逻辑；测首屏加载、切层、算路。

### D. 增删全景↔二维对照

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
4. 全景：连廊 ↔ 二栋热点切换流畅；面板可拖、可折

---

## 给 Agent 的提醒

1. Windows + PowerShell；`&&` 不可用，用 `;`
2. `panorama_full.html` 才是完整版（非 panorama.html demo）
3. JSON 无前缀 / map 有前缀 — 改 zoneLinks 时注意
4. f1_a 单层 check_graph 可能 FAIL — 预期行为
5. 连廊 tab 14–18 无 FLOORS 回退，必须等 JSON 加载
6. 不主动 commit/push

---

*最后更新：2026-06-10*
