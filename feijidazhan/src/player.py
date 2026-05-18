import pygame
from src.config import PLAYER_SIZE, PLAYER_SPEED, PLAYER_INITIAL_HEALTH, PLAYER_MAX_HEALTH, PLAYER_INVINCIBLE_DURATION, PLAYER_FIRE_RATE, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_COLORS

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.health = PLAYER_INITIAL_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.power_level = 1
        self.max_power_level = 3
        self.bomb_count = 1
        self.active = True
        
        self.invincible = False
        self.invincible_end_time = 0
        self.shield_active = False
        self.shield_end_time = 0
        
        self.last_fire_time = 0
        self.keys = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        
    def handle_key_down(self, key):
        if key == pygame.K_w or key == pygame.K_UP:
            self.keys['up'] = True
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.keys['down'] = True
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.keys['left'] = True
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.keys['right'] = True
            
    def handle_key_up(self, key):
        if key == pygame.K_w or key == pygame.K_UP:
            self.keys['up'] = False
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.keys['down'] = False
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.keys['left'] = False
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.keys['right'] = False
            
    def update(self, current_time):
        self.move()
        
        if self.invincible and current_time > self.invincible_end_time:
            self.invincible = False
            
        if self.shield_active and current_time > self.shield_end_time:
            self.shield_active = False
            
    def move(self):
        dx = 0
        dy = 0
        
        if self.keys['up']:
            dy -= self.speed
        if self.keys['down']:
            dy += self.speed
        if self.keys['left']:
            dx -= self.speed
        if self.keys['right']:
            dx += self.speed
            
        self.x += dx
        self.y += dy
        
        self.x = max(self.size // 2, min(self.x, SCREEN_WIDTH - self.size // 2))
        self.y = max(self.size // 2, min(self.y, SCREEN_HEIGHT - self.size // 2))
        
    def fire(self, current_time):
        if current_time - self.last_fire_time > PLAYER_FIRE_RATE:
            self.last_fire_time = current_time
            return True
        return False
    
    def take_damage(self, damage):
        if self.invincible or self.shield_active:
            return False
            
        self.health -= damage
        self.invincible = True
        self.invincible_end_time = pygame.time.get_ticks() + PLAYER_INVINCIBLE_DURATION
        
        if self.health <= 0:
            self.health = 0
            self.active = False
            return True
        return False
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
        
    def power_up(self):
        if self.power_level < self.max_power_level:
            self.power_level += 1
            
    def activate_shield(self, duration):
        self.shield_active = True
        self.shield_end_time = pygame.time.get_ticks() + duration
        
    def add_bomb(self):
        self.bomb_count += 1
        
    def use_bomb(self):
        if self.bomb_count > 0:
            self.bomb_count -= 1
            return True
        return False
    
    def draw(self, screen):
        if self.invincible and int(pygame.time.get_ticks() / 100) % 2 == 0:
            color = (100, 255, 100)
        elif self.shield_active:
            color = (100, 150, 255)
        else:
            color = GAME_COLORS['player']
            
        pygame.draw.polygon(screen, color, [
            (self.x, self.y - self.size // 2),
            (self.x - self.size // 2, self.y + self.size // 2),
            (self.x + self.size // 2, self.y + self.size // 2)
        ])
        
        if self.shield_active:
            pygame.draw.circle(screen, (100, 150, 255), 
                             (int(self.x), int(self.y)), self.size, 2)
            
        if self.health < self.max_health:
            health_bar_width = self.size
            health_bar_height = 4
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, (255, 0, 0), 
                           (self.x - health_bar_width // 2, self.y - self.size // 2 - 10, 
                            health_bar_width, health_bar_height))
            pygame.draw.rect(screen, (0, 255, 0), 
                           (self.x - health_bar_width // 2, self.y - self.size // 2 - 10, 
                            health_bar_width * health_ratio, health_bar_height))
            
    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, 
                          self.size, self.size)
    
    def is_active(self):
        return self.active
    
    def get_health(self):
        return self.health
    
    def get_power_level(self):
        return self.power_level
    
    def get_bomb_count(self):
        return self.bomb_count
    
    def is_invincible(self):
        return self.invincible
    
    def is_shield_active(self):
        return self.shield_active
    
    def get_position(self):
        return (self.x, self.y)