import os

APP_NAME = "停车场管理系统"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

DATABASE_DIR = os.path.join(os.path.dirname(__file__), "data")
DATABASE_FILE = os.path.join(DATABASE_DIR, "parking.db")
BACKUP_DIR = os.path.join(DATABASE_DIR, "backups")

DEFAULT_CONFIG = {
    "total_spaces": 50,
    "free_duration": 30,
    "daily_cap": 100,
    "rates": {
        "小型车": 5.0,
        "大型车": 8.0,
        "新能源车": 3.0
    },
    "areas": ["A区", "B区", "C区", "D区"]
}

os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)