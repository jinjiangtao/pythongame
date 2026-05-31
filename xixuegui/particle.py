import pygame
import math
from settings import (
    EXPERIENCE_RADIUS,
    EXPERIENCE_COLOR,
    EXPERIENCE_VALUE,
    HIT_PARTICLE_LIFETIME
)


class ExperienceOrb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = EXPERIENCE_RADIUS
        self.color = EXPERIENCE_COLOR
        self.value = EXPERIENCE_VALUE
        self.alive = True

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist < player.pickup_range and dist > 0:
            speed = 8
            self.x += (dx / dist) * speed
            self.y += (dy / dist) * speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


class HitParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = HIT_PARTICLE_LIFETIME
        self.spawn_time = pygame.time.get_ticks()
        self.alive = True
        self.radius = 5

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > self.lifetime:
            self.alive = False

    def draw(self, surface):
        now = pygame.time.get_ticks()
        alpha = 255 - int(((now - self.spawn_time) / self.lifetime) * 255)
        color = (255, 255, 255)
        s = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*color, alpha), (self.radius * 2, self.radius * 2), self.radius)
        surface.blit(s, (self.x - self.radius * 2, self.y - self.radius * 2))
