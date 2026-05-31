import pygame
from settings import (
    RED, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED,
    PLAYER_JUMP_FORCE, GRAVITY, SCREEN_HEIGHT
)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = False
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        
        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = PLAYER_JUMP_FORCE
            self.is_jumping = True
            self.on_ground = False
    
    def update(self, platforms):
        self.velocity_y += GRAVITY
        
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.on_ground = False
        
        if self.y >= SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity_y = 0
            self.is_jumping = False
            self.on_ground = True
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0 and self.y + self.height <= platform.y + 30:
                    self.y = platform.y - self.height
                    self.velocity_y = 0
                    self.is_jumping = False
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.y = platform.y + platform.height
                    self.velocity_y = 0
                elif self.velocity_x > 0:
                    self.x = platform.x - self.width
                elif self.velocity_x < 0:
                    self.x = platform.x + platform.width
    
    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, RED, (self.x - camera_x, self.y, self.width, self.height))