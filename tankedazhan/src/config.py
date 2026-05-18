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
FONT = pygame.font.Font("simhei.ttf", 24)
if not FONT:
    FONT = pygame.font.Font(None, 24)