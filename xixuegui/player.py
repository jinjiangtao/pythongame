import pygame
import math
from settings import (
    PLAYER_RADIUS,
    PLAYER_SPEED,
    PLAYER_MAX_HP,
    PLAYER_COLOR,
    EXPERIENCE_PICKUP_RANGE
)


class Player:
    def __init__(self):
        self.x = 500
        self.y = 400
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.color = PLAYER_COLOR
        self.pickup_range = EXPERIENCE_PICKUP_RANGE
        self.exp = 0
        self.level = 1
        self.exp_to_next_level = 100
        self.alive = True

    def update(self, keys, screen_width, screen_height):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

        if self.x - self.radius < 0:
            self.x = self.radius
        if self.x + self.radius > screen_width:
            self.x = screen_width - self.radius
        if self.y - self.radius < 0:
            self.y = self.radius
        if self.y + self.radius > screen_height:
            self.y = screen_height - self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
