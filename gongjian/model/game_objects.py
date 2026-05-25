import pygame
import random
import math

class Archer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.speed = 8
        self.angle = -45
        self.power = 0
        self.max_power = 100
        self.is_charging = False

    def move_left(self):
        self.x = max(50, self.x - self.speed)

    def move_right(self):
        self.x = min(750, self.x + self.speed)

    def start_charging(self):
        self.is_charging = True
        self.power = 0

    def charge(self):
        if self.is_charging and self.power < self.max_power:
            self.power += 2

    def stop_charging(self):
        self.is_charging = False
        power = self.power
        self.power = 0
        return power

class Arrow:
    def __init__(self, x, y, angle, power):
        self.x = x
        self.y = y
        self.width = 6
        self.height = 20
        self.angle = angle
        self.speed = power * 0.5
        self.vx = self.speed * math.cos(math.radians(angle))
        self.vy = self.speed * math.sin(math.radians(angle))
        self.active = True
        self.gravity = 0.2

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        if self.x < 0 or self.x > 800 or self.y > 600:
            self.active = False

class Target:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.type = random.choice(['normal', 'fast', 'bonus'])
        self.x = self.screen_width + 50
        self.y = random.randint(100, 400)
        self.width = 40
        self.height = 40
        self.speed = 2 + random.random() * 2
        if self.type == 'fast':
            self.speed *= 1.5
        self.active = True

    def update(self):
        self.x -= self.speed
        if self.x < -50:
            self.active = False

    def get_score(self):
        if self.type == 'normal':
            return 10
        elif self.type == 'fast':
            return 20
        elif self.type == 'bonus':
            return 30

class FlyingTarget:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.x = self.screen_width + 50
        self.y = random.randint(80, 250)
        self.width = 30
        self.height = 25
        self.speed = 3 + random.random() * 2
        self.dy = random.choice([-1, 1]) * (0.5 + random.random())
        self.active = True

    def update(self):
        self.x -= self.speed
        self.y += self.dy
        if self.y < 50 or self.y > 300:
            self.dy *= -1
        if self.x < -50:
            self.active = False

    def get_score(self):
        return 25

class PowerUp:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.type = random.choice(['arrow', 'score', 'health'])
        self.x = self.screen_width + 50
        self.y = random.randint(100, 450)
        self.width = 30
        self.height = 30
        self.speed = 1.5
        self.active = True

    def update(self):
        self.x -= self.speed
        if self.x < -50:
            self.active = False

class GameState:
    def __init__(self):
        self.score = 0
        self.arrows = 10
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.paused = False
        self.game_won = False
        self.message = ""
        self.message_time = 0

    def add_score(self, points):
        self.score += points

    def remove_arrow(self):
        self.arrows -= 1
        if self.arrows <= 0:
            self.game_over = True

    def remove_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    def add_arrow(self):
        self.arrows = min(15, self.arrows + 2)

    def add_life(self):
        self.lives = min(5, self.lives + 1)

    def set_message(self, msg):
        self.message = msg
        self.message_time = pygame.time.get_ticks()

    def update_level(self):
        self.level += 1

    def reset(self):
        self.score = 0
        self.arrows = 10
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.paused = False
        self.game_won = False
        self.message = ""
        self.message_time = 0

import math