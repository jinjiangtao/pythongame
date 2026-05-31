import pygame
import math
from settings import (
    WEAPON_DAMAGE,
    WEAPON_ATTACK_INTERVAL,
    WEAPON_ATTACK_RANGE
)


class Weapon:
    def __init__(self):
        self.damage = WEAPON_DAMAGE
        self.attack_interval = WEAPON_ATTACK_INTERVAL
        self.attack_range = WEAPON_ATTACK_RANGE
        self.last_attack_time = 0

    def attack(self, player, enemies, hit_particles):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time < self.attack_interval:
            return

        self.last_attack_time = now
        hit_enemies = []
        for enemy in enemies:
            dx = enemy.x - player.x
            dy = enemy.y - player.y
            dist = math.hypot(dx, dy)
            if dist <= self.attack_range:
                hit_enemies.append(enemy)
        return hit_enemies
