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
        r = []
        r.append('<html><head><meta charset="utf-8"><title>File Server</title>')
        r.append('''<style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
                   background: #0f172a; color: #e2e8f0; margin: 0; padding: 40px; }
            .container { max-width: 800px; margin: 0 auto; background: #1e293b; 
                         padding: 20px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }
            h1 { font-size: 1.25rem; color: #38bdf8; margin-top: 0; padding-bottom: 10px; border-bottom: 1px solid #334155; }
            ul { list-style: none; padding: 0; }
            li { padding: 12px 0; border-bottom: 1px solid #334155; transition: background 0.2s; }
            li:last-child { border-bottom: none; }
            a { color: #f1f5f9; text-decoration: none; display: flex; align-items: center; }
            a:hover { color: #38bdf8; }
            .icon { margin-right: 12px; font-size: 1.2rem; }
        </style></head><body><div class="container">''')
        
        r.append(f'<h1>Index of {displaypath}</h1><ul>')
        
        for name in list_dir:
            fullname = os.path.join(path, name)
            is_dir = os.path.isdir(fullname)
            icon = "📁" if is_dir else "📄"
            r.append(f'<li><a href="{html.escape(name)}{"/" if is_dir else ""}">'
                     f'<span class="icon">{icon}</span>{name}</a></li>')
            
        r.append('</ul></div></body></html>')
        
        encoded = '\n'.join(r).encode('utf-8')
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