# 跨楼层连接说明

## 写在哪里？

| 用途 | 文件 |
|------|------|
| **关系定义（机器读）** | [`cross_floor_links.json`](cross_floor_links.json) |
| **说明文档（人读）** | 本文件 |
| **同层路网** | `node_nav/data/f{1..5}_{a\|b}_graph.json` 内的 `nodes` / `edges` |
| **运行时生成跨层边** | `map.html` → `loadCrossFloorSpec()` 读 json，`crossEdges()` 拼进算路图 |
| **同层跨区（非换层）** | [`cross_floor_links.json`](cross_floor_links.json) → `zoneLinks` |

---

## B 座主竖向（1–5F，tab 1–5）

**同一物理位置**，各层 CAD 上方位不同，但节点 **统一命名**：

| nodeId | 标签 | 层 |
|--------|------|-----|
| `elevator` | **东侧电梯** | 1F–5F |
| `stair_east` | **东侧楼梯** | 1F–5F |
| `stair_west` | **西侧楼梯** | 1F–5F（平面图上 1/3F 标在南侧、2/4/5F 标在西侧，同一楼梯井） |

- **东侧井同层互通**：每层 graph 内 `elevator` ↔ `stair_east`，`weight = 1`
- **跨层**：JSON 内五层同 nodeId；**map 合并图**为 `b1_elevator`…`b5_elevator` 等，由 `crossEdges()` 读 **`bZone.unifiedVertical`** 串联（**每层 weight = 6**，见 `crossFloorWeight`）
- **map 运行时前缀**：B tab 1–5 → `b{n}_` + JSON 内 id（如 `b3_link_to_a`）

其他楼梯（如 `out_stair` / `stair_outdoor` 户外楼梯等）保持独立。

---

## A 座竖向（tab 8–12，即 A1F–A5F）

| nodeId | 标签 | 跨层范围 |
|--------|------|----------|
| `stair_south` | **南侧楼梯** | A1F–A5F（1F 原东南侧、2/4/5F 南侧、3F 原大楼楼梯） |
| `stair_small` | **东侧翼楼梯** | **仅 A1F–A3F**（物理上属 A 座东侧翼，非独立建筑） |

- **跨层**：`map.html` 为 A 座节点加前缀 `a1_`…`a5_`，竖向井由 `crossEdges` 按层串联（**每层 weight = 6**）
- 定义见 **`cross_floor_links.json` → `aZone`**

### 1F A 主楼 ↔ 东侧翼（不互通 · 经 2F 转）

**设计声明**：A1F **主楼环廊与东侧翼 1F 层内不连通**（门锁），不能同层步行穿梭。

标准路径：A1F 主楼 → `stair_south` 上 **A2F** → 通道至 `stair_small` 一侧 → 竖井上/下至东侧翼目标层（含 104 等）。

**f1_a graph**：保留 `room_104A/B` ↔ `stair_small` **翼内边**；**禁止** `fork_se → room_104*` 主楼直连。map 已删除旧「小楼」示意 tab，东侧翼仅 A1–3F JSON。

---

## A/B 座 ↔ 连廊（同层跨区）

每层一对连接（**weight = 15**，见 `zoneLinks`）：

| 层 | B 座 tab / JSON 节点 | 连廊 tab / 节点 | A 座 tab / 节点 | map 合并 id 示例 |
|----|---------------------|----------------|----------------|------------------|
| 1F | 1 · `link_to_a` | 14 · `link_to_b` | 8 · `link_to_b` | `b1_link_to_a` … `a1_link_to_b` |
| 2F | 2 · `link_to_a` | 15 · `link_to_b` | 9 · `link_to_b` | `b2_…` |
| 3F | 3 · `link_to_a` | 16 · `link_to_b` | 10 · `link_to_b` | `b3_…` |
| 4F | 4 · `link_to_a` | 17 · `link_to_b` | 11 · `link_to_b` | `b4_…` |
| 5F | 5 · `link_to_a` | 18 · `link_to_b` | 12 · `link_to_b` | `b5_…` |

JSON 内 nodeId 无前缀；map 由 `navNodeId(tab, nodeId)` 加 `b{n}_` / `lk{n}_` / `a{n}_` 前缀。

连廊图内：`link_to_b` — `outdoor_stair` — `link_to_a`（仅 `link_f*_graph.json`）。

**户外楼梯**只保留在连廊 JSON，已从 A/B 座 graph 删除。

---

## A-B 连廊竖向（tab 14–18）

五层同一节点 id：`outdoor_stair`（户外楼梯）。

跨层边在 **`cross_floor_links.json` → `linkCorridor`**，由 `map.html` 生成：

`lk1_outdoor_stair` — `lk2_…` — … — `lk5_outdoor_stair`，**每层 weight = 6**

---

## 修改后记得

1. 改 graph 或 json  
2. bump `map.html` 的 `GRAPH_CACHE_VER`  
3. Ctrl+F5 刷新
