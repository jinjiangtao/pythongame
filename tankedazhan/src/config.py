import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRID_SIZE = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GREEN_GRASS = (34, 139, 34)

PLAYER_SPEED = 3
ENEMY_SPEED = 2
BULLET_SPEED = 6

PLAYER_HEALTH = 3

ENEMY_COUNT_PER_LEVEL = [3, 4, 5, 6, 7]

DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3

BRICK = 1
STEEL = 2
GRASS = 3
BASE = 4
EMPTY = 0

pygame.font.init()

FONT = None

import os

windows_font_paths = [
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/simkai.ttf",
    "C:/Windows/Fonts/simsong.ttf",
    "C:/Windows/Fonts/kaiu.ttf",
    "C:/Windows/Fonts/kaiti.ttf"
]

local_font_paths = [
    "simhei.ttf",
    "simsun.ttc",
    "msyh.ttc",
    "msyhbd.ttc",
    "simkai.ttf",
    "simsong.ttf"
]

for font_path in local_font_paths:
    if os.path.exists(font_path):
        try:
            FONT = pygame.font.Font(font_path, 24)
            break
        except:
            continue

if FONT is None:
    for font_path in windows_font_paths:
        if os.path.exists(font_path):
            try:
                FONT = pygame.font.Font(font_path, 24)
                break
            except:
                continue

if FONT is None:
    try:
        FONT = pygame.font.SysFont("Arial", 24)
    except:
        FONT = pygame.font.Font(None, 24)