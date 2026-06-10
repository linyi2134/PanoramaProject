# 二维地图 ↔ 全景场景对照

> 实现文件：`js/panorama_map_bridge.js`  
> 消费方：`map.html`（点击节点弹窗进全景）、`panorama_full.html`（深链回二维并设起点）

---

## 1. 作用

| 方向 | 行为 |
|------|------|
| **二维 → 全景** | 点击有对照的节点 → 弹窗「是否进入全景」→ `panorama_full.html?scene=…` |
| **全景 → 二维** | 侧栏「二维地图（…）」→ `map.html?start=…` → 自动切 tab、**起点已设**、等待选终点 |

有对照的节点在 `map.html` 上带**蓝色虚线外圈**提示。

---

## 2. 对照表（权威）

### B 区 · 二栋（`b{n}_` · tab 1–5）

全景 suffix **1–4** 对应四分叉（每层 B1F–B5F 规则相同）：

| 全景场景 | 二维 nodeId（JSON 内 local id） |
|----------|--------------------------------|
| `二栋-{n}f-1` | `fork_sw` 西南分叉 |
| `二栋-{n}f-2` | `fork_nw` 西北分叉 |
| `二栋-{n}f-3` | `fork_se` 东南分叉 |
| `二栋-{n}f-4` | `fork_ne` 东北分叉 |

`二栋-{n}f-5`（电梯区）**暂无**二维对照。

### A 区 · 一栋（`a{n}_` · tab 8–12）

**2F–5F**（每层 5 个全景场景）：

| 全景 suffix | 二维 local id |
|-------------|---------------|
| 1 | `stair_south` 南侧楼梯 |
| 2 | `fork_se` 东南分叉 |
| 3 | `fork_sw` 西南分叉 |
| 4 | `fork_nw` 西北分叉 |
| 5 | `fork_ne` 东北分叉 |

**1F 仅 2 个全景场景**：

| 全景 | 二维 local id |
|------|---------------|
| `一栋-1f-1` | `fork_nw` 西北分叉 |
| `一栋-1f-2` | `stair_south` 南侧楼梯 |

### 连廊（`lk{n}_` · tab 14–18）

| 全景 | 二维 local id |
|------|---------------|
| `连廊-{n}f` | `outdoor_stair` 户外楼梯（每层统一） |

### 三栋 · 小楼（`a{n}_stair_small` · 仅 1–3F）

| 全景 | 二维 nodeId | 说明 |
|------|-------------|------|
| `三栋-1f` | `a1_stair_small` | A1F 东侧翼小楼楼梯 |
| `三栋-2f` | `a2_stair_small` | A2F |
| `三栋-3f` | `a3_stair_small` | A3F |

全景里的「三栋」对应二维 **A 座 tab** 上的 `stair_small`，不是独立第八个 tab。

---

## 3. URL 深链

```
# 二维 → 全景
panorama_full.html?scene=二栋-1f-1

# 全景 → 二维（自动起点）
map.html?start=b1_fork_sw
map.html?start=a2_stair_small
map.html?start=lk3_outdoor_stair
```

API（浏览器全局）：

```javascript
PanoramaMapBridge.nodeToPanoramaScene('b1_fork_sw');  // → '二栋-1f-1'
PanoramaMapBridge.panoramaSceneToMapNode('三栋-2f'); // → { navNodeId: 'a2_stair_small', tab: 9, ... }
PanoramaMapBridge.hasPanoramaLink('a1_stair_small'); // → true
```

---

## 4. 扩展对照

1. 在 `panorama_map_bridge.js` 增加 suffix / 场景解析逻辑  
2. bump `map.html` 与 `panorama_full.html` 中 script 的 `?v=` 参数  
3. 手动测：二维点击 → 全景场景正确；全景链接 → 二维 tab + 起点正确  

**不要**在 `room_labels_all.js` 里硬编码二维 id；房间蓝点与走廊对照是两套数据。

---

## 5. 与算路的关系

- 对照仅影响**跳转**，不参与 Dijkstra 边权。  
- `map.html` **同层起终点**会禁用楼梯/电梯竖向边（避免同层绕路上下楼）；**例外**：A1F 主楼↔小楼翼跨子图时保留 A 座竖向边（见 `sameFloorVerticalPolicy`）。  

---

*最后更新：2026-06-10*
