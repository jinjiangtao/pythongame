import pygame
from src.config import BULLET_TYPES, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_COLORS

class Bullet:
    def __init__(self, x, y, direction, bullet_type='player_single'):
        self.x = x
        self.y = y
        self.direction = direction
        self.type = bullet_type
        self.config = BULLET_TYPES[bullet_type]
        self.size = self.config['size']
        self.speed = self.config['speed']
        self.damage = self.config['damage']
        self.active = True
        
    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        if (self.x < -self.size or 
            self.x > SCREEN_WIDTH + self.size or 
            self.y < -self.size or 
            self.y > SCREEN_HEIGHT + self.size):
            self.active = False
            
    def draw(self, screen):
        if self.type.startswith('player'):
            color = GAME_COLORS['player_bullet']
        elif self.type.startswith('boss'):
            color = GAME_COLORS['boss_attack']
        else:
            color = GAME_COLORS['enemy_normal']
            
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)
    
    def is_active(self):
        return self.active
    
    def get_damage(self):
        return self.damage
    
    def deactivate(self):
        self.active = False

class BulletManager:
    def __init__(self):
        self.bullets = []
        
    def add_bullet(self, x, y, direction, bullet_type='player_single'):
        bullet = Bullet(x, y, direction, bullet_type)
        self.bullets.append(bullet)
        
    def add_player_bullets(self, x, y, power_level=1):
        if power_level == 1:
            self.add_bullet(x, y - 25, (0, -1), 'player_single')
        elif power_level == 2:
            self.add_bullet(x - 10, y - 20, (-0.3, -1), 'player_double')
            self.add_bullet(x + 10, y - 20, (0.3, -1), 'player_double')
        elif power_level >= 3:
            self.add_bullet(x, y - 25, (0, -1), 'player_triple')
            self.add_bullet(x - 15, y - 20, (-0.5, -1), 'player_triple')
            self.add_bullet(x + 15, y - 20, (0.5, -1), 'player_triple')
            
    def add_enemy_bullet(self, x, y, enemy_type):
        if enemy_type == 'normal':
            self.add_bullet(x, y + 20, (0, 1), 'enemy_normal')
        elif enemy_type == 'fast':
            self.add_bullet(x, y + 18, (0, 1), 'enemy_fast')
        elif enemy_type == 'heavy':
            self.add_bullet(x, y + 30, (0, 1), 'enemy_heavy')
            
    def add_boss_bullets(self, x, y, pattern='normal'):
        if pattern == 'normal':
            self.add_bullet(x, y + 60, (0, 1), 'boss_bullet')
        elif pattern == 'fan':
            for i in range(-3, 4):
                angle = i * 0.2
                dx = pygame.math.Vector2(0, 1).rotate_rad(angle)
                self.add_bullet(x, y + 60, (dx.x, dx.y), 'boss_fan')
        elif pattern == 'spread':
            for i in range(5):
                angle = (i - 2) * 0.3
                dx = pygame.math.Vector2(0, 1).rotate_rad(angle)
                self.add_bullet(x, y + 60, (dx.x, dx.y), 'boss_spread')
        elif pattern == 'spiral':
            pass
            
    def update(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active():
                self.bullets.remove(bullet)
                
    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
            
    def get_bullets(self):
        return self.bullets
    
    def clear_all(self):
        self.bullets = []
        
    def get_active_count(self):
        return len(self.bullets)