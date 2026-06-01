# 全景图资源

52 张 `.jpg`，与 `panorama_full.html` 中场景 id 对应（如 `连廊-1f.jpg`）。

来源：`indoor_navigator/全景图/`（组员交付）。重新同步：

```powershell
Copy-Item "..\全景图\*.jpg" -Destination . -Force
```

或通过 `python tools/build_panorama_full.py` 仅重建 HTML（不复制图片）。
