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
- 公网演示：GitHub Pages；局域网：python server_main.py
- 目标用户以手机扫码为主；桌面/手机布局分离（CSS @media max-width:768px）

【工作区】
- 唯一运行目录：c:\Users\yoimi\indoor_navigator\PanoramaProject
- 上级 indoor_navigator/ 下仅含 PanoramaProject/；旧杂物在 PanoramaProject/backup/
- GitHub：https://github.com/linyi2134/PanoramaProject
- 勿用 file://；不要未经用户要求 commit / push
- 国内 push 优先：git push git@github.com:linyi2134/PanoramaProject.git main（HTTPS 经代理易断）

【公网 / 扫码】
- Pages 根址：https://linyi2134.github.io/PanoramaProject/
- 推荐二维码：https://linyi2134.github.io/PanoramaProject/map.html
- 全景从 map 顶栏红色「🌐 全景」进入（已压缩，单张约 0.5–0.8 MB）
- Pages 推送后约 1–3 分钟生效；手机需强刷或无痕

【map.html · 2026-06-10 现状】
- 15 tab：B1F–B5F（1–5）、连廊1F–5F（14–18）、A1F–A5F（8–12）
- JSON_GRAPHS：15 层 CAD + node_nav/data/*_graph.json 全部启用
- 合并图前缀：B b{n}_、A a{n}_、连廊 lk{n}_（JSON 内仍无前缀原 id）
- 懒加载：首屏仅 B1F；loadJsonGraphsBackground()；floorJsonReady() 控制未加载层不参与算路
- UI：浅蓝主题；路网边线默认隐藏；导航橙色路径始终显示；起终点绿/红标记
- 设施节点（洗手间等）：role=facility **默认显示橙色标注**（房间仍点击后 revealedLabels 显示）
- 顶栏「🌐 全景」：红色描边按钮（无「可选」字样）
- **地点搜索**：侧栏 🔍（折叠 52px 宽时仍显示大图标）→ 弹窗输入 → 匹配房间/门/设施
  · 房号搜索靠节点 id 数字 + map_data/id_map_f1_b.json 别名（如 133 → b1_mobile_room）
  · 选中后：切层 + 设终点 + 有起点则自动算路
- **全景预取**：浏览 map 时后台 prefetch panoramas/*.jpg（bridge.panoramaImageUrl），进全景走浏览器缓存
- 竖向/跨区：crossFloorWeight=6；zoneLinks=15；同层禁竖向边（A1F 翼/主楼例外）

【map.html · 手机端（≤768px）】
- 顶栏压缩；右侧栏 position:absolute 浮层，默认折叠 52px（◀/▶ + 🔍 + 起/终点竖排）
- 展开 160px：图例、房间列表、路径；不挤压地图宽度
- Panzoom 4.5.1（CDN）：双指/滚轮；切层 resetMapZoom()
- 关键函数：initMobileSide()、initMapPanzoom()、initPlaceSearch()、prefetchPanoramaImage()

【panorama_full.html · 2026-06-10】
- 全景 JPG 已压缩：52 张合计 ~32 MB（原 ~324 MB），3000px q80；原图 backup/panoramas_original/（gitignore）
- URL 缓存戳：?v=20260610-compress（bridge PANORAMA_CACHE_VER 与之一致）
- **无全屏加载遮罩**（已删 sceneLoader 半黑转圈）
- LRU **5 场景**：addScene/loadScene/removeScene，**勿 destroy 整 viewer**（旧逻辑极慢）
- 场景热点：35px 雪碧图箭头（.pnlm-scene）；房间蓝点 14px（room-info-hotspot）
- 导航面板可拖动/折叠；底部「二维地图」链接 **下划线加粗**
- 场景热点：buildSceneHotspots() → type:"scene" + clickHandlerFunc→switchToScene
  · 禁止 cssClass（会去 pnlm-sprite）；禁止 config 设 sceneId（会绕过 LRU）

【二维 ↔ 全景】
- js/panorama_map_bridge.js?v=20260610-prefetch（含 panoramaImageUrl(sceneId)）
- 二维对照节点蓝虚线圈 → 弹窗 → panorama_full.html?scene=…
- 全景侧栏链到 map.html?start=…

【A 座东侧翼】
- A1F 主楼与翼内不互通，须 A2F + stair_small；f1_a 单层 check_graph 可能 FAIL

【必读】
- AGENT_HANDOFF.md、PROJECT_CONTEXT.md、README.md
- map_data/panorama_map_bridge.md、cross_floor_links.md
- map_data/id_map_f1_b.json（B1 搜索房号别名来源）

【运行】
cd PanoramaProject
python server_main.py
→ http://localhost:8000/map.html
→ http://localhost:8000/panorama_full.html

【改 graph / map / 对照后】
- 改 graph 或 cross_floor_links → bump map.html GRAPH_CACHE_VER（当前 20260610-fix-load）
- 改 panorama_map_bridge.js → bump ?v=（当前 20260610-prefetch）
- 改 panoramas/*.jpg → bump PANORAMA_CACHE_VER + 可选重跑 compress_panoramas.py
- pathfind.browser.js ?v=20260609

【验证】
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
# map：侧栏搜「133」→ 移动计算实验室；搜「洗手间」→ 多结果
# map 手机：折叠侧栏可见 🔍；设施橙色字常显
# 全景：无黑屏转圈；Network 里 JPG ~800KB 且带 ?v=20260610-compress

【待办 · 建议优先级】
1. 边权实地丈量（同层边、zoneLinks 等）
2. 清理 cross_floor_links.json 内 campusCrossFloor 废弃字段
3. 2F-B 东侧动线（237/234/236，草稿 backup/indoor_navigator_misc/2F-B座.json）
4. 搜索别名扩展到全楼层 id_map（目前仅 f1_b）；Panzoom 改本地 js/

不做：BLE、Qt 客户端、恢复独立「小楼」tab

【约束】
- 中文；最小改动；改 map.html 勿在 </html> 后再加 JS 块
- 手机布局只写在 @media (max-width:768px) 内
- 全景场景热点勿用 cssClass 替代 pnlm-scene 雪碧图

【本次请你】


完成后说明：改了哪些文件、如何验证、对应哪条待办。
```

---

## 当前进度摘要（2026-06-10 晚）

### 已完成

| 项 | 说明 |
|----|------|
| 二维导航 MVP | 15 tab、CAD、Dijkstra、跨层/跨区、路径高亮 |
| GitHub Pages | index → map；SSH push 稳定 |
| map 手机端 | 折叠侧栏 52px + 搜索图标；Panzoom；设施常显标注 |
| map 搜索 | initPlaceSearch；id_map 房号别名；选结果→终点+算路 |
| map 全景预取 | 看二维时后台拉 panoramas JPG |
| 全景压缩 | 324→32 MB；compress_panoramas.py；原图 backup/panoramas_original/ |
| 全景性能/UI | 无 loader 遮罩；addScene LRU×5；热点 35px/蓝点 14px |
| 互链样式 | map 红框「全景」；全景二维链接下划线 |
| 二维↔全景 | bridge + 双向深链 |

### 待办

1. 同层与跨区边权实地丈量
2. 清理 `cross_floor_links.json` 废弃字段
3. 2F-B 东侧动线（backup 草稿）
4. 搜索 id_map 扩层；Panzoom 本地化；二栋 `-5` 电梯全景对照

### map.html 关键符号

| 符号/函数 | 作用 |
|-----------|------|
| `floorJsonReady` / `loadJsonGraph` | 分层懒加载 |
| `initPlaceSearch` / `runPlaceSearch` | 地点搜索弹窗 |
| `loadRoomSearchAliases` | 读 id_map_f1_b 补房号 |
| `prefetchPanoramaImage` | 二维浏览时预取全景 JPG |
| `revealedLabels` | 房间标注（facility 除外，facility 常显） |
| `GRAPH_CACHE_VER` | 强刷 JSON / cross_floor / id_map |

### panorama_full.html 关键符号

| 符号/函数 | 作用 |
|-----------|------|
| `switchToScene` | addScene + loadScene；LRU 5；**不 destroy viewer** |
| `buildSceneHotspots` | 场景热点；无 cssClass / 无 sceneId |
| `PANORAMA_CACHE_VER` | 全景 JPG 缓存戳 |

### 工具脚本

| 脚本 | 用途 |
|------|------|
| `node_nav/scripts/compress_panoramas.py` | 批量压缩 panoramas/*.jpg |
| `verify_zone_route.py` | 跨区路线 |
| `audit_vertical_links.py` | 竖向边分组 |

### 文件对照

| 用途 | 路径 |
|------|------|
| 扫码入口 | index.html → map.html |
| 二维导航 | map.html |
| 全景 | panorama_full.html |
| 二维↔全景 | js/panorama_map_bridge.js |
| B1 搜索别名 | map_data/id_map_f1_b.json |
| 压缩全景 | panoramas/*.jpg（原图 backup/panoramas_original/） |

---

## 常见任务模板

### A. 补拓扑 / 改边权

改 `node_nav/data/*.json` → 校验 → bump `GRAPH_CACHE_VER` → map Ctrl+F5。

### B. 改 map 搜索 / 手机侧栏

只改 `map.html` 内 `<style>` + `<script>`；手机样式放 `@media (max-width:768px)`。

### C. 改全景

场景热点改 `buildSceneHotspots`；性能勿恢复 destroyViewer 全量重建；JPG 改完 bump `PANORAMA_CACHE_VER`。

### D. 压缩 / 换全景图

`python node_nav/scripts/compress_panoramas.py`（先备份）→ bump 缓存戳 → push。

### E. push GitHub

```powershell
git push git@github.com:linyi2134/PanoramaProject.git main
```

---

## 验证命令速查

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/compress_panoramas.py --dry-run
```

**手动测例**

1. map 搜索「133」「洗手间」→ 有结果 → 跳层设终点
2. 手机 ≤768px：折叠侧栏仍见 🔍；展开见完整搜索条
3. 全景：切场景无黑屏；JPG 体积 ~0.8 MB
4. B1→A1 经连廊；A1 主楼→room_104 经 A2F

---

## 给 Agent 的提醒

1. Windows PowerShell：`&&` 不可用，用 `;`
2. `panorama_full.html` 才是完整版
3. JSON 无前缀 / map 有 b1_ 前缀
4. 搜「133」依赖 id_map_f1_b，其他楼层靠 label/id 内数字
5. 全景场景热点：**cssClass 与 pnlm-sprite 互斥**
6. 不主动 commit/push

---

*最后更新：2026-06-10*
