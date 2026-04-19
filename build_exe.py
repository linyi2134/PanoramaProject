# build_exe.py - 用于生成 .exe 的辅助脚本
# 运行方式：python build_exe.py

import os
import subprocess

# 确保在项目根目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# PyInstaller 打包命令
# --onefile: 打包成单个 exe
# --windowed: 不显示控制台窗口（GUI 模式）
# --name: 生成的 exe 名称
# --add-data: 包含额外的文件（html 和图片）
cmd = [
    "pyinstaller",
    "--onef(.venv) PS E:\PanoramaProject> pip install pyinstaller==6.10.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
ERROR: Ignored the following versions that require a different python version: 4.10 Requires-Python >=3.6,<3.11; 4.6 Requires-Python >=3.6,<3.11; 4.7 Requires-Python >=3.6,<3.11; 4.8 Requires-Python >=3.6,<3.11; 4.9 Requires-Python >=3.6,<3.11; 5.0 Requires-Python >=3.7,<3.11; 5.0.1 Requires-Python >=3.7,<3.11; 5.1 Requires-Python >=3.7,<3.11; 5.10.0 Requires-Python >=3.7,<3.12; 5.10.1 Requires-Python >=3.7,<3.12; 5.11.0 Requires-Python >=3.7,<3.12; 5.12.0 Requires-Python >=3.7,<3.12; 5.13.0 Requires-Python >=3.7,<3.13; 5.13.1 Requires-Python >=3.7,<3.13; 5.13.2 Requires-Python >=3.7,<3.13; 5.2 Requires-Python >=3.7,<3.11; 5.3 Requires-Python >=3.7,<3.11; 5.4 Requires-Python >=3.7,<3.11; 5.4.1 Requires-Python >=3.7,<3.11; 5.5 Requires-Python >=3.7,<3.12; 5.6 Requires-Python >=3.7,<3.12; 5.6.1 Requires-Python >=3.7,<3.12; 5.6.2 Requires-Python >=3.7,<3.12; 5.7.0 Requires-Python >=3.7,<3.12; 5.8.0 Requires-Python >=3.7,<3.12; 5.9.0 Requires-Python >=3.7,<3.12; 6.0.0 Requires-Python >=3.8,<3.13; 6.1.0 Requires-Python >=3.8,<3.13; 6.10.0 Requires-Python >=3.8,<3.14; 6.11.0 Requires-Python >=3.8,<3.14; 6.11.1 Requires-Python >=3.8,<3.14; 6.12.0 Requires-Python >=3.8,<3.14; 6.13.0 Requires-Python >=3.8,<3.14; 6.14.0 Requires-Python >=3.8,<3.14; 6.14.1 Requires-Python >=3.8,<3.14; 6.14.2 Requires-Python >=3.8,<3.14; 6.2.0 Requires-Python >=3.8,<3.13; 6.3.0 Requires-Python >=3.8,<3.13; 6.4.0 Requires-Python >=3.8,<3.13; 6.5.0 Requires-Python >=3.8,<3.13; 6.6.0 Requires-Python >=3.8,<3.13; 6.7.0 Requires-Python >=3.8,<3.13; 6.8.0 Requires-Python >=3.8,<3.13; 6.9.0 Requires-Python >=3.8,<3.13
ERROR: Could not find a version that satisfies the requirement pyinstaller==6.10.0 (from versions: 2.0, 2.1, 3.0, 3.1, 3.1.1, 3.2, 3.2.1, 3.3, 3.3.1, 3.4, 3.5, 3.6, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.5.1, 6.15.0, 6.16.0, 6.17.0, 6.18.0, 6.19.0)
ERROR: No matching distribution found for pyinstaller==6.10.0     ile",
    "--windowed",
    "--name", "PanoramaNav",
    "--add-data", f"panorama.html{os.pathsep}.",
    "--add-data", f"panorama.jpg{os.pathsep}.",
    "server_main.py"
]

print("开始打包...")
subprocess.run(cmd)
print("打包完成！exe 文件在 dist 目录下")