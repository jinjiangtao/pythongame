import pygame
from settings import GOLD, COIN_SIZE

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = COIN_SIZE
        self.height = COIN_SIZE
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False
        self.bob_offset = 0
        self.bob_direction = 1
    
    def update(self):
        if not self.collected:
            self.bob_offset += 0.1 * self.bob_direction
            if self.bob_offset > 5 or self.bob_offset < -5:
                self.bob_direction *= -1
    
    def draw(self, screen, camera_x):
        if not self.collected:
            pygame.draw.rect(screen, GOLD, (
                self.x - camera_x,
                self.y + self.bob_offset,
                self.width,
                self.height
            ))
    
    def collect(self):
        self.collected = True