import pygame
import random
from src.config import PROP_TYPES, SCREEN_WIDTH, SCREEN_HEIGHT

class Prop:
    def __init__(self, x, y, prop_type=None):
        self.x = x
        self.y = y
        self.type = prop_type if prop_type else random.choice(list(PROP_TYPES.keys()))
        self.config = PROP_TYPES[self.type]
        self.size = 20
        self.speed = 2
        self.active = True
        
    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT + self.size:
            self.active = False
            
    def draw(self, screen):
        color = self.config['color']
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size, 2)
        
        font = pygame.font.Font(None, 16)
        icon = ''
        if self.type == 'power_up':
            icon = 'P'
        elif self.type == 'shield':
            icon = 'S'
        elif self.type == 'health':
            icon = '+'
        elif self.type == 'bomb':
            icon = 'B'
            
        text = font.render(icon, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)
    
    def is_active(self):
        return self.active
    
    def get_type(self):
        return self.type
    
    def get_config(self):
        return self.config

class PropManager:
    def __init__(self):
        self.props = []
        self.drop_chance = 0.15
        
    def try_spawn(self, x, y):
        if random.random() < self.drop_chance:
            self.add_prop(x, y)
            
    def add_prop(self, x, y, prop_type=None):
        prop = Prop(x, y, prop_type)
        self.props.append(prop)
        
    def update(self):
        for prop in self.props[:]:
            prop.update()
            if not prop.is_active():
                self.props.remove(prop)
                
    def draw(self, screen):
        for prop in self.props:
            prop.draw(screen)
            
    def get_props(self):
        return self.props
    
    def clear_all(self):
        self.props = []
        
    def set_drop_chance(self, chance):
        self.drop_chance = min(1.0, max(0.0, chance))