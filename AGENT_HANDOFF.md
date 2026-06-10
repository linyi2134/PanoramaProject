# Agent 交接 Prompt

将下面 **「Prompt 正文」** 整段复制到新对话的第一条消息，并按任务改「本次请你」一节。

---

## Prompt 正文（复制起点）

```
你正在接手 B7 教学楼「校园导览与信息导航系统」（课程项目「知途」）。

【产品形态】
- Web 应用（HTML + JS + Python 静态服务），不是 Qt 客户端
- 主入口：map.html（二维 CAD 地图 + 选起终点 + Dijkstra + 路径高亮）
- 辅助：panorama_full.html（52 场景全景 + 与二维深链互通）
- 手机演示需局域网 IP + 二维码（勿用 localhost）

【工作区】
- 唯一运行目录：c:\Users\yoimi\indoor_navigator\PanoramaProject
- 上级 indoor_navigator/ 下仅含 PanoramaProject/；旧杂物在 PanoramaProject/backup/
- GitHub：https://github.com/linyi2134/PanoramaProject
- 勿用 file://；不要未经用户要求 commit / push

【map.html · 2026-06-10 现状】
- 15 tab：B1F–B5F（1–5）、连廊1F–5F（14–18）、A1F–A5F（8–12）
- JSON_GRAPHS：15 层 CAD + node_nav/data/*_graph.json 全部启用
- 合并图前缀：B b{n}_、A a{n}_、连廊 lk{n}_（JSON 内仍无前缀原 id）
- 竖向跨层：cross_floor_links.json → crossEdges()；crossFloorWeight=6
- 竖向分组：B 三井各 5 层；A stair_south 5 层、stair_small 仅 3 层；连廊 outdoor_stair 5 层
- 跨区：zoneLinks（B↔连廊↔A，weight=15）；无 CROSS_CAMPUS 直连
- 同层算路：起终点同 tab 时禁用楼梯/电梯竖向边；A1F 主楼↔小楼翼跨子图时保留 A 座竖向边（sameFloorVerticalPolicy）
- UI：路网边线默认隐藏；导航橙色路径始终显示；起终点绿/红标记

【二维 ↔ 全景 · 已打通】
- 对照表：js/panorama_map_bridge.js + map_data/panorama_map_bridge.md
- 二维：点击有对照节点 → 弹窗 → panorama_full.html?scene=…
- 全景：侧栏「二维地图（…）」→ map.html?start=… → 自动切层并设起点
- 对照概要：
  · B 二栋 suffix 1–4 → 西南/西北/东南/东北分叉
  · A 一栋 2–5F suffix 1–5 → 南侧楼梯 + 四分叉
  · A 一栋 1F 仅 1–2 → 西北分叉、南侧楼梯
  · 连廊各层 → outdoor_stair
  · 三栋 1–3F → a{n}_stair_small 小楼楼梯
- 房间蓝点（room_labels_all.js）与走廊对照独立，勿混用

【A 座东侧翼】
- A1F 主楼与翼内不互通，须 A2F + stair_small；f1_a 单层 check_graph 可能 FAIL
- 全景「三栋」= 翼内小楼视角，二维节点为 stair_small（非独立 tab）

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
- 改 graph 或 cross_floor_links → bump map.html GRAPH_CACHE_VER（当前 20260609-same-floor-vert）
- 改 panorama_map_bridge.js → bump map.html / panorama_full.html 中 bridge 的 ?v=（当前 20260609-san）
- pathfind.browser.js ?v=20260609；改后 Ctrl+F5

【验证】
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
# map 算路：B1 room137 → A1 office101（经连廊）；A1 主楼 → room_104（经 A2F）
# map 同层：B1 两点不走电梯；A1 主楼→room_104 仍可用楼梯
# 对照：B1 西南分叉 ↔ 二栋-1f-1；连廊2F ↔ lk2_outdoor_stair；三栋-2f ↔ a2_stair_small

【待办 · 建议优先级】
1. 边权实地丈量（同层边、zoneLinks 等）
2. 清理 cross_floor_links.json 内 campusCrossFloor 废弃字段
3. 2F-B 东侧动线（237/234/236，草稿 backup/indoor_navigator_misc/2F-B座.json）
4. 可选：server 0.0.0.0 + 二维码；二栋-xf-5 电梯区全景对照

不做：BLE、Qt 客户端、恢复独立「小楼」tab

【约束】中文；最小改动；改 map.html 勿在 </html> 后再加 JS 块

【本次请你】
（在此填写具体任务）

完成后说明：改了哪些文件、如何验证、对应哪条待办。
```

---

## 当前进度摘要（2026-06-10）

### 已完成

| 项 | 说明 |
|----|------|
| 二维导航 MVP | 15 tab、CAD、Dijkstra、跨层/跨区、路径高亮、起终点 UI |
| 合并图 id | b{n}_ / a{n}_ / lk{n}_；竖向链经 crossEdges |
| 同层算路策略 | 同 tab 禁竖向边；A1F 翼/主楼例外保留 A 楼梯 |
| **二维↔全景** | `panorama_map_bridge.js`；B/A/连廊/三栋对照；双向深链 |
| 跨层/跨区 | weight=6 / zoneLinks=15；verify_zone_route PASS |
| 全景 | 52 场景 + room_labels_all.js（含 A1F 洗手间补标） |
| 仓库 | GitHub linyi2134/PanoramaProject；backup/ 归档 |

### 待办

1. 同层与跨区边权实地丈量  
2. 清理 `cross_floor_links.json` 内 `campusCrossFloor` 废弃字段  
3. 2F-B 东侧动线合并（草稿在 backup）  
4. 可选：0.0.0.0 + 二维码；二栋 `-5` 电梯全景对照  

### map.html 关键符号

| 符号/函数 | 作用 |
|-----------|------|
| `buildGraph(s,e)` + `sameFloorVerticalPolicy` | 合并图；同层竖向边过滤 |
| `crossEdges` | 跨层/跨区边 |
| `onNodeClick` / `offerPanoramaJump` | 选点 + 全景弹窗 |
| `applyStartFromPanorama` | 读 `?start=` 深链 |
| `PanoramaMapBridge.*` | 对照表（bridge JS） |
| `GRAPH_CACHE_VER` | 强刷 JSON / cross_floor_links |

### 文件对照

| 用途 | 路径 |
|------|------|
| 二维导航 | `map.html` |
| 全景完整版 | `panorama_full.html` |
| **二维↔全景对照** | `js/panorama_map_bridge.js`、`map_data/panorama_map_bridge.md` |
| 跨层/跨区 | `map_data/cross_floor_links.json`、`.md` |
| 路网 | `node_nav/data/*.json` |
| 全景标注 | `js/room_labels_all.js` |
| 底图 | `plans/*_cad.png` |
| 校验脚本 | `verify_zone_route.py`、`audit_vertical_links.py`、`check_graph.py` |

---

## 常见任务模板

### A. 补拓扑 / 改边权

改 `node_nav/data/*.json` → 校验脚本 → bump `GRAPH_CACHE_VER` → map Ctrl+F5。

### B. 新楼层坐标

pick-coords 导出 → `apply_cad_coords.py` → 确认 `JSON_GRAPHS` 含该 tab。

### C. 改 map 交互

只改 `map.html` 内**一份** `<script>`；测同层/跨层/跨区/全景弹窗。

### D. 增删全景↔二维对照

改 `panorama_map_bridge.js` → bump bridge `?v=` → 按 `panorama_map_bridge.md` 表测双向深链。

### E. 单层 Python 试算

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
```

**map 手动测例**

1. B1 `room137_front` → A1 `office101`（经连廊）  
2. A1 主楼 → `room_104A`（经 A2F + stair_small）  
3. 同层 B1 两点：路径不经过电梯/楼梯  
4. B1 西南分叉：弹窗进 `二栋-1f-1`；全景返回起点为 `b1_fork_sw`  
5. A2 小楼楼梯 ↔ `三栋-2f`；连廊 3F ↔ `lk3_outdoor_stair`  

---

## 给 Agent 的提醒

1. Windows + PowerShell；`&&` 不可用，用 `;`  
2. `panorama_full.html` 才是全景完整版（非 panorama.html demo）  
3. JSON 无前缀 / map 有前缀 — 改 zoneLinks 时注意  
4. f1_a 单层 check_graph 可能 FAIL — 预期行为  
5. 三栋全景对照的是 **A 座 stair_small**，不是独立地图 tab  
6. 不主动 commit/push  

---

*最后更新：2026-06-10*
