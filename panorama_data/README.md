# 全景数据说明

## 文件

| 文件 | 说明 |
|------|------|
| `../panoramas/*.jpg` | 52 张全景图，文件名 = 场景 id（如 `二栋-1f-1.jpg`） |
| `../js/room_labels_all.js` | **一栋 / 二栋 / 三栋** 房间标注（47 场景、213 点） |
| `../backup/misc/room_labels_erdong.js` | 旧版仅二栋（已归档；现用 `room_labels_all.js`） |
| `../panorama_full.html` | 完整全景：⚡立即跳转 + 🚶逐步引导 + 场景/房间号导航 + 蓝点 |

默认场景为 **连廊-1f**（无房间标注）；进入 **二栋-1f-1** 等才有蓝点。请打开 **panorama_full.html**，不是 5 场景 demo 的 `panorama.html`。

## 房间标注

| 分区 | 场景数 | 说明 |
|------|--------|------|
| 二栋 | 22 | B7 主楼（软件学院） |
| 一栋 | 22 | A 区办公楼 |
| 三栋 | 3 | 小楼 |
| 连廊 | 0 | 仅场景跳转，无房间点 |

坐标为 Pannellum 球面 `pitch` / `yaw`，与二维 `node_nav/data/*.json` 的 `x_px/y_px` **未打通**。

### 增改房间标注

1. 编辑 `js/room_labels_all.js` 中 `window.ROOM_DATA_BY_SCENE`
2. 有 `rawNumber` 的条目会进入「按房间号导航」下拉框
3. 刷新 http://localhost:8000/panorama_full.html

### 场景 id 与建筑

| 前缀 | 建筑 |
|------|------|
| `二栋-` | B7 主楼（软件学院，B 座全景） |
| `一栋-` | A 区办公楼 |
| `连廊-` | 连廊 |
| `三栋-` | 小楼 |

## 运行

```bash
cd PanoramaProject
python server_main.py
# http://localhost:8000/panorama_full.html
```

上级目录 `indoor_navigator/新全景图标注/` 为组员交付原件；合并后数据以 `js/room_labels_all.js` 为准。

