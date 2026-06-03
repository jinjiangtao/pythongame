# pig.py - 猪头类

import math
import pygame
from settings import PIG_RADIUS, PIG_COLOR

class Pig:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = PIG_RADIUS
        self.alive = True
    
    def draw(self, screen):
        """绘制猪头"""
        if not self.alive:
            return
        
        pygame.draw.circle(screen, PIG_COLOR, (int(self.x), int(self.y)), self.radius)
        
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x) - 8, int(self.y) - 5), 4)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x) + 8, int(self.y) - 5), 4)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x) - 7, int(self.y) - 6), 1)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x) + 9, int(self.y) - 6), 1)
        
        pygame.draw.polygon(screen, (0, 0, 0), [
            (int(self.x) - 3, int(self.y) + 2),
            (int(self.x), int(self.y) + 5),
            (int(self.x) + 3, int(self.y) + 2)
        ])
        
        pygame.draw.arc(screen, (0, 0, 0), 
                        (int(self.x) - 10, int(self.y) + 2, 20, 10), 
                        math.radians(20), math.radians(160), 2)