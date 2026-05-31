import pygame
from settings import BROWN

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, BROWN, (self.x - camera_x, self.y, self.width, self.height))