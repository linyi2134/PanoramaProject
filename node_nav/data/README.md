# 楼内路网数据（`node_nav/data`）

## 文件命名

| 规则 | 示例 |
|------|------|
| `f{楼层}_{区}_graph.json` | `f1_a_graph.json` = 1 层 A 座 |
| 区：`a` / `b`（小写，对应 A 座 / B 座） | `f3_b_graph.json` = 3 层 B 座 |

总览见 **`index.json`**（列出全部图层及节点/边数量）。

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
| `zone` | `A` 或 `B` |
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

## 连廊命名

- A 座侧：`link_to_b`（接 B 区）
- B 座侧：`link_to_a`（接 A 区）

## 归档

旧文件名、示范图 `b1_b_zone_graph.json` 等在 **`_archive/`**，勿再引用。

## 重新整理

若批量改回旧格式后需再统一，在 `PanoramaProject` 下执行：

```bash
python node_nav/scripts/normalize_graphs.py
```
