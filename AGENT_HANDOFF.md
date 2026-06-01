# Agent 交接 Prompt

将下面整段复制到新对话的第一条消息（可按任务删改「本次请你」一节）。

---

## Prompt 正文（复制起点）

```
你正在接手 B7 教学楼「校园导览与信息导航系统」代码库。

【必读】先阅读仓库内：
- PanoramaProject/PROJECT_CONTEXT.md（项目全貌，部分条目可能滞后）
- PanoramaProject/AGENT_HANDOFF.md（本文件，最新交接摘要）
- PanoramaProject/node_nav/data/README.md（路网 JSON 规范）
- PanoramaProject/map_data/README.md（map 与 JSON 双轨、PNG 坐标流程）

【仓库路径】
- 主项目：c:\Users\yoimi\indoor_navigator\PanoramaProject（**唯一运行目录**）
- 上级 `indoor_navigator/` 根目录的 `final_map .html`、`panorama(1).html`、`全景图/` 已并入主项目，可删原件

【GitHub】
https://github.com/linyi2134/PanoramaProject （分支 main）
不要未经用户要求 commit/push。

【运行方式】
cd PanoramaProject && python server_main.py
→ http://localhost:8000/map.html（二维地图，默认；13 层 + 跨楼）
→ http://localhost:8000/panorama_full.html（全景完整版，52 场景）
→ http://localhost:8000/panorama.html（全景 demo，5 场景）
→ http://localhost:8000/tools/export_floor_png.html（导出示意 SVG/PNG）

⚠️ 必须在 PanoramaProject 下启动 server；不要用 file:// 打开 HTML。
⚠️ 不要在 indoor_navigator 根目录跑 server_main.py。

【技术事实 · 算路与数据】
- Dijkstra 三处同逻辑：indoor_nav/、node_nav/src/pathfind.js、js/pathfind.browser.js
- 课程路网：node_nav/data/f{1-5}_{a|b}_graph.json（10 文件）
- map.html 内嵌 FLOORS（示意 SVG 760×520，id 如 f1_wash）与 JSON（id 如 washroom）仍双轨
- 1F B 区试点已合并坐标：map_data/id_map_f1_b.json → f1_b_graph.json 含 x_px/y_px + meta.planImage
- map.html 已支持：plans/f{n}_b.png 底图；JSON_GRAPHS 目前仅启用 1F（f1_b_graph.json）
- 示意 PNG 760×520 可与 FLOORS 坐标照搬；CAD 图（f1_cad.png 等）尺寸不同，需重标坐标
- 不做自动定位（手动选点/搜索）

【技术事实 · 全景（已整合）】
| 文件 | 说明 |
|------|------|
| `panorama_full.html` | 52 场景 + BFS 导航面板；图片路径 `panoramas/*.jpg` |
| `panoramas/` | 52 张全景 jpg（体积较大，clone 需注意） |
| `tools/build_panorama_full.py` | 从根目录 `panorama(1).html` 重生 HTML（原件删除后需改脚本路径） |

【已有脚本（PanoramaProject 内）】
- node_nav/scripts/apply_layout_coords.py — 对照表 + map.html 坐标 → JSON x_px/y_px
- node_nav/scripts/export_map_png.py — 示意 PNG/SVG（--all --svg）
- node_nav/scripts/dwg_or_pdf_to_png.py — DWG 经同名 PDF 转 PNG（无 ODA 时）；3F 用 3F(3).pdf
- tools/export_floor_png.html — 浏览器导出示意 PNG/SVG

【CAD / 平面图】
- 根目录：1F(1).dwg/pdf、3F(1).dwg、3F(3).pdf
- plans/：f1_b.png…f5_b.png（示意）、f1_cad.png、f3_cad.png 等（CAD 裁切版）
- ODA File Converter（winget）安装失败 exit 1603；直转 DWG 暂不可用，用 PDF 中转即可

【代码约束】
- 最小改动；匹配现有风格
- 不要引入 Qt；优先 Web + Python 静态服务
- 改 map.html 时注意只保留一份 FLOORS，</html> 后不要粘重复 JS（final_map .html 第 834 行后有垃圾块需删）

【本次请你】
（在此填写具体任务，例如：）
- 整合 final_map .html 进 PanoramaProject/map.html，并保留 JSON/PNG 能力
- 或：移入 panorama(1).html + 全景图/，修路径，与 map 互链
- 或：继续做 2F–5F 的 id_map + apply_layout_coords
- 或：做 pick-coords.html 在 f1_cad.png 上标点

完成后说明：改了哪些文件、如何验证、对应哪条待办。
```

---

## 当前进度摘要（2026-06 更新）

### 已完成

| 项 | 说明 |
|----|------|
| map.html 13 层 | final_map 已合并：B7 1–5F + 小楼 + A 区；CROSS 跨楼；pathfind.browser.js |
| map.html 接入 | PNG 底图（PLAN_IMAGES）、1F JSON 算路（JSON_GRAPHS） |
| 全景完整版 | `panorama_full.html` + `panoramas/`（52 场景），与 map 互链 |
| 1F B 坐标试点 | `map_data/id_map_f1_b.json`，`f1_b_graph.json` 含 x_px/y_px、meta.planWidth/Height |
| plans/ | 示意 f1_b…f5_b.png；CAD f1_cad.png、f3_cad.png |
| 导出/转换工具 | export_map_png.py、apply_layout_coords.py、dwg_or_pdf_to_png.py、export_floor_png.html |
| map_data/README.md | PNG ↔ id ↔ map 流程说明 |

### 进行中 / 待办（建议优先级）

1. ~~**整合组员二维终稿**~~ — **已完成**：`final_map` 13 层 + CROSS + 小楼/A 区绘制已并入 `map.html`；保留 pathfind.browser.js、PNG、JSON；1F JSON 跨楼边映射 `fork_se`/`link_to_a`  
2. ~~**整合全景完整版**~~ — **已完成**：`panoramas/`（52 张 jpg）+ `panorama_full.html`；`map.html` ↔ 全景互链；`panorama.html` 保留 5 场景 demo  
3. **扩展 JSON 坐标** — 2F–5F 建 id_map_f{n}_b.json，跑 apply_layout_coords，在 map.html JSON_GRAPHS 逐层启用  
4. **CAD 底图坐标** — f1_cad / f3_cad 与示意坐标不通用；需 pick-coords 或手工重标  
5. **FLOORS ↔ JSON 单源** — 长期：抽离 schematic_floors.json 或统一 id  
6. **连通性校验** — 各层 graph JSON isFinished、python -m indoor_nav route 样例  
7. ~~**Git push**~~ — 已与 GitHub 同步（含 panoramas；仓库体积较大）

### 文件对照（避免混淆）

| 用途 | 文件 |
|------|------|
| 二维导航（主入口） | `map.html`（13 层示意 + PNG；1F JSON 试点） |
| 全景完整版 | `panorama_full.html` + `panoramas/*.jpg` |
| 全景 demo | `panorama.html`（5 场景 + 根目录 demo 图） |
| 1F JSON 路网 | `node_nav/data/f1_b_graph.json` |
| 1F id 对照 | `map_data/id_map_f1_b.json` |
| 组员原件（可删） | 上级目录 `final_map .html`、`panorama(1).html`、`全景图/` |

---

## 常见任务模板（可选用）

### A. 合并 final_map 进 map.html

```
本次请你：阅读 indoor_navigator/final_map .html 与 PanoramaProject/map.html，
将 final_map 的 13 层 FLOORS、CROSS、drawSmallBuilding/drawOfficeBuilding 合并进 map.html；
删除 final_map 834 行后的垃圾；保留 js/pathfind.browser.js、PLAN_IMAGES、JSON_GRAPHS；
header 加全景链接。不要 commit。
```

### B. 整合全景完整版

```
本次请你：将 indoor_navigator/panorama(1).html 与 全景图/ 移入 PanoramaProject
（建议 panoramas/ + panorama_full.html），修正 panorama 图片路径，
与 map.html 互链。验证 http://localhost:8000/panorama_full.html 可漫游。
```

### C. 扩展 JSON 坐标（下一层）

```
本次请你：参照 map_data/id_map_f1_b.json，创建 id_map_f2_b.json，
运行 apply_layout_coords.py，并在 map.html JSON_GRAPHS 启用 2F。
```

### D. CAD 底图 + 取点工具

```
本次请你：创建 tools/pick-coords.html，加载 plans/f1_cad.png 与 f1_b_graph.json 节点列表，
点击地图输出 x_px/y_px，并可导出更新后的 JSON 片段。
```

### E. PNG + 坐标（1F 已完成，其他层）

```
本次请你：python node_nav/scripts/export_map_png.py --all
对 f2_b 建 id 对照并 apply_layout_coords（见 map_data/README.md）。
```

### F. 校验路网

```
本次请你：校验 f1_a/f1_b 的 edges 连通性，python -m indoor_nav route 跑通 2 条示例路径。
```

### G. 推送 GitHub

```
本次请你：git status 后整理 commit 并 push（用户已授权）。
```

---

## 验证命令速查

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py

# 1F 算路
python -m indoor_nav route node_nav/data/f1_b_graph.json room137_front washroom

# 重导示意 PNG
python node_nav/scripts/export_map_png.py --all

# DWG → PNG（经 PDF）
python node_nav/scripts/dwg_or_pdf_to_png.py "1F(1).dwg" -o plans/f1_cad.png
python node_nav/scripts/dwg_or_pdf_to_png.py "3F(1).dwg" -o plans/f3_cad.png

# 应用坐标对照表
python node_nav/scripts/apply_layout_coords.py
python node_nav/scripts/apply_layout_coords.py id_map_f2_b.json f2_b_graph.json
```

---

## 给 Agent 的提醒

1. 用户环境：**Windows + PowerShell**；旧版 PowerShell 不支持 `&&`，用 `;` 分隔命令  
2. **760×520** 是示意坐标系（viewBox / 示意 PNG），不是浏览器窗口像素尺寸  
3. **CAD PNG**（如 698×637）与示意坐标**不能**直接混用  
4. `map.html` 有效内容应在单个 `</html>` 内；`final_map .html` 末尾有重复 FLOORS 需删  
5. 全景 `panorama(1).html` 默认认为 jpg 与 html **同目录**；图片实际在 `全景图/`  
6. 用户偏好：**中文回复**；最小改动；不主动 commit/push  
7. 详细背景以 `PROJECT_CONTEXT.md` + 本文件为准；`PROJECT_CONTEXT.md` 中「待办/二维状态」可能略滞后  

---

*最后更新：2026-06，final_map / 全景完整版已并入并 push。*
