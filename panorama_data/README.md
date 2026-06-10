# 全景数据说明

## 文件

| 文件 | 说明 |
|------|------|
| `../panoramas/*.jpg` | 52 张全景图，文件名 = 场景 id（如 `二栋-1f-1.jpg`） |
| `../js/room_labels_all.js` | **一栋 / 二栋 / 三栋** 房间标注（47 场景、213+ 点） |
| `../js/panorama_map_bridge.js` | **走廊节点 ↔ 全景场景** 对照（与房间蓝点独立） |
| `../panorama_full.html` | 完整全景：跳转引导 + 房间蓝点 + **二维深链** |

默认场景为 **连廊-1f**（无房间标注）；进入 **二栋-1f-1** 等才有蓝点。请用 **panorama_full.html**，不是 5 场景 demo 的 `panorama.html`。

## 两类标注（勿混淆）

| 类型 | 数据 | 用途 |
|------|------|------|
| **房间蓝点** | `room_labels_all.js` → `ROOM_DATA_BY_SCENE` | 房间内 pitch/yaw；「按房间号导航」 |
| **走廊↔全景** | `panorama_map_bridge.js` | 四分叉、楼梯口等与全景站位对照；二维/全景深链 |

房间蓝点的 `pitch/yaw` 与二维 `x_px/y_px` **未自动同步**。走廊对照见 [map_data/panorama_map_bridge.md](../map_data/panorama_map_bridge.md)。

## 房间标注

| 分区 | 场景数 | 说明 |
|------|--------|------|
| 二栋 | 22 | B7 主楼（B 座全景） |
| 一栋 | 22 | A 区办公楼 |
| 三栋 | 3 | 小楼（↔ 二维 `a{n}_stair_small`） |
| 连廊 | 5 | 无房间蓝点；↔ 二维 `lk{n}_outdoor_stair` |

### 增改房间标注

1. 编辑 `js/room_labels_all.js` 中 `window.ROOM_DATA_BY_SCENE`
2. 有 `rawNumber` 的条目进入「按房间号导航」下拉框
3. 刷新 `panorama_full.html`（Ctrl+F5）

### 增改走廊↔全景对照

改 `js/panorama_map_bridge.js` → 更新 `map_data/panorama_map_bridge.md` → bump script `?v=`。

## 场景 id 与建筑

| 前缀 | 建筑 | 二维对照要点 |
|------|------|----------------|
| `二栋-` | B 座（软件学院） | suffix 1–4 → 四分叉 |
| `一栋-` | A 座办公楼 | 1F 两场景；2–5F 南侧楼梯+四分叉 |
| `连廊-` | 连廊 | 各层 → `outdoor_stair` |
| `三栋-` | 小楼（翼内视角） | 1–3F → A 座 `stair_small` |

## 二维深链

| 入口 | URL 示例 |
|------|----------|
| 全景指定场景 | `panorama_full.html?scene=二栋-1f-1` |
| 二维指定起点 | `map.html?start=b1_fork_sw` |

全景侧栏「二维地图（…）」链到当前场景对应的二维节点；从二维点击对照节点可弹窗进入全景。

## 运行

```powershell
cd PanoramaProject
python server_main.py
# http://localhost:8000/panorama_full.html
# http://localhost:8000/map.html
```

上级 `indoor_navigator/新全景图标注/` 为组员交付原件；合并后以 `js/room_labels_all.js` 为准。

---

*最后更新：2026-06-10*
