import pygame
import random
from src.config import ENEMY_TYPES, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_COLORS

class Enemy:
    def __init__(self, x, y, enemy_type='normal'):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.config = ENEMY_TYPES[enemy_type]
        self.size = self.config['size']
        self.speed = self.config['speed']
        self.health = self.config['health']
        self.max_health = self.config['health']
        self.score = self.config['score']
        self.fire_rate = self.config['fire_rate']
        self.bullet_speed = self.config['bullet_speed']
        self.active = True
        self.last_fire_time = 0
        self.move_pattern = 'straight'
        self.move_timer = 0
        self.target_x = x
        
    def update(self, current_time):
        self.move()
        
        if self.type != 'boss' and self.y > SCREEN_HEIGHT + self.size:
            self.active = False
            
        if current_time - self.last_fire_time > self.fire_rate:
            should_fire = self.should_fire()
            self.last_fire_time = current_time
            return should_fire
        return False
    
    def move(self):
        if self.type == 'fast':
            self.fast_move()
        elif self.type == 'heavy':
            self.heavy_move()
        elif self.type == 'boss':
            self.boss_move()
        else:
            self.normal_move()
            
    def normal_move(self):
        self.y += self.speed
        
    def fast_move(self):
        self.move_timer += 1
        if self.move_timer < 60:
            self.y += self.speed * 1.5
            self.x += (self.target_x - self.x) * 0.02
        else:
            self.y += self.speed
            
    def heavy_move(self):
        self.y += self.speed * 0.8
        self.move_timer += 1
        if self.move_timer % 120 < 60:
            self.x += 1
        else:
            self.x -= 1
            self.x = max(self.size // 2, min(self.x, SCREEN_WIDTH - self.size // 2))
            
    def boss_move(self):
        self.move_timer += 1
        if self.move_timer < 120:
            self.y += self.speed
        else:
            if self.move_timer % 200 < 100:
                self.x += 2
            else:
                self.x -= 2
                self.x = max(self.size // 2, min(self.x, SCREEN_WIDTH - self.size // 2))
            
    def should_fire(self):
        if self.type == 'boss':
            return True
        return random.random() < 0.3
    
    def draw(self, screen):
        if self.type == 'normal':
            color = GAME_COLORS['enemy_normal']
        elif self.type == 'fast':
            color = GAME_COLORS['enemy_fast']
        elif self.type == 'heavy':
            color = GAME_COLORS['enemy_heavy']
        else:
            color = GAME_COLORS['boss']
            
        pygame.draw.polygon(screen, color, [
            (self.x, self.y - self.size // 2),
            (self.x - self.size // 2, self.y + self.size // 2),
            (self.x + self.size // 2, self.y + self.size // 2)
        ])
        
        if self.type == 'boss':
            pygame.draw.circle(screen, (255, 100, 100), 
                             (int(self.x), int(self.y)), self.size // 3)
            
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
            
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.active = False
            return True
        return False
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, 
                          self.size, self.size)
    
    def is_active(self):
        return self.active
    
    def get_score(self):
        return self.score
    
    def get_bullet_info(self):
        return {
            'x': self.x,
            'y': self.y + self.size // 2,
            'type': self.type
        }
    
    def is_boss(self):
        return self.type == 'boss'

class EnemyManager:
    def __init__(self):
        self.enemies = []
        
    def add_enemy(self, x, y, enemy_type='normal'):
        enemy = Enemy(x, y, enemy_type)
        self.enemies.append(enemy)
        
    def add_boss(self):
        boss = Enemy(SCREEN_WIDTH // 2, -150, 'boss')
        self.enemies.append(boss)
        
    def update(self, current_time):
        firing_enemies = []
        for enemy in self.enemies[:]:
            should_fire = enemy.update(current_time)
            if should_fire:
                firing_enemies.append(enemy)
            if not enemy.is_active():
                self.enemies.remove(enemy)
        return firing_enemies
    
    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
            
    def get_enemies(self):
        return self.enemies
    
    def clear_all(self):
        self.enemies = []
        
    def get_active_count(self):
        return len(self.enemies)
    
    def has_boss(self):
        return any(enemy.is_boss() for enemy in self.enemies)