import pygame
import random
import settings

class CloudPlatform:
    def __init__(self, x, y, width, moving=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = settings.PLATFORM_HEIGHT
        self.moving = moving
        self.move_direction = 1 if random.random() > 0.5 else -1
        self.base_x = x
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, scroll_speed):
        self.y += scroll_speed
        
        if self.moving:
            self.x += self.move_direction * 1.5
            if self.x < 0 or self.x + self.width > settings.GAME_WIDTH:
                self.move_direction *= -1
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.ellipse(screen, settings.CLOUD_WHITE, 
                          (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, settings.CLOUD_GRAY, 
                          (self.x + 5, self.y + 5, self.width - 10, self.height - 10), 2)
        pygame.draw.circle(screen, settings.CLOUD_WHITE, (self.x + 15, self.y - 5), 12)
        pygame.draw.circle(screen, settings.CLOUD_WHITE, 
                          (self.x + self.width // 2, self.y - 8), 15)
        pygame.draw.circle(screen, settings.CLOUD_WHITE, 
                          (self.x + self.width - 15, self.y - 5), 12)

    @staticmethod
    def generate_random_platform(level=1):
        width = random.randint(settings.PLATFORM_MIN_WIDTH, 
                              settings.PLATFORM_MAX_WIDTH)
        x = random.randint(10, settings.GAME_WIDTH - width - 10)
        moving = random.random() < (0.3 + level * 0.05)
        return x, width, moving
