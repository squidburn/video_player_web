# video_player_web

一个基于 Python 标准库的本地媒体文件浏览与流式播放服务。

## 功能特点

- 浏览当前目录下的文件和子目录
- 支持视频/音频文件的在线播放
- 支持 `Range` 请求，适合大文件流媒体
- 可直接打包为单文件可执行程序

## 项目结构

```text
video_player_web/
├─ src/
│  └─ video_player_web/
│     ├─ __init__.py
│     ├─ handler.py
│     ├─ main.py
│     ├─ templates/
│     │  └─ list_directory.html
│     └─ utils/
│        ├─ __init__.py
│        └─ py_get_ip.py
├─ build.ps1
├─ .vscode/
│  └─ launch.json
└─ README.md
```

## 运行方式

### 1. 直接运行源码

```powershell
cd D:\squidburn\program\python\video_player_web
.\.venv\Scripts\python.exe src\video_player_web\main.py 80
```

然后在浏览器访问：

```text
http://localhost/
```

### 2. 使用 VS Code 调试

已提供 `.vscode/launch.json`，直接按 F5 即可运行。

## 打包为单文件 exe

在项目根目录执行：

```powershell
.
\build.ps1
```

打包结果会生成到 `dist/` 目录下。

## 各文件说明

### `src/video_player_web/handler.py`

负责处理 HTTP 请求：

- `MediaHandler`：继承自 `SimpleHTTPRequestHandler`
- `list_directory()`：自定义目录列表页面，使用模板文件渲染
- `do_GET()`：处理带 `Range` 请求的媒体文件分段传输
- `ThreadedServer`：多线程 HTTP 服务，支持并发请求

### `src/video_player_web/main.py`

程序入口：

- 读取端口参数（默认 8000）
- 创建并启动 `ThreadedServer`
- 打印服务地址与本机 IP

### `src/video_player_web/templates/list_directory.html`

目录浏览页模板，HTML 结构与样式单独放在这里，便于修改界面。

### `src/video_player_web/utils/py_get_ip.py`

用于获取本机局域网 IP，方便在终端中显示可访问地址。

## 常见说明

- 建议使用 80 端口，但在 Windows 上某些环境下需要管理员权限。
- 如果 80 端口被占用或权限不足，可改为 8000、8080 等端口。
- 如需外部访问，请确保防火墙允许对应端口。
