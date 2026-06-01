"""从 indoor_navigator/panorama(1).html 生成 PanoramaProject/panorama_full.html"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "panorama(1).html"
DST = Path(__file__).resolve().parents[1] / "panorama_full.html"

MAP_LINK = """
        <p style="margin-top:10px;font-size:12px;text-align:center;">
            <a href="map.html" style="color:#58a6ff;text-decoration:none;">🗺️ 二维地图导航</a>
            <span style="opacity:0.5;margin:0 6px;">|</span>
            <a href="panorama.html" style="color:#aaa;text-decoration:none;font-size:11px;">简易 demo</a>
        </p>
"""

PANORAMA_PREFIX = """
        const PANORAMA_BASE = 'panoramas/';
        for (const id of Object.keys(scenesConfig)) {
            const p = scenesConfig[id].panorama;
            if (p && !p.startsWith(PANORAMA_BASE)) scenesConfig[id].panorama = PANORAMA_BASE + p;
        }

"""

def main():
    src = SRC.read_text(encoding="utf-8")
    if MAP_LINK.strip() not in src:
        src = src.replace(
            '<button id="navigateBtn">🚀 开始导航</button>',
            '<button id="navigateBtn">🚀 开始导航</button>' + MAP_LINK,
        )
    marker = "        // ======================= 4. 初始化 Pannellum ======================="
    if "PANORAMA_BASE" not in src:
        src = src.replace(marker, PANORAMA_PREFIX + marker)
    src = src.replace(
        "<title>B7教学楼全景导航（完整版）</title>",
        "<title>B7教学楼全景导航（完整版·52场景）</title>",
    )
    DST.write_text(src, encoding="utf-8")
    print(f"Wrote {DST} ({len(src)} bytes)")


if __name__ == "__main__":
    main()
