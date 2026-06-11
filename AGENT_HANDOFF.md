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

【公网 / 扫码 / Pages 部署】
- Pages 根址：https://linyi2134.github.io/PanoramaProject/
- 推荐二维码：https://linyi2134.github.io/PanoramaProject/map.html
- 自定义 workflow：`.github/workflows/deploy-pages.yml` + 根目录 `.nojekyll`（显式 pages: write，避免内置 pages-build-deployment 401/卡 Queued）
- Settings → Pages → Source：**GitHub Actions** → **Deploy GitHub Pages**；Actions 权限 **Read and write**
- 推送后约 1–3 分钟生效；手机强刷或无痕

【map.html · 2026-06-11 现状】
- 15 tab：B1F–B5F（1–5）、连廊1F–5F（14–18）、A1F–A5F（8–12）
- JSON_GRAPHS：15 层 CAD + node_nav/data/*_graph.json 全部启用
- 合并图前缀：B b{n}_、A a{n}_、连廊 lk{n}_（JSON 内仍无前缀原 id）
- 懒加载：首屏仅 B1F；loadJsonGraphsBackground()；floorJsonReady() 控制未加载层不参与算路
- UI：浅蓝主题；路网边线默认隐藏；导航橙色路径始终显示；起终点绿/红标记
- 设施节点（洗手间等）：role=facility **默认显示橙色标注**（房间仍点击后 revealedLabels 显示）
- **可跳转节点**（跨区/楼梯/电梯）：琥珀色外圈 `#e8912d` + **常显标签**；图例「可跳转（跨区/楼梯）」
  · 节点：link_to_a / link_to_b、elevator、stair_*、outdoor_stair
  · 点击 → portalModal：可选跳转到对应区域二维图；楼梯/电梯提供上楼/下楼；仍可进全景或继续选点
  · 逻辑：getCrossRegionPortal() 读 crossFloorSpec.zoneLinks + unifiedVertical；jumpToPortalOption() → switchFloor
- **地点搜索**：侧栏 🔍 → 弹窗 → 房号/名称匹配 → 跳层设终点 + 算路（15 层 id_map_*.json）
- **资源预取**：prefetchAllCadImages() 先 15 张 CAD（当前层优先）→ runPanoramaPrefetch() 当前层全景 → 依次其它层
  · 切 tab：AbortController 取消进行中的全景 fetch，重新排队；已缓存 scene 不重复拉
- 顶栏「🌐 全景」：红色描边按钮
- 竖向/跨区：crossFloorWeight=6；zoneLinks=15；cross_floor_links.json 已删 campusCrossFloor 废弃字段

【map.html · 手机端（≤768px）】
- 顶栏压缩；侧栏折叠 52px（◀ + 🔍 + 起/终点）→ 展开 160px 浮层
- Panzoom 4.5.1（本地 js/panzoom.min.js）；切层 resetMapZoom()
- 关键函数：initMobileSide()、initMapPanzoom()、initPlaceSearch()、schedulePanoramaPrefetch()、offerPortalModal()

【panorama_full.html】
- 全景 JPG 压缩：52 张 ~32 MB；?v=20260610-compress
- 无全屏 loader；LRU 5 场景（勿 destroy 整 viewer）
- 场景热点 35px；房间蓝点 14px；buildSceneHotspots 禁止 cssClass / sceneId

【二维 ↔ 全景】
- js/panorama_map_bridge.js?v=20260610-prefetch（panoramaImageUrl）
- 对照节点蓝虚线圈；portalModal 也可进全景

【A 座东侧翼】
- A1F 主楼与翼内不互通，须 A2F + stair_small；f1_a 单层 check_graph 可能 FAIL

【必读】
- AGENT_HANDOFF.md、PROJECT_CONTEXT.md、README.md
- map_data/cross_floor_links.md、panorama_map_bridge.md、map_data/id_map_*.json

【运行】
cd PanoramaProject
python server_main.py
→ http://localhost:8000/map.html

【改 graph / map / 对照后】
- 改 graph 或 cross_floor_links → bump map.html GRAPH_CACHE_VER（当前 20260611-id-map-all）
- 改 panorama_map_bridge.js → bump ?v=（当前 20260610-prefetch）
- 改 panoramas/*.jpg → bump PANORAMA_CACHE_VER（20260610-compress）
- 改 .github/workflows/deploy-pages.yml → push 后看 Actions「Deploy GitHub Pages」

【验证】
python node_nav/scripts/verify_zone_route.py
python node_nav/scripts/audit_vertical_links.py
# map：搜「133」；点 B1 连廊口见琥珀圈+跳转弹窗；切层后 Network 见旧全景 canceled
# 全景：无黑屏；JPG ~800KB

【不做】BLE、Qt 客户端、恢复独立「小楼」tab

【约束】
- 中文；最小改动；改 map.html 勿在 </html> 后再加 JS 块
- 手机布局只写在 @media (max-width:768px) 内
- 全景场景热点勿用 cssClass 替代 pnlm-scene 雪碧图

【本次请你】


完成后说明：改了哪些文件、如何验证。
```

---

## 当前进度摘要（2026-06-11）

| 项 | 说明 |
|----|------|
| 二维导航 MVP | 15 tab、CAD、Dijkstra、跨层/跨区、路径高亮 |
| GitHub Pages | 自定义 `deploy-pages.yml`；index → map |
| map 搜索 | initPlaceSearch；15 层 id_map 房号别名 |
| map 跨区跳转 | portalModal；楼梯上/下楼；琥珀圈常显标注 |
| map 预取 | 先 15 CAD → 当前层全景 → 其余层；切层 abort |
| map 手机端 | 折叠侧栏 + Panzoom（本地）+ 设施常显 |
| 全景压缩/性能 | ~32 MB；LRU×5；无 loader |
| 二维↔全景 | bridge + 双向深链 |
| cross_floor 清理 | 删除 campusCrossFloor 废弃字段 |
| 边权 | 同层/跨区/跨层已实地走查校验 |
| 2F-B 东侧动线 | 237/234/236 等已合并进 f2_b_graph.json 并验收 |
| id_map | 15 层 map_data/id_map_*.json + generate_id_maps.py |
| Panzoom | js/panzoom.min.js 4.5.1 本地化 |

### map.html 关键符号

| 符号/函数 | 作用 |
|-----------|------|
| `isCrossRegionPortalNode` / `getCrossRegionPortal` | 识别可跳转节点与目标 |
| `offerPortalModal` / `jumpToPortalOption` | 跨区/换层弹窗与切 tab |
| `prefetchAllCadImages` / `runPanoramaPrefetch` | CAD 与全景预取队列 |
| `schedulePanoramaPrefetch` | 切层时 abort 并重排队 |
| `initPlaceSearch` / `loadRoomSearchAliases` | 地点搜索 |
| `GRAPH_CACHE_VER` | 强刷 JSON / cross_floor / id_map |

### 部署

| 文件 | 说明 |
|------|------|
| `.github/workflows/deploy-pages.yml` | Pages 发布（permissions: pages write） |
| `.nojekyll` | 静态站不走 Jekyll |

### 工具脚本

| 脚本 | 用途 |
|------|------|
| `compress_panoramas.py` | 批量压缩 panoramas |
| `verify_zone_route.py` | 跨区路线 |
| `audit_vertical_links.py` | 竖向边分组 |

---

## 常见任务模板

### A. 补拓扑 / 改边权

改 `node_nav/data/*.json` → 校验 → bump `GRAPH_CACHE_VER` → map Ctrl+F5。

### B. 改 map 交互 / 跳转 / 预取

只改 `map.html` 内 `<style>` + `<script>`；手机样式放 `@media (max-width:768px)`。

### C. 改全景

改 `buildSceneHotspots`；勿 destroy viewer；JPG 改完 bump `PANORAMA_CACHE_VER`。

### D. push GitHub / Pages

```powershell
git push git@github.com:linyi2134/PanoramaProject.git main
```

Actions 看 **Deploy GitHub Pages**（非卡死的 pages-build-deployment #7）。

---

## 验证命令速查

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py
python node_nav/scripts/verify_zone_route.py
```

**手动测例**

1. map 搜「133」「洗手间」→ 跳层设终点
2. 点 B1「连廊（接A区）」→ 琥珀圈 → 弹窗「进入连廊1F」
3. 点电梯 → 上楼/下楼选项；选后切到对应 tab
4. DevTools Network：先 plans/*_cad.png，再 panoramas/*.jpg；切层见 canceled
5. B1→A1 经连廊；全景无黑屏 loader

---

## 给 Agent 的提醒

1. Windows PowerShell：`&&` 不可用，用 `;`
2. JSON 无前缀 / map 有 b1_ 前缀
3. 内置 Pages workflow 可能 401 或 Queued 卡死 → 用 deploy-pages.yml
4. 全景场景热点：**cssClass 与 pnlm-sprite 互斥**
5. 不主动 commit/push

---

*最后更新：2026-06-11（待办已清空）*
