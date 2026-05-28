import pygame
import random
import math
from constants import *

class PowerUp:
    TYPES = ["slow", "invincible", "double_score"]
    
    def __init__(self, powerup_type=None):
        self.type = powerup_type if powerup_type else random.choice(PowerUp.TYPES)
        self.width = POWERUP_WIDTH
        self.height = POWERUP_HEIGHT
        self.x = SCREEN_WIDTH
        self.y = GROUND_Y - self.height - random.randint(50, 150)
        self.velocity_y = 0
        self.bob_offset = 0
        self.picked = False
    
    def update(self, speed):
        self.x -= speed
        self.bob_offset = (self.bob_offset + 0.1) % (2 * 3.14159)
        self.y = GROUND_Y - self.height - 80 + int(10 * math.sin(self.bob_offset))
    
    def draw(self, screen):
        colors = {
            "slow": CYAN,
            "invincible": YELLOW,
            "double_score": PINK
        }
        
        icons = {
            "slow": "S",
            "invincible": "★",
            "double_score": "×2"
        }
        
        color = colors[self.type]
        icon = icons[self.type]
        
        pygame.draw.circle(screen, color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2)
        pygame.draw.circle(screen, WHITE, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2 - 3)
        pygame.draw.circle(screen, color, (self.x + self.width // 2, self.y + self.height // 2), self.width // 2 - 6)
        
        font = pygame.font.Font(None, 20)
        text = font.render(icon, True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.x + self.width < 0

class PowerUpManager:
    def __init__(self):
        self.powerups = []
        self.last_spawn_time = 0
        self.spawn_interval = random.randint(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)
    
    def spawn_powerup(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.powerups.append(PowerUp())
            self.last_spawn_time = current_time
            self.spawn_interval = random.randint(POWERUP_SPAWN_INTERVAL_MIN, POWERUP_SPAWN_INTERVAL_MAX)
    
    def update(self, speed):
        for powerup in self.powerups[:]:
            powerup.update(speed)
            if powerup.is_off_screen() or powerup.picked:
                self.powerups.remove(powerup)
    
    def draw(self, screen):
        for powerup in self.powerups:
            powerup.draw(screen)
    
    def get_powerups(self):
        return self.powerups