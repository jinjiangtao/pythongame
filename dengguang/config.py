import pygame
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "灯光迷阵"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)
RED = (255, 50, 50)
PURPLE = (150, 50, 200)

BUTTON_COLOR = BLUE
BUTTON_HOVER_COLOR = (70, 170, 255)
BUTTON_TEXT_COLOR = WHITE

CELL_ON_COLOR = YELLOW
CELL_OFF_COLOR = GRAY
CELL_HOVER_COLOR = ORANGE
CELL_BORDER_COLOR = BLACK
CELL_GLOW_COLOR = (255, 255, 100)

OBSTACLE_COLOR = (60, 60, 60)
FROZEN_COLOR = (100, 150, 255)

FONT_SIZE_SMALL = 20
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 36
FONT_SIZE_XLARGE = 48
FONT_SIZE_XXLARGE = 64

pygame.font.init()

def get_chinese_font():
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/kaiu.ttf",
        "C:/Windows/Fonts/fangsong.ttf",
        "/Library/Fonts/SimHei.ttf",
        "/Library/Fonts/Songti.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/arphic/ukai.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path
    return None

CHINESE_FONT_PATH = get_chinese_font()

if CHINESE_FONT_PATH:
    try:
        FONT_SMALL = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_SMALL)
        FONT_MEDIUM = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_MEDIUM)
        FONT_LARGE = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_LARGE)
        FONT_XLARGE = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_XLARGE)
        FONT_XXLARGE = pygame.font.Font(CHINESE_FONT_PATH, FONT_SIZE_XXLARGE)
    except:
        FONT_SMALL = pygame.font.Font(None, FONT_SIZE_SMALL)
        FONT_MEDIUM = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        FONT_LARGE = pygame.font.Font(None, FONT_SIZE_LARGE)
        FONT_XLARGE = pygame.font.Font(None, FONT_SIZE_XLARGE)
        FONT_XXLARGE = pygame.font.Font(None, FONT_SIZE_XXLARGE)
else:
    FONT_SMALL = pygame.font.Font(None, FONT_SIZE_SMALL)
    FONT_MEDIUM = pygame.font.Font(None, FONT_SIZE_MEDIUM)
    FONT_LARGE = pygame.font.Font(None, FONT_SIZE_LARGE)
    FONT_XLARGE = pygame.font.Font(None, FONT_SIZE_XLARGE)
    FONT_XXLARGE = pygame.font.Font(None, FONT_SIZE_XXLARGE)

MAX_HINTS = 3

SOUND_VOLUME = 0.5
MUSIC_VOLUME = 0.3

CELL_ANIMATION_DURATION = 150
VICTORY_ANIMATION_DURATION = 2000
TRANSITION_DURATION = 500

GAME_MODES = {
    "classic": {"name": "经典模式", "description": "无时间和步数限制"},
    "timed": {"name": "限时模式", "description": "在限定时间内通关"},
    "limited_steps": {"name": "限步模式", "description": "在限定步数内通关"}
}

DIFFICULTIES = {
    "easy": {"name": "简单", "time_limit": 0, "step_limit": 0, "hint_count": 5},
    "normal": {"name": "普通", "time_limit": 120, "step_limit": 30, "hint_count": 3},
    "hard": {"name": "困难", "time_limit": 60, "step_limit": 20, "hint_count": 2},
    "expert": {"name": "专家", "time_limit": 30, "step_limit": 15, "hint_count": 1}
}

STAR_THRESHOLDS = {
    "time": {1: 120, 2: 60, 3: 30},
    "steps": {1: 30, 2: 20, 3: 10}
}