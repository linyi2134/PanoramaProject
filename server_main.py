import http.server
import socketserver
import webbrowser
import os

# 设置端口号
PORT = 8000

# 切换到当前文件所在的目录（也就是项目根目录）
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