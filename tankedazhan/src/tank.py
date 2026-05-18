import random
import pygame
from src.config import *
from src.bullet import Bullet

class Tank:
    def __init__(self, x, y, direction, is_player=False):
        self.x = x
        self.y = y
        self.direction = direction
        self.is_player = is_player
        self.speed = PLAYER_SPEED if is_player else ENEMY_SPEED
        self.width = GRID_SIZE - 4
        self.height = GRID_SIZE - 4
        self.health = PLAYER_HEALTH if is_player else 1
        self.max_health = self.health
        self.last_shot_time = 0
        self.shot_cooldown = 500 if is_player else 1000
        
        self.ai_change_direction_time = 0
        self.ai_change_direction_interval = 1000 + random.randint(0, 1000)
        self.ai_shot_chance = 0.02
    
    def update(self, keys=None, current_time=0):
        if self.is_player and keys:
            self.handle_player_input(keys)
        else:
            self.update_ai(current_time)
    
    def handle_player_input(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction = DIR_UP
            self.y -= self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction = DIR_DOWN
            self.y += self.speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = DIR_LEFT
            self.x -= self.speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = DIR_RIGHT
            self.x += self.speed
        
        self.clamp_position()
    
    def update_ai(self, current_time):
        if current_time - self.ai_change_direction_time > self.ai_change_direction_interval:
            self.direction = random.randint(0, 3)
            self.ai_change_direction_time = current_time
            self.ai_change_direction_interval = 1000 + random.randint(0, 1000)
        
        if self.direction == DIR_UP:
            self.y -= self.speed
        elif self.direction == DIR_DOWN:
            self.y += self.speed
        elif self.direction == DIR_LEFT:
            self.x -= self.speed
        elif self.direction == DIR_RIGHT:
            self.x += self.speed
        
        self.clamp_position()
    
    def clamp_position(self):
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
    
    def shoot(self, current_time):
        if current_time - self.last_shot_time > self.shot_cooldown:
            self.last_shot_time = current_time
            bullet_x = self.x + self.width // 2 - 4
            bullet_y = self.y + self.height // 2 - 4
            return Bullet(bullet_x, bullet_y, self.direction, self.is_player)
        return None
    
    def ai_should_shoot(self):
        return random.random() < self.ai_shot_chance
    
    def take_damage(self, damage=1):
        self.health -= damage
        return self.health <= 0
    
    def draw(self, screen):
        if self.is_player:
            color = BLUE
        else:
            color = GRAY
        
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        pygame.draw.rect(screen, color, 
                        (self.x, self.y, self.width, self.height))
        
        gun_length = 15
        gun_width = 6
        
        if self.direction == DIR_UP:
            pygame.draw.rect(screen, color,
                            (center_x - gun_width // 2, self.y - gun_length + 5,
                             gun_width, gun_length))
        elif self.direction == DIR_DOWN:
            pygame.draw.rect(screen, color,
                            (center_x - gun_width // 2, self.y + self.height - 5,
                             gun_width, gun_length))
        elif self.direction == DIR_LEFT:
            pygame.draw.rect(screen, color,
                            (self.x - gun_length + 5, center_y - gun_width // 2,
                             gun_length, gun_width))
        elif self.direction == DIR_RIGHT:
            pygame.draw.rect(screen, color,
                            (self.x + self.width - 5, center_y - gun_width // 2,
                             gun_length, gun_width))
        
        if self.is_player and self.health > 0:
            health_bar_width = self.width
            health_bar_height = 4
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, RED, 
                            (self.x, self.y - 10, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, GREEN, 
                            (self.x, self.y - 10, health_bar_width * health_ratio, health_bar_height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)