import pygame
from config import CELL_ON_COLOR, CELL_OFF_COLOR, CELL_HOVER_COLOR, CELL_BORDER_COLOR, BLACK

class LightCell:
    def __init__(self, x, y, size, row, col):
        self.x = x
        self.y = y
        self.size = size
        self.row = row
        self.col = col
        self.is_on = False
        self.is_hovered = False
        self.rect = pygame.Rect(x, y, size, size)
    
    def draw(self, screen):
        if self.is_on:
            color = CELL_ON_COLOR
            glow_color = (255, 255, 100)
            pygame.draw.rect(screen, glow_color, self.rect.inflate(4, 4), border_radius=4)
        else:
            color = CELL_OFF_COLOR
        
        if self.is_hovered and not self.is_on:
            color = CELL_HOVER_COLOR
        
        pygame.draw.rect(screen, color, self.rect, border_radius=4)
        
        pygame.draw.rect(screen, CELL_BORDER_COLOR, self.rect, 3, border_radius=4)
        
        if self.is_on:
            center_x = self.x + self.size // 2
            center_y = self.y + self.size // 2
            pygame.draw.circle(screen, (255, 255, 200), (center_x, center_y), self.size // 5)
    
    def toggle(self):
        self.is_on = not self.is_on
    
    def set_state(self, state):
        self.is_on = state
    
    def get_state(self):
        return self.is_on
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)