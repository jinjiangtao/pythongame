import pygame
import random
from config import *

class Pet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PET_SIZE
        self.type = random.choice(['cat', 'dog', 'rabbit', 'bear', 'penguin'])
        self.speed_x = (random.random() - 0.5) * 2
        self.speed_y = (random.random() - 0.5) * 2
        self.appear_time = pygame.time.get_ticks()
        self.stay_duration = random.randint(PET_STAY_TIME_MIN, PET_STAY_TIME_MAX)
        self.is_moving = random.choice([True, False])
        self.target_x = x
        self.target_y = y
        self.move_interval = 0
        self.catched = False
        self.caught_animation = 0
        
        self.colors = {
            'cat': (255, 165, 0),
            'dog': (139, 90, 43),
            'rabbit': (255, 182, 193),
            'bear': (139, 69, 19),
            'penguin': (0, 0, 0)
        }
    
    def update(self, current_time):
        if self.catched:
            self.caught_animation += 0.15
            if self.caught_animation > 3:
                return False
            return True
        
        if current_time - self.appear_time > self.stay_duration:
            return False
        
        if self.is_moving:
            self.move_interval += 1
            if self.move_interval > 60:
                self.move_interval = 0
                self.target_x = self.x + (random.random() - 0.5) * 80
                self.target_y = self.y + (random.random() - 0.5) * 80
                self.target_x = max(self.size, min(GAME_AREA_WIDTH - self.size, self.target_x))
                self.target_y = max(self.size, min(GAME_AREA_HEIGHT - self.size, self.target_y))
            
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            if distance > 1:
                self.x += dx * 0.05
                self.y += dy * 0.05
        
        return True
    
    def draw(self, screen):
        if self.catched:
            self.draw_caught(screen)
        else:
            self.draw_pet(screen)
    
    def draw_pet(self, screen):
        color = self.colors[self.type]
        
        if self.type == 'cat':
            pygame.draw.polygon(screen, color, [
                (self.x, self.y - self.size//2),
                (self.x - self.size//4, self.y - self.size//3),
                (self.x - self.size//2, self.y)
            ])
            pygame.draw.polygon(screen, color, [
                (self.x, self.y - self.size//2),
                (self.x + self.size//4, self.y - self.size//3),
                (self.x + self.size//2, self.y)
            ])
            pygame.draw.ellipse(screen, color, 
                (self.x - self.size//2, self.y - self.size//4, self.size, self.size//2))
            pygame.draw.circle(screen, color, (self.x, self.y + self.size//4), self.size//3)
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y), 5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y), 5)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y), 2)
        
        elif self.type == 'dog':
            pygame.draw.ellipse(screen, color, 
                (self.x - self.size//2, self.y - self.size//3, self.size, self.size//2))
            pygame.draw.circle(screen, color, (self.x, self.y + self.size//4), self.size//3)
            pygame.draw.circle(screen, color, (self.x - self.size//3, self.y - self.size//2), self.size//5)
            pygame.draw.circle(screen, color, (self.x + self.size//3, self.y - self.size//2), self.size//5)
            pygame.draw.ellipse(screen, (255, 255, 255), 
                (self.x - self.size//3, self.y - self.size//6, self.size//4, self.size//4))
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y), 5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y), 5)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y), 2)
        
        elif self.type == 'rabbit':
            pygame.draw.ellipse(screen, color, 
                (self.x - self.size//5, self.y - self.size//2, self.size//5, self.size//2))
            pygame.draw.ellipse(screen, color, 
                (self.x + self.size//10, self.y - self.size//2, self.size//5, self.size//2))
            pygame.draw.circle(screen, color, (self.x, self.y), self.size//3)
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y - self.size//8), 4)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y - self.size//8), 4)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y - self.size//8), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y - self.size//8), 2)
            pygame.draw.line(screen, (255, 182, 193), (self.x - self.size//4, self.y + self.size//6), (self.x - self.size//3, self.y + self.size//3), 2)
            pygame.draw.line(screen, (255, 182, 193), (self.x + self.size//4, self.y + self.size//6), (self.x + self.size//3, self.y + self.size//3), 2)
        
        elif self.type == 'bear':
            pygame.draw.circle(screen, color, (self.x - self.size//3, self.y - self.size//3), self.size//4)
            pygame.draw.circle(screen, color, (self.x + self.size//3, self.y - self.size//3), self.size//4)
            pygame.draw.circle(screen, color, (self.x, self.y), self.size//2.5)
            pygame.draw.circle(screen, (255, 215, 0), (self.x, self.y), self.size//5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y - self.size//8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y - self.size//8), 5)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y - self.size//8), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y - self.size//8), 2)
        
        elif self.type == 'penguin':
            pygame.draw.ellipse(screen, color, 
                (self.x - self.size//3, self.y - self.size//4, self.size*2//3, self.size//2))
            pygame.draw.circle(screen, color, (self.x, self.y + self.size//4), self.size//3)
            pygame.draw.ellipse(screen, (255, 255, 255), 
                (self.x - self.size//3, self.y - self.size//6, self.size*2//3, self.size//3))
            pygame.draw.circle(screen, (255, 255, 255), (self.x - self.size//6, self.y), 5)
            pygame.draw.circle(screen, (255, 255, 255), (self.x + self.size//6, self.y), 5)
            pygame.draw.circle(screen, (0, 0, 0), (self.x - self.size//6, self.y), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + self.size//6, self.y), 2)
            pygame.draw.line(screen, color, (self.x - self.size//2, self.y), (self.x - self.size//1.5, self.y - self.size//4), 3)
            pygame.draw.line(screen, color, (self.x + self.size//2, self.y), (self.x + self.size//1.5, self.y - self.size//4), 3)
    
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
        color = (50, 205, 50)
        pygame.draw.circle(screen, color + (alpha,), (self.x, self.y), int(self.size * (1 + self.caught_animation)), 3)
        font = self.get_chinese_font(32)
        text = font.render('+10', True, SUCCESS_COLOR)
        text_rect = text.get_rect(center=(self.x, self.y - self.size))
        screen.blit(text, text_rect)
    
    def check_click(self, mouse_x, mouse_y):
        distance = ((mouse_x - self.x)**2 + (mouse_y - self.y)**2)**0.5
        return distance < self.size//2