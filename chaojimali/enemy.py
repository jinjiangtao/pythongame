import pygame
from settings import GREEN, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED

class Enemy:
    def __init__(self, x, y, move_range=100):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = ENEMY_SPEED
        self.direction = 1
        self.start_x = x
        self.move_range = move_range
        self.alive = True
    
    def update(self):
        if not self.alive:
            return
        
        self.x += self.speed * self.direction
        self.rect.x = self.x
        
        if self.x > self.start_x + self.move_range or self.x < self.start_x:
            self.direction *= -1
    
    def draw(self, screen, camera_x):
        if self.alive:
            pygame.draw.rect(screen, GREEN, (self.x - camera_x, self.y, self.width, self.height))
    
    def die(self):
        self.alive = False