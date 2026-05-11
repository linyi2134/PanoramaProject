import http.server
import socketserver
import webbrowser
import os
import sys

# 设置端口号
PORT = 8000

# 切换到资源目录：源码运行时为本文件目录；PyInstaller 单文件 exe 为解压目录
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 创建一个简单的 HTTP 服务器
Handler = http.server.SimpleHTTPRequestHandler

# 启动服务器（非阻塞方式，会在后台运行）
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"服务器已启动，地址: http://localhost:{PORT}")
    print("请在浏览器中打开 panorama.html")
    # 自动打开浏览器
    webbrowser.open(f"http://localhost:{PORT}/panorama.html")
    # 保持服务器运行
    httpd.serve_forever()