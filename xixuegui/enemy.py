import pygame
import math
import random
from settings import (
    ENEMY_BASE_RADIUS,
    ENEMY_BASE_SPEED,
    ENEMY_BASE_HP,
    ENEMY_COLOR,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


class Enemy:
    def __init__(self, difficulty_multiplier=1.0):
        side = random.randint(0, 3)
        if side == 0:
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = -50
        elif side == 1:
            self.x = SCREEN_WIDTH + 50
            self.y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = SCREEN_HEIGHT + 50
        else:
            self.x = -50
            self.y = random.randint(0, SCREEN_HEIGHT)

        self.radius = int(ENEMY_BASE_RADIUS * (1 + (difficulty_multiplier - 1) * 0.2))
        self.speed = ENEMY_BASE_SPEED * (1 + (difficulty_multiplier - 1) * 0.15)
        self.max_hp = int(ENEMY_BASE_HP * difficulty_multiplier)
        self.hp = self.max_hp
        self.color = ENEMY_COLOR
        self.alive = True

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        if self.hp < self.max_hp:
            bar_width = self.radius * 2
            bar_height = 5
            bar_x = self.x - bar_width / 2
            bar_y = self.y - self.radius - 10
            fill = (self.hp / self.max_hp) * bar_width
            pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, fill, bar_height))
