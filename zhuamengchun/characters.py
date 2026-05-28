import pygame
import random
import math
from config import *

class Pet:
    def __init__(self, x, y, special_type=None, level=1):
        self.x = x
        self.y = y
        self.size = PET_SIZE
        self.type = random.choice(['cat', 'dog', 'rabbit', 'bear', 'penguin'])
        self.special_type = special_type
        self.level = level
        
        self.speed_mult = 1 + (level - 1) * DIFFICULTY_SPEED_MULTIPLIER
        self.speed_x = (random.random() - 0.5) * 2 * self.speed_mult
        self.speed_y = (random.random() - 0.5) * 2 * self.speed_mult
        self.appear_time = pygame.time.get_ticks()
        
        stay_time_range = max(PET_STAY_TIME_MIN - (level - 1) * DIFFICULTY_STAY_TIME_DECREASE, 800)
        self.stay_duration = random.randint(stay_time_range, PET_STAY_TIME_MAX - (level - 1) * DIFFICULTY_STAY_TIME_DECREASE)
        
        self.is_moving = random.choice([True, False])
        self.target_x = x
        self.target_y = y
        self.move_interval = 0
        self.catched = False
        self.caught_animation = 0
        
        self.movement_type = random.choice(['linear', 'curve', 'zigzag'])
        self.move_points = []
        self.current_point_index = 0
        self.curve_angle = 0
        self.zigzag_direction = 1
        
        if self.special_type == 'flash':
            self.points = 30
            self.glow_color = FLASH_PET_COLOR
        elif self.special_type == 'accel':
            self.points = 15
            self.glow_color = ACCEL_PET_COLOR
        elif self.special_type == 'trick':
            self.points = -20
            self.glow_color = TRICK_PET_COLOR
        else:
            self.points = 10
            self.glow_color = None
        
        self.glow_animation = 0
        self.animation_frame = 0
        
        self.colors = {
            'cat': (255, 165, 0),
            'dog': (139, 90, 43),
            'rabbit': (255, 182, 193),
            'bear': (139, 69, 19),
            'penguin': (0, 0, 0)
        }
        
        self.generate_move_points()
    
    def generate_move_points(self):
        if self.movement_type == 'curve':
            self.curve_angle = random.uniform(0, math.pi * 2)
        elif self.movement_type == 'zigzag':
            self.zigzag_direction = random.choice([-1, 1])
    
    def update(self, current_time):
        if self.catched:
            self.caught_animation += 0.15
            if self.caught_animation > 3:
                return False
            return True
        
        if current_time - self.appear_time > self.stay_duration:
            return False
        
        if self.is_moving:
            self.move_pet()
        
        self.glow_animation = (self.glow_animation + 0.1) % (math.pi * 2)
        self.animation_frame = (self.animation_frame + 1) % 60
        
        return True
    
    def move_pet(self):
        self.move_interval += 1
        move_speed = 0.05 * self.speed_mult
        
        if self.movement_type == 'linear':
            if self.move_interval > 60:
                self.move_interval = 0
                self.target_x = self.x + (random.random() - 0.5) * 100
                self.target_y = self.y + (random.random() - 0.5) * 100
                self.target_x = max(self.size, min(GAME_AREA_WIDTH - self.size, self.target_x))
                self.target_y = max(self.size, min(GAME_AREA_HEIGHT - self.size, self.target_y))
            
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            if distance > 1:
                self.x += dx * move_speed
                self.y += dy * move_speed
        
        elif self.movement_type == 'curve':
            self.curve_angle += 0.05 * self.speed_mult
            center_x = self.x + math.cos(self.curve_angle) * 50
            center_y = self.y + math.sin(self.curve_angle) * 50
            self.x += (center_x - self.x) * move_speed
            self.y += (center_y - self.y) * move_speed
            
            self.x = max(self.size, min(GAME_AREA_WIDTH - self.size, self.x))
            self.y = max(self.size, min(GAME_AREA_HEIGHT - self.size, self.y))
        
        elif self.movement_type == 'zigzag':
            if self.move_interval > 20:
                self.move_interval = 0
                self.zigzag_direction *= -1
            
            self.x += self.zigzag_direction * 2 * self.speed_mult
            self.y += 1 * self.speed_mult
            
            if self.x <= self.size or self.x >= GAME_AREA_WIDTH - self.size:
                self.zigzag_direction *= -1
            if self.y <= self.size or self.y >= GAME_AREA_HEIGHT - self.size:
                self.y = max(self.size, min(GAME_AREA_HEIGHT - self.size, self.y))
    
    def draw(self, screen):
        if self.catched:
            self.draw_caught(screen)
        else:
            self.draw_pet(screen)
    
    def draw_pet(self, screen):
        color = self.colors[self.type]
        
        if self.glow_color:
            glow_size = 5 + int(math.sin(self.glow_animation) * 3)
            glow_surface = pygame.Surface((self.size * 2 + glow_size * 2, self.size * 2 + glow_size * 2), pygame.SRCALPHA)
            glow_alpha = int(128 + math.sin(self.glow_animation) * 64)
            pygame.draw.circle(glow_surface, (*self.glow_color, glow_alpha), 
                             (self.size + glow_size, self.size + glow_size), 
                             self.size // 2 + glow_size)
            screen.blit(glow_surface, (self.x - self.size - glow_size, self.y - self.size - glow_size))
        
        if self.type == 'cat':
            ear_points = [
                (self.x, self.y - self.size//2),
                (self.x - self.size//4, self.y - self.size//3),
                (self.x - self.size//2, self.y)
            ]
            pygame.draw.polygon(screen, self.darken_color(color, 0.8), ear_points)
            pygame.draw.polygon(screen, color, 
                               [(p[0] + 2, p[1] + 2) for p in ear_points], 2)
            
            ear_points2 = [
                (self.x, self.y - self.size//2),
                (self.x + self.size//4, self.y - self.size//3),
                (self.x + self.size//2, self.y)
            ]
            pygame.draw.polygon(screen, self.darken_color(color, 0.8), ear_points2)
            pygame.draw.polygon(screen, color, 
                               [(p[0] - 2, p[1] + 2) for p in ear_points2], 2)
            
            body_rect = pygame.Rect(self.x - self.size//2, self.y - self.size//4, self.size, self.size//2)
            pygame.draw.ellipse(screen, self.darken_color(color, 0.8), body_rect)
            pygame.draw.ellipse(screen, color, 
                (self.x - self.size//2 + 2, self.y - self.size//4 + 2, self.size - 4, self.size//2 - 4), 2)
            
            pygame.draw.circle(screen, color, (self.x, self.y + self.size//4), self.size//3)
            pygame.draw.circle(screen, color, (self.x, self.y + self.size//4), self.size//3, 2)
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y), 5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y), 5)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y), 2)
        
        elif self.type == 'dog':
            pygame.draw.ellipse(screen, self.darken_color(color, 0.8), 
                (self.x - self.size//2, self.y - self.size//3, self.size, self.size//2))
            pygame.draw.ellipse(screen, color, 
                (self.x - self.size//2 + 2, self.y - self.size//3 + 2, self.size - 4, self.size//2 - 4), 2)
            
            pygame.draw.circle(screen, color, (self.x, self.y + self.size//4), self.size//3)
            pygame.draw.circle(screen, color, (self.x, self.y + self.size//4), self.size//3, 2)
            pygame.draw.circle(screen, color, (self.x - self.size//3, self.y - self.size//2), self.size//5)
            pygame.draw.circle(screen, color, (self.x + self.size//3, self.y - self.size//2), self.size//5)
            pygame.draw.ellipse(screen, (255, 255, 255), 
                (self.x - self.size//3, self.y - self.size//6, self.size//4, self.size//4))
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y), 5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y), 5)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y), 2)
        
        elif self.type == 'rabbit':
            ear_rect1 = pygame.Rect(self.x - self.size//5, self.y - self.size//2, self.size//5, self.size//2)
            pygame.draw.ellipse(screen, self.darken_color(color, 0.8), ear_rect1)
            pygame.draw.ellipse(screen, color, 
                (self.x - self.size//5 + 1, self.y - self.size//2 + 1, self.size//5 - 2, self.size//2 - 2), 2)
            
            ear_rect2 = pygame.Rect(self.x + self.size//10, self.y - self.size//2, self.size//5, self.size//2)
            pygame.draw.ellipse(screen, self.darken_color(color, 0.8), ear_rect2)
            pygame.draw.ellipse(screen, color, 
                (self.x + self.size//10 + 1, self.y - self.size//2 + 1, self.size//5 - 2, self.size//2 - 2), 2)
            
            pygame.draw.circle(screen, color, (self.x, self.y), self.size//3)
            pygame.draw.circle(screen, color, (self.x, self.y), self.size//3, 2)
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y - self.size//8), 4)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y - self.size//8), 4)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y - self.size//8), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y - self.size//8), 2)
            pygame.draw.line(screen, (255, 182, 193), (self.x - self.size//4, self.y + self.size//6), (self.x - self.size//3, self.y + self.size//3), 2)
            pygame.draw.line(screen, (255, 182, 193), (self.x + self.size//4, self.y + self.size//6), (self.x + self.size//3, self.y + self.size//3), 2)
        
        elif self.type == 'bear':
            pygame.draw.circle(screen, color, (self.x - self.size//3, self.y - self.size//3), self.size//4)
            pygame.draw.circle(screen, color, (self.x - self.size//3, self.y - self.size//3), self.size//4, 2)
            pygame.draw.circle(screen, color, (self.x + self.size//3, self.y - self.size//3), self.size//4)
            pygame.draw.circle(screen, color, (self.x + self.size//3, self.y - self.size//3), self.size//4, 2)
            pygame.draw.circle(screen, color, (self.x, self.y), self.size//2.5)
            pygame.draw.circle(screen, color, (self.x, self.y), self.size//2.5, 2)
            pygame.draw.circle(screen, (255, 215, 0), (self.x, self.y), self.size//5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y - self.size//8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y - self.size//8), 5)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y - self.size//8), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y - self.size//8), 2)
        
        elif self.type == 'penguin':
            pygame.draw.ellipse(screen, color, 
                (self.x - self.size//3, self.y - self.size//4, self.size*2//3, self.size//2))
            pygame.draw.ellipse(screen, color, 
                (self.x - self.size//3 + 2, self.y - self.size//4 + 2, self.size*2//3 - 4, self.size//2 - 4), 2)
            pygame.draw.circle(screen, color, (self.x, self.y + self.size//4), self.size//3)
            pygame.draw.circle(screen, color, (self.x, self.y + self.size//4), self.size//3, 2)
            pygame.draw.ellipse(screen, (255, 255, 255), 
                (self.x - self.size//3, self.y - self.size//6, self.size*2//3, self.size//3))
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y), 5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y), 5)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y), 2)
            pygame.draw.line(screen, color, (self.x - self.size//2, self.y), (self.x - self.size//1.5, self.y - self.size//4), 3)
            pygame.draw.line(screen, color, (self.x + self.size//2, self.y), (self.x + self.size//1.5, self.y - self.size//4), 3)
        
        if self.special_type:
            font = self.get_chinese_font(14)
            if self.special_type == 'flash':
                label = '×3'
                label_color = FLASH_PET_COLOR
            elif self.special_type == 'accel':
                label = '⚡'
                label_color = ACCEL_PET_COLOR
            elif self.special_type == 'trick':
                label = '!'
                label_color = TRICK_PET_COLOR
            else:
                label = ''
                label_color = WHITE
            
            if label:
                text = font.render(label, True, label_color)
                text_rect = text.get_rect(center=(self.x, self.y - self.size//2 - 10))
                screen.blit(text, text_rect)
    
    def darken_color(self, color, factor):
        return tuple(max(0, int(c * factor)) for c in color)
    
    def get_chinese_font(self, size):
        font_paths = [
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/msyh.ttc',
            'C:/Windows/Fonts/simsun.ttc',
        ]
        for path in font_paths:
            try:
                return pygame.font.Font(path, size)
            except:
                continue
        return pygame.font.Font(None, size)
    
    def draw_caught(self, screen):
        alpha = int(255 * (1 - self.caught_animation / 3))
        if self.points > 0:
            color = SUCCESS_COLOR if self.points >= 10 else GOLD_COLOR
        else:
            color = FAILURE_COLOR
        
        pygame.draw.circle(screen, color + (alpha,), (self.x, self.y), int(self.size * (1 + self.caught_animation)), 3)
        
        font = self.get_chinese_font(32)
        if self.points > 0:
            text = font.render(f'+{self.points}', True, color)
        else:
            text = font.render(str(self.points), True, color)
        text_rect = text.get_rect(center=(self.x, self.y - self.size))
        screen.blit(text, text_rect)
    
    def check_click(self, mouse_x, mouse_y):
        distance = ((mouse_x - self.x)**2 + (mouse_y - self.y)**2)**0.5
        return distance < self.size//2


class Prop:
    def __init__(self, x, y, prop_type):
        self.x = x
        self.y = y
        self.prop_type = prop_type
        self.size = 40
        self.appear_time = pygame.time.get_ticks()
        self.duration = 5000
        self.catched = False
        self.caught_animation = 0
        self.rotation = 0
        
        self.colors = {
            'time': (255, 165, 0),
            'catch_all': (0, 255, 255),
            'score': (255, 215, 0)
        }
    
    def update(self, current_time):
        if self.catched:
            self.caught_animation += 0.15
            if self.caught_animation > 3:
                return False
            return True
        
        if current_time - self.appear_time > self.duration:
            return False
        
        self.rotation = (self.rotation + 2) % 360
        return True
    
    def draw(self, screen):
        if self.catched:
            self.draw_caught(screen)
        else:
            self.draw_prop(screen)
    
    def draw_prop(self, screen):
        color = self.colors.get(self.prop_type, WHITE)
        
        glow_size = 8 + int(math.sin(pygame.time.get_ticks() * 0.005) * 3)
        glow_surface = pygame.Surface((self.size * 2 + glow_size * 2, self.size * 2 + glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*color, 100), 
                         (self.size + glow_size, self.size + glow_size), 
                         self.size // 2 + glow_size)
        screen.blit(glow_surface, (self.x - self.size - glow_size, self.y - self.size - glow_size))
        
        rotated_surface = pygame.transform.rotate(
            pygame.Surface((self.size, self.size), pygame.SRCALPHA), 
            self.rotation
        )
        
        pygame.draw.circle(screen, color, (self.x, self.y), self.size // 2)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size // 2, 2)
        
        font = self.get_chinese_font(16)
        if self.prop_type == 'time':
            label = '+时'
        elif self.prop_type == 'catch_all':
            label = '全'
        elif self.prop_type == 'score':
            label = '倍'
        else:
            label = '?'
        
        text = font.render(label, True, WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
    
    def get_chinese_font(self, size):
        font_paths = [
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/msyh.ttc',
            'C:/Windows/Fonts/simsun.ttc',
        ]
        for path in font_paths:
            try:
                return pygame.font.Font(path, size)
            except:
                continue
        return pygame.font.Font(None, size)
    
    def draw_caught(self, screen):
        alpha = int(255 * (1 - self.caught_animation / 3))
        color = self.colors.get(self.prop_type, WHITE)
        pygame.draw.circle(screen, color + (alpha,), (self.x, self.y), int(self.size * (1 + self.caught_animation)), 3)
    
    def check_click(self, mouse_x, mouse_y):
        distance = ((mouse_x - self.x)**2 + (mouse_y - self.y)**2)**0.5
        return distance < self.size // 2


class Effect:
    def __init__(self, x, y, effect_type):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.frame = 0
        self.max_frames = 30
        
        if effect_type == 'success':
            self.color = GOLD_COLOR
        elif effect_type == 'failure':
            self.color = SHOCK_COLOR
        else:
            self.color = WHITE
    
    def update(self):
        self.frame += 1
        return self.frame < self.max_frames
    
    def draw(self, screen):
        progress = self.frame / self.max_frames
        
        if self.effect_type == 'success':
            radius = int(20 + progress * 60)
            alpha = int(255 * (1 - progress))
            pygame.draw.circle(screen, self.color + (alpha,), (self.x, self.y), radius, 3)
            
            for i in range(8):
                angle = (i / 8) * math.pi * 2 + progress * math.pi
                end_x = self.x + math.cos(angle) * (30 + progress * 50)
                end_y = self.y + math.sin(angle) * (30 + progress * 50)
                pygame.draw.line(screen, self.color + (alpha,), (self.x, self.y), (end_x, end_y), 2)
        
        elif self.effect_type == 'failure':
            offset = int(math.sin(progress * math.pi * 4) * 10 * (1 - progress))
            pygame.draw.circle(screen, self.color, (self.x + offset, self.y), 15, 3)
            
            shake_text = self.get_chinese_font(20).render('未命中', True, self.color)
            screen.blit(shake_text, (self.x - 30 + offset, self.y - 50))
    
    def get_chinese_font(self, size):
        font_paths = [
            'C:/Windows/Fonts/simhei.ttf',
            'C:/Windows/Fonts/msyh.ttc',
            'C:/Windows/Fonts/simsun.ttc',
        ]
        for path in font_paths:
            try:
                return pygame.font.Font(path, size)
            except:
                continue
        return pygame.font.Font(None, size)
