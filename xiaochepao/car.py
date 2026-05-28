import pygame
from constants import *

class Car:
    def __init__(self):
        self.x = 100
        self.y = GROUND_Y - CAR_HEIGHT
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False
    
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_FORCE
            self.is_jumping = True
    
    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.velocity_y = 0
            self.is_jumping = False
    
    def draw(self, screen):
        body_color = BLUE
        window_color = WHITE
        wheel_color = BLACK
        
        pygame.draw.rect(screen, body_color, (self.x, self.y + 10, self.width, self.height - 15))
        
        pygame.draw.rect(screen, window_color, (self.x + 15, self.y + 15, 20, 12))
        
        pygame.draw.circle(screen, wheel_color, (self.x + 10, self.y + self.height), 8)
        pygame.draw.circle(screen, wheel_color, (self.x + 40, self.y + self.height), 8)
        
        pygame.draw.circle(screen, GRAY, (self.x + 10, self.y + self.height), 4)
        pygame.draw.circle(screen, GRAY, (self.x + 40, self.y + self.height), 4)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)