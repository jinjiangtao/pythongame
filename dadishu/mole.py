import pygame
import random
from constants import *

class Mole:
    def __init__(self, hole):
        self.hole = hole
        self.center_x, self.center_y = hole.get_center()
        self.target_y = self.center_y - MOLE_HEIGHT // 2
        self.current_y = self.center_y + HOLE_HEIGHT // 2
        self.state = 'hidden'
        self.hit_time = 0
        self.show_time = 0
        self.type = 'normal'
        self.type_config = MOLE_TYPES['normal']
    
    def set_type(self, mole_type=None):
        if mole_type is None:
            rand = random.random()
            cumulative = 0
            for m_type, config in MOLE_TYPES.items():
                cumulative += config['probability']
                if rand < cumulative:
                    mole_type = m_type
                    break
        self.type = mole_type
        self.type_config = MOLE_TYPES[mole_type]
    
    def get_points(self):
        return self.type_config['points']
    
    def update(self, current_time):
        if self.state == 'showing':
            if self.current_y > self.target_y:
                self.current_y -= MOLE_SPEED
            else:
                self.current_y = self.target_y
                self.state = 'visible'
                self.show_time = current_time
        elif self.state == 'visible':
            pass
        elif self.state == 'hiding':
            if self.current_y < self.center_y + HOLE_HEIGHT // 2:
                self.current_y += MOLE_SPEED
            else:
                self.current_y = self.center_y + HOLE_HEIGHT // 2
                self.state = 'hidden'
                self.set_type()
        elif self.state == 'hit':
            if current_time - self.hit_time > 500:
                self.state = 'hiding'
    
    def show(self):
        if self.state == 'hidden':
            self.state = 'showing'
    
    def hit(self, current_time):
        if self.state == 'visible':
            self.state = 'hit'
            self.hit_time = current_time
            return True
        return False
    
    def is_visible(self):
        return self.state == 'visible'
    
    def is_hit(self):
        return self.state == 'hit'
    
    def is_hidden(self):
        return self.state == 'hidden'
    
    def get_rect(self):
        return pygame.Rect(
            self.center_x - MOLE_WIDTH // 2,
            self.current_y - MOLE_HEIGHT // 2,
            MOLE_WIDTH,
            MOLE_HEIGHT
        )
    
    def draw(self, screen):
        if self.state == 'hidden':
            return
        
        body_y = self.current_y
        body_x = self.center_x
        
        if self.state == 'hit':
            color = RED
        else:
            color = self.type_config['color']
        
        pygame.draw.ellipse(screen, color,
                          (body_x - MOLE_WIDTH // 2, body_y - MOLE_HEIGHT // 2,
                           MOLE_WIDTH, MOLE_HEIGHT), 0)
        
        pygame.draw.circle(screen, (255, 200, 150), (body_x - 15, body_y - 15), 8)
        pygame.draw.circle(screen, (255, 200, 150), (body_x + 15, body_y - 15), 8)
        
        pygame.draw.circle(screen, BLACK, (body_x - 15, body_y - 18), 4)
        pygame.draw.circle(screen, BLACK, (body_x + 15, body_y - 18), 4)
        
        pygame.draw.circle(screen, (255, 255, 255), (body_x - 13, body_y - 20), 2)
        pygame.draw.circle(screen, (255, 255, 255), (body_x + 17, body_y - 20), 2)
        
        pygame.draw.ellipse(screen, (255, 150, 150),
                          (body_x - 8, body_y - 5, 16, 8), 0)
        
        pygame.draw.polygon(screen, (255, 200, 150), [
            (body_x - 25, body_y - 5),
            (body_x - 35, body_y - 15),
            (body_x - 20, body_y - 10)
        ])
        pygame.draw.polygon(screen, (255, 200, 150), [
            (body_x + 25, body_y - 5),
            (body_x + 35, body_y - 15),
            (body_x + 20, body_y - 10)
        ])
        
        if self.type == 'golden':
            pygame.draw.circle(screen, YELLOW, (body_x, body_y - MOLE_HEIGHT // 2 - 5), 5)
        elif self.type == 'red':
            pygame.draw.polygon(screen, BLACK, [
                (body_x - 10, body_y - MOLE_HEIGHT // 2 - 5),
                (body_x + 10, body_y - MOLE_HEIGHT // 2 - 5),
                (body_x, body_y - MOLE_HEIGHT // 2 - 15)
            ])