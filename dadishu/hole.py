import pygame
from constants import *

class Hole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = HOLE_WIDTH // 2
        self.center_x = x + self.radius
        self.center_y = y + HOLE_HEIGHT // 2
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, DARK_BROWN, 
                          (self.x, self.y, HOLE_WIDTH, HOLE_HEIGHT), 0)
        pygame.draw.ellipse(screen, BLACK, 
                          (self.x + 10, self.y + 10, HOLE_WIDTH - 20, HOLE_HEIGHT - 20), 0)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, HOLE_WIDTH, HOLE_HEIGHT)
    
    def get_center(self):
        return (self.center_x, self.center_y)