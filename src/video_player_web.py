import include.py_get_ip as get_ip
import os, re, socket, html
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
import socket

class MediaHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args): pass
    
    def list_directory(self, path):
        try:
            list_dir = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission")
            return None

        list_dir.sort(key=lambda a: (not os.path.isdir(os.path.join(path, a)), a.lower()))

        displaypath = html.escape(self.path)

        # 构造列表项 HTML
        items = []
        for name in list_dir:
            fullname = os.path.join(path, name)
            is_dir = os.path.isdir(fullname)
            icon = "📁" if is_dir else "📄"
            href = html.escape(name) + ("/" if is_dir else "")
            items.append(f'<li><a href="{href}"><span class="icon">{icon}</span>{html.escape(name)}</a></li>')
        items_html = '\n'.join(items)

        # 从模板加载页面（模板保存在 src/templates/list_directory.html）
        tpl_path = os.path.join(os.path.dirname(__file__), 'templates', 'list_directory.html')
        with open(tpl_path, 'r', encoding='utf-8') as f:
            tpl = f.read()
        content = tpl.replace('%%DISPLAYPATH%%', displaypath).replace('%%ITEMS%%', items_html)

        encoded = content.encode('utf-8')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        return None

    def do_GET(self):
        path = self.translate_path(self.path)
        if os.path.isfile(path) and self.headers.get('Range'):
            # 这里保留你原有的高性能流媒体传输逻辑
            size = os.path.getsize(path)
            range_h = self.headers.get('Range')
            m = re.search(r'bytes=(\d+)-(\d*)', range_h)
            if m:
                start = int(m.group(1))
                end = int(m.group(2)) if m.group(2) else size - 1
                self.send_response(206)
                self.send_header('Accept-Ranges', 'bytes')
                self.send_header('Content-Type', self.guess_type(path))
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
                self.send_header('Content-Length', str(end - start + 1))
                self.end_headers()
                with open(path, 'rb') as f:
                    f.seek(start)
                    remaining = end - start + 1
                    while remaining > 0:
                        chunk = f.read(min(128 * 1024, remaining))
                        if not chunk: break
                        self.wfile.write(chunk)
                        remaining -= len(chunk)
                return
        return super().do_GET()

class ThreadedServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    def handle_error(self, request, client_address): pass
    def server_bind(self):
        super().server_bind()
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
if __name__ == "__main__":
    print("http://localhost:80")
    print(get_ip.get_ip())
    ThreadedServer(('0.0.0.0', 80), MediaHandler).serve_forever()