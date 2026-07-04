import os
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from video_player_web.handler import MediaHandler, ThreadedServer
from video_player_web.utils.py_get_ip import get_ip


def main():
    port = 8000
    try:
        port = int(os.environ.get('VIDEO_PLAYER_PORT', sys.argv[1] if len(sys.argv) > 1 else 80))
    except Exception:
        port = 8000

    host = '0.0.0.0'
    try:
        print(f"Starting server: http://localhost:{port}")
        print("Local IP:", get_ip())
        ThreadedServer((host, port), MediaHandler).serve_forever()
    except Exception:
        print("Server failed to start:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()