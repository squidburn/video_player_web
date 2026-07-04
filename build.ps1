$ErrorActionPreference = "Stop"

pyinstaller --clean --onefile `
  --paths src `
  --add-data "src/video_player_web/templates;video_player_web/templates" `
  src/video_player_web/main.py