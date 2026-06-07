import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_NAME = "ocr_history.db"
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

HISTORY_TABLE = "ocr_records"

SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

LANGUAGES = {
    "中文": "chi_sim",
    "英文": "eng",
    "中英文混合": "chi_sim+eng"
}

MODES = {
    "快速模式": "--oem 3 --psm 6",
    "精准模式": "--oem 3 --psm 6"
}

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = "OCR 图片文字识别工具"

PREVIEW_SIZE = (400, 400)

DEFAULT_LANGUAGE = "中英文混合"
DEFAULT_MODE = "精准模式"
AUTO_COPY_TO_CLIPBOARD = True
