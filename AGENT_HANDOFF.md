# Agent 交接 Prompt

将下面整段复制到新对话的第一条消息（可按任务删改「本次请你」一节）。

---

## Prompt 正文（复制起点）

```
你正在接手 B7 教学楼「校园导览与信息导航系统」（课程项目「知途」）。

【产品状态】系统已可端到端演示：二维为主、全景为辅；接近可交付，剩余为数据对齐与体验优化。
第四周仅数据搜集；第五周完成 final_map 合并、52 场景全景、1F JSON+PNG 试点、文档与周报。

【必读】
- PanoramaProject/AGENT_HANDOFF.md（本文件）
- PanoramaProject/PROJECT_CONTEXT.md
- PanoramaProject/map_data/README.md（双轨与坐标，必读）
- PanoramaProject/node_nav/data/README.md（JSON 规范）

【路径与 Git】
- 唯一运行目录：c:\Users\yoimi\indoor_navigator\PanoramaProject
- GitHub：https://github.com/linyi2134/PanoramaProject （main）
- 本地可能有未 push 提交（含 panoramas ~300MB）；push 前 git status
- 上级 indoor_navigator 的 final_map .html、panorama(1).html、全景图/ 已并入，可删
- 不要未经用户要求 commit/push

【运行】
cd PanoramaProject
python server_main.py
→ map.html（默认，13 层 + 跨楼算路）
→ panorama_full.html（52 场景）
→ panorama.html（5 场景 demo）
⚠️ 必须在 PanoramaProject 下启动；禁止 file://；勿在 indoor_navigator 根目录跑 server

【坐标系 · 极易误解】
- 当前二维底图与点位统一为 SVG viewBox 760×520（map.html FLOORS 的 x,y）
- plans/f{n}_b.png 是同坐标系的示意 PNG 贴图，不是 CAD 真实比例
- f1_cad.png 等尺寸不同，不可直接套用 FLOORS 的 x,y
- 未启用 JSON 的楼层：节点/边/算路用 FLOORS（id 如 f2_wash）
- 启用 JSON 的楼层（仅 1F）：节点位置仍来自示意 xy（写入 JSON 的 x_px/y_px），
  算路 id/边用 f1_b_graph.json（如 washroom）；跨楼边在 map.html 中映射 fork_se/link_to_a

【双轨数据】
| 层 | 示意图 map.html FLOORS | 课程 JSON node_nav/data |
|----|------------------------|-------------------------|
| id | f1_wash, f1_rm138 | washroom, room137_front |
| 1F 桥接 | map_data/id_map_f1_b.json（整合时编写，非组员原件） |
| 应用 | apply_layout_coords.py → f1_b_graph.json 的 x_px/y_px |
| 启用 | map.html 的 JSON_GRAPHS 仅 {1: f1_b_graph.json} |
注意：id_map 中 match=inferred 为语义近似/手填坐标，非实地测绘。

【已完成】
- map.html：13 层（B7 1–5F + 小楼 + A 区）、CROSS、drawSmallBuilding/drawOfficeBuilding
- pathfind.browser.js + PNG 底图 + 1F JSON 试点
- panorama_full.html + panoramas/（52 jpg）+ 与 map 互链
- 脚本：apply_layout_coords、export_map_png、dwg_or_pdf_to_png、build_panorama_full
- 文档：AGENT_HANDOFF、README、项目进展备忘.docx、每周进展报告-第5周.docx

【待办 · 建议优先级】
1. 2F–5F B 区：新建 id_map_f{n}_b.json（勿复制 1F）→ apply_layout_coords → JSON_GRAPHS 逐层启用
2. 连通性：python -m indoor_nav route 校验各层；isFinished
3. 可选：tools/pick-coords.html（CAD 底图标点）
4. 可选：二维房间 ↔ 全景场景绑点；A 区/小楼 JSON 图
不做：BLE 定位、Qt 客户端

【关键文件】
map.html | panorama_full.html | js/pathfind.browser.js
node_nav/data/f*_graph.json | map_data/id_map_f1_b.json | plans/

【验证】
python -m indoor_nav route node_nav/data/f1_b_graph.json room137_front washroom
浏览器 1F：PNG +「JSON路网」；试跨楼路径（如 1F → 小楼）

【约束】中文回复；最小改动；改 map.html 勿重复 </html> 后 JS 块

【本次请你】
（填写任务，例如：）
- 做 2F：id_map_f2_b.json 初稿 + apply_layout_coords + JSON_GRAPHS 启用 2F
- 或：校验 f1_b/f2_b 连通性并修 CROSS
- 或：git push / 更新周报

完成后：改了哪些文件、如何验证、对应哪条待办。
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
7. **Git push** — 本地 commit `3ec3422` 可能仍 ahead of origin（含 panoramas ~300MB）；需用户环境 `git push` 确认

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

1. 用户环境：**Windows + PowerShell**；用 `;` 分隔命令，不用 `&&`  
2. **760×520 = map.html 示意 xy**；PNG 底图同系；JSON x_px/y_px 从 FLOORS 抄入（经 id_map）  
3. **id_map_f1_b.json** 为整合时编写的桥接表（direct/inferred），不是组员原始交付  
4. 1F JSON 模式下算路边以 **f1_b_graph.json** 为准（边较少），不是 FLOORS 全走廊网  
5. **CAD PNG** 与示意坐标不可混用；换 CAD 主底图需重标  
6. `map.html` 仅保留单个 `</html>`；勿粘贴 final_map 末尾垃圾块  
7. 用户偏好：**中文**；最小改动；不主动 commit/push  
8. 备忘 Word：`项目进展备忘-已完成与待办.docx`、`每周进展报告-第5周.docx`

---

*最后更新：2026-06-01，交接 Prompt 刷新（坐标系 / id_map / 可运行状态）。*
