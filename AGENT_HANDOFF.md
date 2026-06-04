# Agent 交接 Prompt

将下面整段复制到新对话的第一条消息（可按任务删改「本次请你」一节）。

---

## Prompt 正文（复制起点）

```
你正在接手 B7 教学楼「校园导览与信息导航系统」（课程项目「知途」）。

【产品状态】二维地图 + CAD 取点 + 52 场景全景（二栋房间标注已合并）可端到端演示；待办主要为各层 JSON 坐标写回、路网校验、二维↔全景绑点。

【必读】
- PanoramaProject/AGENT_HANDOFF.md（本文件）
- PanoramaProject/PROJECT_CONTEXT.md
- PanoramaProject/map_data/README.md（CAD / pick-coords）
- PanoramaProject/panorama_data/README.md（全景房间标注）
- PanoramaProject/node_nav/data/README.md（JSON 规范）
- PanoramaProject/CAD取点协作流程-简要说明.docx（组员协作用）

【路径与 Git】
- 唯一运行目录：c:\Users\yoimi\indoor_navigator\PanoramaProject
- GitHub：https://github.com/linyi2134/PanoramaProject （main）
- 不要未经用户要求 commit/push
- 上级 indoor_navigator/panorama.html 已合并进 panorama_full，可删；勿在根目录跑 server

【运行】
cd PanoramaProject
python server_main.py
→ map.html（13 层 + CAD 底图 A/B）
→ panorama_full.html（52 场景 + 二栋房间蓝点 + 场景导航）
→ tools/pick-coords.html（A/B 座 CAD 拖点 → cad_pick JSON）
→ panorama.html（5 场景 demo）
⚠️ 禁止 file://；必须在 PanoramaProject 下启动

【CAD / 二维坐标】
- PDF：1F-A…5F-A.pdf、1_2_5F-B.pdf、3_4F-B.pdf → plans/*_cad.png（export_all_cad_plans.py）
- pick-coords → map_data/cad_pick_f{n}_{a|b}.json → apply_cad_coords.py → f*_graph.json
- map.html：B 1–5F + A（楼层 8–12）已贴 CAD PNG；JSON_GRAPHS 仅 1F B 试点启用
- 示意 760×520 与 CAD 像素坐标不可混用

【全景】
- 图：panoramas/*.jpg（52）
- 二栋房间标注：js/room_labels_erdong.js（pitch/yaw）
- 一栋/连廊/三栋：仅场景跳转，无房间蓝点

【待办 · 建议优先级】
1. 各层 cad_pick 标完并 apply → JSON_GRAPHS 逐层启用
2. python -m indoor_nav route 校验连通性
3. 可选：补一栋/连廊 room_labels；二维房间 ↔ 全景场景 id 对照表
不做：BLE、Qt 客户端

【验证】
python -m indoor_nav route node_nav/data/f1_b_graph.json room137_front washroom
http://localhost:8000/map.html
http://localhost:8000/panorama_full.html（进二栋-1f-1 看蓝点）
http://localhost:8000/tools/pick-coords.html

【约束】中文；最小改动；改 map.html 勿重复 </html> 后 JS 块

【本次请你】
读完之后不做任何事

完成后：改了哪些文件、如何验证、对应哪条待办。
```

---

## 当前进度摘要（2026-06-03 更新）

### 已完成

| 项 | 说明 |
|----|------|
| map.html 13 层 | B7 1–5F + 小楼 + A 区；CROSS；CAD 底图（`plans/*_cad.png`） |
| CAD 取点 | `tools/pick-coords.html`（A/B 1–5F）+ `apply_cad_coords.py` + `export_all_cad_plans.py` |
| PDF 命名 | `1F-A.pdf`…`5F-A.pdf`、`1_2_5F-B.pdf`、`3_4F-B.pdf`；见 `map_data/cad_sources.json` |
| 全景 52 场景 | `panorama_full.html` + `panoramas/`；与 map 互链 |
| **二栋房间标注** | `js/room_labels_erdong.js` 已合并；蓝点悬停/点击；覆盖 22 个二栋场景 |
| 1F JSON 试点 | `f1_b_graph.json` + `JSON_GRAPHS` 仅 1F |
| 文档 | `panorama_data/README.md`、`CAD取点协作流程-简要说明.docx` |

### 进行中 / 待办

1. **CAD 坐标**：组员各层 `cad_pick` → `apply_cad_coords` → 启用 `JSON_GRAPHS`  
2. **路网校验**：各层 `isFinished`、`python -m indoor_nav route`  
3. **全景扩展**：一栋/连廊/三栋房间标注；与二维 graph 节点绑点  
4. ~~pick-coords / 全景合并~~ — 已完成  

### 文件对照

| 用途 | 文件 |
|------|------|
| 二维导航 | `map.html` |
| 全景（主） | `panorama_full.html` + `panoramas/*.jpg` |
| 二栋房间数据 | `js/room_labels_erdong.js` |
| 全景说明 | `panorama_data/README.md` |
| CAD 取点 | `tools/pick-coords.html` |
| 全景 demo | `panorama.html`（5 场景） |
| 路网 JSON | `node_nav/data/f*_graph.json` |
| 组员原件（可删） | 上级 `indoor_navigator/panorama.html`、`全景图/` |

---

## 常见任务模板

### H. 补全景房间标注（一栋/连廊）

```
本次请你：参照 js/room_labels_erdong.js，为 一栋-* 或 连廊-* 场景增加 pitch/yaw 房间点，
更新 panorama_full 左侧面板提示。不要改 panoramas 文件名。
```

### C. 扩展 JSON 坐标（下一层）

```
本次请你：组员提交 map_data/cad_pick_f2_b.json 后运行 apply_cad_coords.py，
并在 map.html JSON_GRAPHS 启用 2F。
```

### G. 推送 GitHub

```
本次请你：git status 后 commit 并 push（用户已授权）。
```

---

## 验证命令速查

```powershell
cd c:\Users\yoimi\indoor_navigator\PanoramaProject
python server_main.py

# 全景 + 二栋房间
# http://localhost:8000/panorama_full.html → 场景 二栋-1f-1

# CAD 取点
# http://localhost:8000/tools/pick-coords.html

# 1F 算路
python -m indoor_nav route node_nav/data/f1_b_graph.json room137_front washroom

python node_nav/scripts/export_all_cad_plans.py --dpi 400
python node_nav/scripts/apply_cad_coords.py map_data/cad_pick_f1_a.json
```

---

## 给 Agent 的提醒

1. **Windows + PowerShell**；用 `;` 分隔命令  
2. **全景房间坐标** = pitch/yaw（球面），**二维** = x_px/y_px（CAD PNG），勿混用  
3. `room_labels_erdong.js` 仅 **二栋**；修改后刷新 panorama_full 即可  
4. pick-coords 改 graph 节点后点「重新加载 JSON」  
5. 用户偏好：中文；最小改动；不主动 commit/push  

---

*最后更新：2026-06-03（全景二栋房间标注合并 + CAD A/B + 交接 Prompt 刷新）。*
