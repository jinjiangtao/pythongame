import pygame
import random
from settings import *

class Alien:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = ALIEN_WIDTH
        self.height = ALIEN_HEIGHT
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y + 10), 5)
        pygame.draw.circle(screen, WHITE, (self.x + self.width - 10, self.y + 10), 5)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class AlienFleet:
    def __init__(self, level=1):
        self.aliens = []
        self.direction = 1
        self.base_speed = ALIEN_SPEED + (level - 1) * 0.5
        self.speed = self.base_speed
        self.drop_amount = ALIEN_DROP_SPEED
        self.shoot_chance = ALIEN_SHOOT_CHANCE + (level - 1) * 0.002
        self.level = level
        self.create_fleet()

    def create_fleet(self):
        self.aliens.clear()
        start_x = (SCREEN_WIDTH - (ALIENS_PER_ROW * ALIEN_HORIZONTAL_SPACE)) // 2
        start_y = 60

        for row in range(ALIEN_ROWS):
            color = ALIEN_COLORS[row % len(ALIEN_COLORS)]
            for col in range(ALIENS_PER_ROW):
                x = start_x + col * ALIEN_HORIZONTAL_SPACE
                y = start_y + row * ALIEN_VERTICAL_SPACE
                self.aliens.append(Alien(x, y, color))

    def update(self):
        edge_reached = False
        for alien in self.aliens:
            alien.x += self.speed * self.direction
            if alien.x <= 0 or alien.x >= SCREEN_WIDTH - alien.width:
                edge_reached = True

        if edge_reached:
            self.direction *= -1
            for alien in self.aliens:
                alien.y += self.drop_amount
            self.speed = min(self.base_speed * 1.2, self.speed + 0.3)

    def draw(self):
        for alien in self.aliens:
            alien.draw()

    def check_collision(self, bullet):
        for alien in self.aliens:
            if alien.get_rect().colliderect(bullet.get_rect()):
                return alien
        return None

    def remove_alien(self, alien):
        if alien in self.aliens:
            self.aliens.remove(alien)

    def can_shoot(self):
        return len(self.aliens) > 0 and random.random() < self.shoot_chance

    def get_bottom_y(self):
        if not self.aliens:
            return 0
        return max(alien.y + alien.height for alien in self.aliens)

    def reset(self, level=1):
        self.level = level
        self.base_speed = ALIEN_SPEED + (level - 1) * 0.5
        self.speed = self.base_speed
        self.shoot_chance = ALIEN_SHOOT_CHANCE + (level - 1) * 0.002
        self.direction = 1
        self.create_fleet()

    def is_empty(self):
        return len(self.aliens) == 0
