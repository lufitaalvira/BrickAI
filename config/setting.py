"""
Configuration and constants for Brick Detection System
"""
import sys
from pathlib import Path

# Tentukan PROJECT_ROOT dengan cara yang lebih robust
if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).parent.parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Paths
MODEL_PATH = PROJECT_ROOT / "model" / "best.pt"
ASSETS_PATH = PROJECT_ROOT / "assets"
DATA_PATH = PROJECT_ROOT / "data"

# Model Config
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45
CLASS_NAMES = {
    0: "Setengah Matang",
    1: "Matang"
}

# Upload Config
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
ALLOWED_FORMATS = ['jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov']

# App Config
APP_TITLE = "🧱 Sistem Deteksi Bata Real-time"
APP_ICON = "🧱"
PAGE_LAYOUT = "wide"

# Display Config
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FPS = 30

# Colors
PRIMARY_COLOR = "#e86930"
SECONDARY_COLOR = "#1a1a1a"
BACKGROUND_COLOR = "#f5f1e8"

