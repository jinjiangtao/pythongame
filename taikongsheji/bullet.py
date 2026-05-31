import pygame
from settings import *

class Bullet:
    def __init__(self, x, y, is_player_bullet=True):
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = x - self.width // 2
        self.y = y
        self.speed = PLAYER_BULLET_SPEED if is_player_bullet else ALIEN_BULLET_SPEED
        self.color = BULLET_COLOR if is_player_bullet else ALIEN_BULLET_COLOR
        self.is_player_bullet = is_player_bullet

    def update(self):
        if self.is_player_bullet:
            self.y -= self.speed
        else:
            self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.y < 0 or self.y > SCREEN_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
