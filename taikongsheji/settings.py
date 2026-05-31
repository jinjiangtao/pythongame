import pygame
import random
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

PLAYER_COLOR = GREEN
ALIEN_COLORS = [RED, BLUE, YELLOW]
BULLET_COLOR = WHITE
ALIEN_BULLET_COLOR = RED

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_SPEED = 7

ALIEN_WIDTH = 40
ALIEN_HEIGHT = 30
ALIEN_SPEED = 2
ALIEN_DROP_SPEED = 20
ALIEN_HORIZONTAL_SPACE = 60
ALIEN_VERTICAL_SPACE = 50
ALIENS_PER_ROW = 8
ALIEN_ROWS = 3

BULLET_WIDTH = 5
BULLET_HEIGHT = 15
PLAYER_BULLET_SPEED = 10
ALIEN_BULLET_SPEED = 5
ALIEN_SHOOT_CHANCE = 0.005

PLAYER_LIVES = 3
ALIEN_POINTS = 10

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("太空侵略者")

def get_chinese_font(font_size):
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/kaiu.ttf",
        "C:/Windows/Fonts/fangsong.ttf",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, font_size)
            except:
                continue
    
    sys_fonts = pygame.font.get_fonts()
    chinese_fonts = ["msyh", "simhei", "simsun", "kaiu", "fangsong", 
                     "microsoftyahei", "microsoft_yahei"]
    
    for font_name in chinese_fonts:
        if font_name.lower() in [f.lower() for f in sys_fonts]:
            try:
                return pygame.font.SysFont(font_name, font_size)
            except:
                continue
    
    return pygame.font.Font(None, font_size)

font = get_chinese_font(74)
small_font = get_chinese_font(36)

clock = pygame.time.Clock()