import base64
import os
from datetime import datetime

from backend.settings import BASE_DIR


def handle_player_screenshot(player_uuid, content):
    parent_dir = os.path.join(BASE_DIR, "media")
    player_path = os.path.join(parent_dir, str(player_uuid))
    os.makedirs(player_path, exist_ok=True)
    path = os.path.join(player_path, "screenshot_" + datetime.utcnow().isoformat().replace(':', '-') + ".png")
    with open(path, "wb") as f:
        f.write(base64.decodebytes(content["screenshot"].encode("utf-8")))


