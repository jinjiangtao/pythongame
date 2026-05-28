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
        self.has_double_jumped = False
        self.is_invincible = False
        self.invincible_timer = 0
        self.blink_timer = 0
        self.visible = True
    
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_FORCE
            self.is_jumping = True
            self.has_double_jumped = False
        elif self.is_jumping and not self.has_double_jumped:
            self.velocity_y = SECOND_JUMP_FORCE
            self.has_double_jumped = True
    
    def set_invincible(self, duration):
        self.is_invincible = True
        self.invincible_timer = duration
        self.blink_timer = 0
        self.visible = True
    
    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.velocity_y = 0
            self.is_jumping = False
            self.has_double_jumped = False
        
        if self.is_invincible:
            self.invincible_timer -= 16
            self.blink_timer += 16
            if self.blink_timer >= 100:
                self.visible = not self.visible
                self.blink_timer = 0
            if self.invincible_timer <= 0:
                self.is_invincible = False
                self.visible = True
    
    def draw(self, screen):
        if not self.visible:
            return
        
        body_color = BLUE if not self.is_invincible else CYAN
        window_color = WHITE
        wheel_color = BLACK
        
        pygame.draw.rect(screen, body_color, (self.x, self.y + 10, self.width, self.height - 15))
        
        pygame.draw.rect(screen, window_color, (self.x + 15, self.y + 15, 20, 12))
        
        pygame.draw.circle(screen, wheel_color, (self.x + 10, self.y + self.height), 8)
        pygame.draw.circle(screen, wheel_color, (self.x + 40, self.y + self.height), 8)
        
        pygame.draw.circle(screen, GRAY, (self.x + 10, self.y + self.height), 4)
        pygame.draw.circle(screen, GRAY, (self.x + 40, self.y + self.height), 4)
        
        if self.is_invincible:
            pygame.draw.circle(screen, YELLOW, (self.x + self.width // 2, self.y + 5), 5)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_mask(self):
        mask = pygame.mask.Mask((self.width, self.height), False)
        for y in range(self.height):
            for x in range(self.width):
                if y >= 10 and y < self.height - 5:
                    if not (x >= 15 and x < 35 and y >= 15 and y < 27):
                        mask.set_at((x, y), True)
                elif y >= self.height - 8 and y < self.height:
                    if x >= 2 and x <= 18:
                        mask.set_at((x, y), True)
                    elif x >= 32 and x <= 48:
                        mask.set_at((x, y), True)
        return mask