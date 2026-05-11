# build_exe.py - 用于生成 .exe 的辅助脚本
# 运行方式：python build_exe.py
# 需先安装：pip install pyinstaller

import os
import subprocess
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)


def add_data(src: str) -> str:
    """PyInstaller --add-data：SRC{pathsep}. （当前目录为解压资源目标）"""
    return f"{src}{os.pathsep}."


# 与 panorama.html 中引用的全景图一致
ASSETS = [
    "panorama.html",
    "corridor.jpg",
    "lobby.jpg",
    "outer_stair.jpg",
    "inner_stair.jpg",
    "second_floor.jpg",
]

cmd = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--name",
    "PanoramaNav",
]
for path in ASSETS:
    cmd.extend(["--add-data", add_data(path)])
cmd.append("server_main.py")

print("开始打包...")
ret = subprocess.run(cmd)
print("打包完成！exe 文件在 dist 目录下" if ret.returncode == 0 else "打包失败，请查看上方错误信息。")
sys.exit(ret.returncode)
