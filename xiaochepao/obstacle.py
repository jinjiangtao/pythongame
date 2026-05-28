import pygame
import random
from constants import *

class Obstacle:
    def __init__(self):
        self.width = OBSTACLE_WIDTH
        self.height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
        self.x = SCREEN_WIDTH
        self.y = GROUND_Y - self.height
    
    def update(self):
        self.x -= OBSTACLE_SPEED
    
    def draw(self, screen):
        body_color = RED
        detail_color = ORANGE
        
        pygame.draw.rect(screen, body_color, (self.x, self.y, self.width, self.height))
        
        pygame.draw.rect(screen, detail_color, (self.x + 5, self.y + 10, self.width - 10, 8))
        pygame.draw.rect(screen, detail_color, (self.x + 5, self.y + self.height - 20, self.width - 10, 8))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.x + self.width < 0