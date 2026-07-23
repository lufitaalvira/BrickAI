"""
Configuration and constants for Brick Detection System
"""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
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

# Ekspor semua variabel
__all__ = [
    'PROJECT_ROOT',
    'MODEL_PATH',
    'ASSETS_PATH',
    'DATA_PATH',
    'CONFIDENCE_THRESHOLD',
    'IOU_THRESHOLD',
    'CLASS_NAMES',
    'MAX_FILE_SIZE',
    'ALLOWED_FORMATS',
    'APP_TITLE',
    'APP_ICON',
    'PAGE_LAYOUT',
    'CAMERA_WIDTH',
    'CAMERA_HEIGHT',
    'FPS',
    'PRIMARY_COLOR',
    'SECONDARY_COLOR',
    'BACKGROUND_COLOR'
]
