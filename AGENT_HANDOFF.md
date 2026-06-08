# Agent 交接 Prompt

将下面 **「Prompt 正文」** 整段复制到新对话的第一条消息，并按任务改「本次请你」一节。

---

## Prompt 正文（复制起点）

```
你正在接手 B7 教学楼「校园导览与信息导航系统」（课程项目「知途」）。

【产品形态】
- Web 应用（HTML + JS + Python 静态服务），不是 Qt 客户端
- 主入口：map.html（二维 CAD 地图 + 选起终点 + Dijkstra + 路径高亮）
- 辅助：panorama_full.html（52 场景全景）；可选 PyInstaller 打包 exe
- 手机演示需局域网 IP + 二维码（勿用 localhost）

【工作区】
- 唯一运行目录：c:\Users\yoimi\indoor_navigator\PanoramaProject
- 上级 indoor_navigator/ 下仅含 PanoramaProject/；旧杂物在 PanoramaProject/backup/
- GitHub：https://github.com/linyi2134/PanoramaProject
- 勿用 file://；不要未经用户要求 commit / push

【map.html · 2026-06-09 现状】
- 15 tab 标签：B1F–B5F（tab 1–5）、连廊1F–5F（14–18）、A1F–A5F（8–12）
- JSON_GRAPHS：15 层 CAD + node_nav/data/*_graph.json 全部启用
- 合并图 nodeId 前缀（JSON 内仍无前缀原 id）：
  · B tab 1–5 → b1_…b5_（如 b1_room137_front）
  · A tab 8–12 → a1_…a5_
  · 连廊 tab 14–18 → lk1_…lk5_
- 竖向跨层：cross_floor_links.json → crossEdges()；crossFloorWeight=6（每上下一层，含电梯）
- 竖向分组：B 三井 elevator/stair_east/stair_west 各 5 层独立链；A stair_south 5 层、stair_small 仅 3 层；连廊 outdoor_stair 5 层
- 跨区：zoneLinks（B↔连廊↔A，weight=15）；已移除 CROSS_CAMPUS 直连
- UI：路网边线默认隐藏（顶栏「⬡ 路网线」可开）；导航橙色路径始终显示
- 交互：右侧选起点/终点 → 地图点选；选起点后自动切终点；forceRender() 刷新 UI
- 起终点：gMarkers 层（绿起/红终）；换层指引区分乘电梯/走楼梯/经连廊

【A 座东侧翼】
- 无独立「小楼」；A1F 主楼与东侧翼层内不互通，须 A2F + stair_small
- f1_a：room_104A/B ↔ stair_small 翼内边；无 fork_se → 104 主楼直连
- f1_a 单层 check_graph 可能 FAIL；合并图跨层算路正常

【竖向节点 id（JSON 内）】
- B：elevator / stair_east / stair_west
- A：stair_south（1–5F）、stair_small（1–3F）
- 连廊：outdoor_stair

【必读】
- PanoramaProject/AGENT_HANDOFF.md、PROJECT_CONTEXT.md
- map_data/cross_floor_links.md + cross_floor_links.json
- map_data/README.md、node_nav/data/README.md

【运行】
cd PanoramaProject
python server_main.py
→ http://localhost:8000/map.html

【改 graph / map 后】
- bump map.html 的 GRAPH_CACHE_VER（当前 20260609-floor-w6）
- pathfind.browser.js 带 ?v=20260609；改后 Ctrl+F5

【验证】
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
python node_nav/scripts/check_graph.py node_nav/data/f3_b_graph.json
# map：B1 room137 → A1 office101（经连廊）；A1 主楼 → room_104（须经 A2F）

【待办 · 建议优先级】
1. 边权实地丈量（同层边、zoneLinks 等）
2. 清理 cross_floor_links.json 内 campusCrossFloor 废弃字段（map 已不再读）
3. 2F-B 东侧动线（237/234/236，草稿 backup/indoor_navigator_misc/2F-B座.json）
4. 可选：server 0.0.0.0 + 二维码；二维节点 ↔ 全景对照

不做：BLE、Qt 客户端、恢复独立「小楼」tab

【约束】中文；最小改动；改 map.html 勿在 </html> 后再加 JS 块

【本次请你】
（在此填写具体任务）

完成后说明：改了哪些文件、如何验证、对应哪条待办。
```

---

## 当前进度摘要（2026-06-09）

### 已完成

| 项 | 说明 |
|----|------|
| 二维导航 MVP | 15 tab、CAD、Dijkstra、跨层/跨区、路径高亮、起终点 UI |
| 合并图 id | b{n}_ / a{n}_ / lk{n}_；B/A 竖向链经 crossEdges |
| 跨层 cost | crossFloorWeight=6；减少乱换层 |
| 跨区 | zoneLinks + verify_zone_route PASS；无 B-A 直连 |
| 地图 UI | 路网线可隐藏；tab 标签 B1F 等；换层文案区分电梯/楼梯 |
| pathfind | js/pathfind.browser.js 语法修复 + 缓存参数 |
| A 东侧翼 | f1_a 拓扑与「1F 不互通、经 A2F」对齐 |
| 仓库整理 | backup/ 归档；plans/_archive/；外层仅留 PanoramaProject |
| 全景 | 52 场景 + room_labels_all.js |

### 待办

1. 同层与跨区边权实地丈量  
2. JSON 内 campusCrossFloor 字段清理（可选，map 已忽略）  
3. 2F-B 队友东侧动线合并（草稿在 backup）  
4. 手机扫码、全景对照（可选）

### map.html 关键符号

| 符号/函数 | 作用 |
|-----------|------|
| `graphIdPrefix` / `navNodeId` | 合并图 nodeId |
| `buildGraph` + `crossEdges` | 15 层 + 跨层/跨区 |
| `runDijkstra` / `onNodeClick` | 算路与选点 |
| `showEdges` / `toggleShowEdges` | 路网边线开关 |
| `renderPath` / `renderMarkers` | 导航路径与起终点 |
| `GRAPH_CACHE_VER` | 强刷 JSON / cross_floor_links |

### 文件对照

| 用途 | 路径 |
|------|------|
| 二维导航 | `map.html` |
| 跨层/跨区 | `map_data/cross_floor_links.json`、`.md` |
| 路网 | `node_nav/data/f*_*_graph.json`、`link_f*_graph.json` |
| 底图 | `plans/*_cad.png`（15 张） |
| 跨区验证 | `node_nav/scripts/verify_zone_route.py` |
| 竖向审计 | `node_nav/scripts/audit_vertical_links.py` |
| CAD 取点 | `tools/pick-coords.html` |
| 归档 | `backup/`、`plans/_archive/` |

---

## 常见任务模板

### A. 补拓扑 / 改边权

改 `node_nav/data/*.json` → `check_graph.py` / `verify_zone_route.py` → bump `GRAPH_CACHE_VER` → map Ctrl+F5。

### B. 新楼层坐标

pick-coords 导出 → `apply_cad_coords.py` → 确认 `JSON_GRAPHS` 含该 tab。

### C. 改 map 交互

只改 `map.html` 一处逻辑；勿重复 `</html>` 后脚本；测同层/跨层/跨区与路径高亮。

### D. 单层 Python 试算

```powershell
python -m indoor_nav route node_nav/data/f1_b_graph.json room137_front washroom
```

跨层/跨区用 map 或 verify_zone_route（带前缀）。

---

## 验证命令速查

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
python node_nav/scripts/check_graph.py node_nav/data/f3_a_graph.json
```

**map 手动测例**

1. B1F 起点 room137 → A1F 终点 office101（应经连廊，非 B 口瞬移到 A 口）  
2. A1F 主楼 → room_104A（应经 A2F + stair_small）  
3. 同层 B1F 两点：起终点标记与橙色路径立即出现  
4. 「⬡ 路网线」默认关；导航路径仍可见  

---

## 给 Agent 的提醒

1. Windows + PowerShell；`&&` 不可用，用 `;`  
2. panorama_full.html 才是全景完整版  
3. JSON 无前缀 / map 有前缀 — 改 zoneLinks 时注意  
4. f1_a 单层 check_graph 可能 FAIL — 预期行为  
5. 不主动 commit/push  

---

*最后更新：2026-06-09*
