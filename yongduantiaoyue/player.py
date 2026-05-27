import pygame
import settings

class Player:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.x = settings.GAME_WIDTH // 2 - self.width // 2
        self.y = settings.SCREEN_HEIGHT // 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = settings.PLAYER_SPEED
        self.jump_power = settings.JUMP_POWER
        self.gravity = settings.GRAVITY
        self.on_ground = False
        self.can_double_jump = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys):
        self.velocity_x = 0
        
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            self.can_double_jump = True
        elif keys[pygame.K_SPACE] and self.can_double_jump:
            self.velocity_y = self.jump_power * settings.DOUBLE_JUMP_MULTIPLIER
            self.can_double_jump = False

        self.velocity_y += self.gravity
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x < 0:
            self.x = 0
        if self.x + self.width > settings.GAME_WIDTH:
            self.x = settings.GAME_WIDTH - self.width

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.ellipse(screen, settings.PLAYER_COLOR, 
                          (self.x + 5, self.y + 5, self.width - 10, self.height - 10))
        pygame.draw.ellipse(screen, settings.PLAYER_DARK, 
                          (self.x + 10, self.y + 10, self.width - 20, self.height - 20), 2)
        pygame.draw.circle(screen, settings.BLACK, (self.x + 15, self.y + 15), 4)
        pygame.draw.circle(screen, settings.BLACK, (self.x + 25, self.y + 15), 4)
        pygame.draw.arc(screen, (255, 0, 0), (self.x + 12, self.y + 22, 16, 10), 0.1, 3.0, 2)

    def reset(self):
        self.x = settings.GAME_WIDTH // 2 - self.width // 2
        self.y = settings.SCREEN_HEIGHT // 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.can_double_jump = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
