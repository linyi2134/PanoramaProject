# 楼内路网数据（`node_nav/data`）

## 文件命名

| 规则 | 示例 |
|------|------|
| `f{楼层}_{区}_graph.json` | `f1_a_graph.json` = 1 层 A 座 |
| 区：`a` / `b`（小写） | `f3_b_graph.json` = 3 层 B 座 |
| **`link_f{楼层}_graph.json`** | **`link_f1_graph.json` = 1 层 A-B 连廊**（`meta.zone`: `LINK`） |

总览见 **`index.json`**（A/B 10 份 + 连廊 5 份）。

## JSON 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `description` | string | 如 `1F-A座`（原 `explain` 已统一） |
| `isFinished` | boolean | 该层数据是否定稿（原 `isfinish`） |
| `meta` | object | 见下表 |
| `nodes` | array | 节点 |
| `edges` | array | 无向边，`weight` 为步行距离（米） |
| `facilities` | array | 设施 POI，通过 `nodeId` 挂到节点 |

### `meta`

| 字段 | 说明 |
|------|------|
| `building` | 楼栋，如 `B7`（原 `area` 已改） |
| `floor` | 楼层数字 |
| `zone` | `A`、`B` 或 **`LINK`**（连廊） |
| `units` | 距离单位，默认 `meter` |
| `note` | 备注 |

## 节点 `nodes[]`

| 字段 | 说明 |
|------|------|
| `id` | **snake_case、英文**，无空格（如 `link_to_a`、`office101_front`） |
| `label` | 界面显示用中文名 |
| `floor` | 与 `meta.floor` 一致 |
| `role` | `corridor` / `door` / `vertical` / `facility` / `room` |
| `x_px`, `y_px` | 可选，相对平面图像素坐标（地图 UI 用） |

## 连廊（LINK）

- 文件：`link_f1_graph.json` … `link_f5_graph.json`
- 1F 底图 `plans/link_f1_cad.png`；2–5F 共用 `plans/link_f2_cad.png`（复制为 f3–f5）
- 统一节点 id：`link_to_b`、`link_to_a`、`outdoor_stair`；**1F 另有 `entrance`**
- 1F 边：向B→入口→楼梯→向A（weight 10-5-10）；2–5F：向B→楼梯→向A（15-10）
- `map.html` 显示时节点带前缀 `lk1_`…`lk5_`（防跨层 id 冲突）；JSON 文件内无前缀
- pick-coords 分区选 **「连廊（A-B）」**

## 连廊与 A/B 座衔接命名

- A 座侧：`link_to_b`（接 B 区）
- B 座侧：`link_to_a`（接 A 区）

## 归档

旧文件名、示范图 `b1_b_zone_graph.json` 等在 **`_archive/`**，勿再引用。

## 重新整理

若批量改回旧格式后需再统一，在 `PanoramaProject` 下执行：

```bash
python node_nav/scripts/normalize_graphs.py
```

## 合规校验（推荐合并 graph 前执行）

要求：**每个 node 至少一条 edge；全图连通**。

```bash
python node_nav/scripts/check_graph.py node_nav/data/f4_b_graph.json
python node_nav/scripts/diff_graph.py          # 对比上级 ../*_graph.json 与 data/
python node_nav/scripts/check_cad_pick.py map_data/cad_pick_f4_b.json
```

pick-coords 只加载 **`node_nav/data/*_graph.json`**（含 `link_f*_graph.json`）；改 graph 后须点 **「重新加载 JSON」**。fetch 带 `GRAPH_CACHE_VER` 防浏览器缓存。

