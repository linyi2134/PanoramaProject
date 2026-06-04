# PanoramaProject · 校园导览与信息导航系统

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Course%20Project-lightgrey)]()
[![GitHub](https://img.shields.io/badge/GitHub-linyi2134%2FPanoramaProject-181717?logo=github)](https://github.com/linyi2134/PanoramaProject)

B7 教学楼室内导航课程项目：**360° 全景漫游** + **楼内路网最短路径（Dijkstra）**。  
主路线为「二维地图 + 搜索起终点」；全景作为可选辅助体验。

> 仓库地址：[github.com/linyi2134/PanoramaProject](https://github.com/linyi2134/PanoramaProject)

---

## 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [路网数据](#路网数据)
- [路径规划用法](#路径规划用法)
- [打包为 exe](#打包为-exe)
- [开发路线](#开发路线)
- [文档](#文档)
- [参与贡献](#参与贡献)
- [许可证](#许可证)

---

## 功能特性

| 模块 | 状态 | 说明 |
|------|------|------|
| 二维地图导航 | ✅ 可用 | `map.html`：13 层示意（B7 + 小楼 + A 区）、起终点、Dijkstra 路径 |
| 全景完整漫游 | ✅ 可用 | `panorama_full.html`：52 场景；二栋房间蓝点（`js/room_labels_erdong.js`）+ BFS 导航 |
| 全景 demo | ✅ 可用 | `panorama.html`：5 场景入门演示 |
| 楼内路网数据 | ✅ 进行中 | B7 **1–5 层 × A/B 座** 共 10 份 `graph.json`；**1F B 区** 已接地图坐标 |
| 最短路径算法 | ✅ 可用 | Python `indoor_nav` + `js/pathfind.browser.js`（Dijkstra） |
| 设施最近查找 | ✅ 可用 | 地图「最近厕所」+ 命令行 `nearest` |
| 自动室内定位 | ⏸ 不做 | 采用用户选点 / 搜索；可选二维码定点 |

---

## 技术栈

| 层次 | 技术 |
|------|------|
| 全景前端 | HTML + [Pannellum 2.5.6](https://github.com/mpetroff/pannellum)（CDN） |
| 本地服务 | Python 标准库 `http.server` |
| 路径规划 | Dijkstra（`heapq` / 浏览器 JS） |
| 数据格式 | JSON（`nodes` / `edges` / `facilities`） |
| 打包 | PyInstaller（可选，生成 Windows `.exe`） |

原课程方案中的 Qt/OpenGL 路线已由 **Web + Python** 替代，便于迭代与演示。

---

## 项目结构

```
PanoramaProject/
├── server_main.py          # 本地 HTTP 服务（默认端口 8000，默认打开 map.html）
├── map.html                # 二维导航主入口
├── panorama_full.html      # 全景完整版（52 场景）
├── panorama.html           # 全景 demo（5 场景）
├── panoramas/              # 完整版全景 jpg（约 300MB+）
├── js/room_labels_erdong.js # 二栋全景房间标注 pitch/yaw
├── panorama_data/README.md  # 全景与房间标注说明
├── js/pathfind.browser.js  # 浏览器端 Dijkstra
├── build_exe.py            # PyInstaller 打包脚本
├── corridor.jpg …          # demo 全景图（5 张）
├── indoor_nav/             # Python 路径规划模块
│   ├── dijkstra.py
│   └── __main__.py         # 命令行：route / nearest
├── node_nav/
│   ├── data/               # 楼内路网 JSON（正式数据）
│   │   ├── index.json      # 各层索引
│   │   ├── f1_a_graph.json … f5_b_graph.json
│   │   └── README.md       # 数据字段约定
│   ├── src/
│   │   ├── pathfind.js     # 浏览器端 Dijkstra
│   │   ├── index.js        # Node 示例
│   │   └── run-b1b.js
│   └── scripts/
│       └── normalize_graphs.py
├── plans/                  # （计划）各层平面图 PNG
└── docs/ 等 *.md           # 方案与周报（仓库根目录）
```

---

## 快速开始

### 环境要求

- Python **3.10+**（仅标准库即可跑服务；打包需 `pyinstaller`）
- 现代浏览器（Chrome / Edge / Firefox）
- （可选）Node.js：仅用于运行 `node_nav` 下的示例脚本

### 1. 克隆仓库

```bash
git clone https://github.com/linyi2134/PanoramaProject.git
cd PanoramaProject
```

### 2. 启动本地服务

```bash
python server_main.py
```

浏览器将自动打开：

- 二维地图：<http://localhost:8000/map.html>
- 全景完整版：<http://localhost:8000/panorama_full.html>
- 全景 demo：<http://localhost:8000/panorama.html>

> 首次 `git clone` 因 `panoramas/` 体积较大，下载时间会偏长。

### 3. 命令行试算路径（Python）

在 `PanoramaProject` 目录下：

```bash
# 两点最短路
python -m indoor_nav route node_nav/data/f1_a_graph.json washroom a_door

# 从某节点找最近「洗手间」
python -m indoor_nav nearest node_nav/data/f1_b_graph.json 洗手间 room137_front
```

### 4. Node 示例（可选）

```bash
node node_nav/src/run-b1b.js
```

---

## 路网数据

- **命名**：`f{楼层}_{区}_graph.json`（区：`a` = A 座，`b` = B 座）
- **示例**：`f1_a_graph.json` = 1 层 A 座
- **字段说明**：见 [node_nav/data/README.md](node_nav/data/README.md)
- **总览**：见 [node_nav/data/index.json](node_nav/data/index.json)

每层 JSON 结构概要：

```json
{
  "description": "1F-A座",
  "isFinished": false,
  "meta": {
    "building": "B7",
    "floor": 1,
    "zone": "A",
    "units": "meter"
  },
  "nodes": [{ "id": "washroom", "label": "洗手间", "floor": 1, "role": "facility" }],
  "edges": [{ "from": "washroom", "to": "a_door", "weight": 6 }],
  "facilities": [{ "id": "poi_wash", "type": "洗手间", "nodeId": "washroom", "label": "洗手间" }]
}
```

节点 `id` 使用 **snake_case**（无空格）。地图 UI 计划增加可选字段 `x_px`、`y_px`。

---

## 路径规划用法

### Python API

```python
from indoor_nav import load_graph_json, shortest_path, nearest_facility_by_type

g = load_graph_json("node_nav/data/f1_b_graph.json")
route = shortest_path(g, "room137_front", "washroom")
# route["distance"], route["path_node_ids"], route["path_labels"]

near = nearest_facility_by_type(g, "mobile_room", "楼梯")
```

### JavaScript（与 Python 同构）

```javascript
import { dijkstra, nearestFacility } from "./node_nav/src/pathfind.js";
// graph 为与 JSON 同结构的对象
```

---

## 打包为 exe

```bash
pip install pyinstaller
python build_exe.py
```

生成单文件可执行程序，内嵌全景资源与静态页；双击后启动本地服务并打开浏览器。

---

## 开发路线

| 阶段 | 内容 |
|------|------|
| 已完成 | 全景原型、10 层路网 JSON、Dijkstra 双端实现、数据规范与 GitHub 托管 |
| 进行中 | 各层 `edges` / 边权实地校对，`isFinished` 标记 |
| 下一步 | `plans/*.png` 平面图 → 节点 `x_px/y_px` → `map.html` MVP |
| 后续 | 多层切换、搜索起终点、全景与地图节点映射 |

详见：[二维地图主导-分阶段推进方案.md](二维地图主导-分阶段推进方案.md)

---

## 文档

| 文档 | 说明 |
|------|------|
| [node_nav/data/README.md](node_nav/data/README.md) | 路网 JSON 规范 |
| [扩展方案与技术栈建议.md](扩展方案与技术栈建议.md) | 技术选型与扩展方向 |
| [二维地图主导-分阶段推进方案.md](二维地图主导-分阶段推进方案.md) | 地图 MVP 分阶段计划 |

---

## 参与贡献

1. Fork 本仓库并创建分支（如 `feature/map-mvp`）。
2. 修改路网时请编辑 `node_nav/data/f*_graph.json`，勿改 `_archive/` 内历史文件。
3. 大图 JSON 变更后运行：`python -m indoor_nav route …` 做连通性抽查。
4. 提交 Pull Request 并简要说明楼层与改动范围。

数据整理脚本：

```bash
python node_nav/scripts/normalize_graphs.py
```

---

## 许可证

本项目为课程实践项目，全景素材与楼内数据仅供教学演示。第三方库遵循各自许可证（如 Pannellum、PyInstaller）。

---

## 致谢

- [Pannellum](https://pannellum.org/) — 全景查看
- 课程方案参考 indoor-wayfinder 等开源项目的图结构与 Dijkstra 思路

---

<p align="center">
  <sub>知途 · IT创新实践导论 · B7 教学楼</sub>
</p>
