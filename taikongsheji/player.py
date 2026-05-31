import pygame
from settings import *

class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_LIVES

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x, self.y, self.width, self.height))
        pygame.draw.polygon(screen, PLAYER_COLOR, [
            (self.x + self.width // 2, self.y - 10),
            (self.x + 10, self.y),
            (self.x + self.width - 10, self.y)
        ])

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def reset(self):
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.lives = PLAYER_LIVES

    def hit(self):
        self.lives -= 1
        return self.lives <= 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
