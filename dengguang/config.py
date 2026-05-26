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
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (50, 150, 255)
GREEN = (0, 200, 0)

BUTTON_COLOR = BLUE
BUTTON_HOVER_COLOR = (70, 170, 255)
BUTTON_TEXT_COLOR = WHITE

CELL_ON_COLOR = YELLOW
CELL_OFF_COLOR = GRAY
CELL_HOVER_COLOR = ORANGE
CELL_BORDER_COLOR = BLACK

FONT_SIZE_SMALL = 20
FONT_SIZE_MEDIUM = 24
FONT_SIZE_LARGE = 36
FONT_SIZE_XLARGE = 48

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
    except:
        FONT_SMALL = pygame.font.Font(None, FONT_SIZE_SMALL)
        FONT_MEDIUM = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        FONT_LARGE = pygame.font.Font(None, FONT_SIZE_LARGE)
        FONT_XLARGE = pygame.font.Font(None, FONT_SIZE_XLARGE)
else:
    FONT_SMALL = pygame.font.Font(None, FONT_SIZE_SMALL)
    FONT_MEDIUM = pygame.font.Font(None, FONT_SIZE_MEDIUM)
    FONT_LARGE = pygame.font.Font(None, FONT_SIZE_LARGE)
    FONT_XLARGE = pygame.font.Font(None, FONT_SIZE_XLARGE)

MAX_HINTS = 3