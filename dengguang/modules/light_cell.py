import pygame
from config import CELL_ON_COLOR, CELL_OFF_COLOR, CELL_HOVER_COLOR, CELL_BORDER_COLOR, BLACK, OBSTACLE_COLOR, FROZEN_COLOR

class LightCell:
    def __init__(self, x, y, size, row, col):
        self.x = x
        self.y = y
        self.size = size
        self.row = row
        self.col = col
        self.is_on = False
        self.is_hovered = False
        self.is_obstacle = False
        self.is_frozen = False
        self.rect = pygame.Rect(x, y, size, size)
        
        self.animation_phase = 0
        self.animation_type = None
        self.animation_start = 0
    
    def draw(self, screen, theme=None):
        if theme is None:
            on_color = CELL_ON_COLOR
            off_color = CELL_OFF_COLOR
            hover_color = CELL_HOVER_COLOR
            border_color = CELL_BORDER_COLOR
            glow_color = (255, 255, 100)
        else:
            on_color = theme["cell_on"]
            off_color = theme["cell_off"]
            hover_color = theme["cell_hover"]
            border_color = theme["cell_border"]
            glow_color = theme["glow_color"]
        
        if self.is_obstacle:
            pygame.draw.rect(screen, OBSTACLE_COLOR, self.rect, border_radius=8)
            pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=8)
            
            pygame.draw.line(screen, (100, 100, 100), 
                           (self.x + 10, self.y + 10), 
                           (self.x + self.size - 10, self.y + self.size - 10), 3)
            pygame.draw.line(screen, (100, 100, 100), 
                           (self.x + self.size - 10, self.y + 10), 
                           (self.x + 10, self.y + self.size - 10), 3)
            return
        
        if self.is_frozen:
            frozen_alpha = 150 + int(50 * (1 + pygame.time.get_ticks() / 500 % 2))
            
            surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(surface, (FROZEN_COLOR[0], FROZEN_COLOR[1], FROZEN_COLOR[2], frozen_alpha), 
                           (0, 0, self.size, self.size), border_radius=8)
            screen.blit(surface, (self.x, self.y))
            
            pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=8)
            
            ice_crystal = pygame.font.Font(None, self.size // 2).render("❄", True, (200, 230, 255))
            crystal_rect = ice_crystal.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            screen.blit(ice_crystal, crystal_rect)
            return
        
        if self.is_on:
            glow_size = self.size + 8 + int(8 * pygame.time.get_ticks() / 300 % 2)
            glow_x = self.x + self.size // 2 - glow_size // 2
            glow_y = self.y + self.size // 2 - glow_size // 2
            
            glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            glow_alpha = 40 + int(20 * pygame.time.get_ticks() / 300 % 2)
            pygame.draw.rect(glow_surface, (glow_color[0], glow_color[1], glow_color[2], glow_alpha), 
                           (0, 0, glow_size, glow_size), border_radius=8)
            screen.blit(glow_surface, (glow_x, glow_y))
            
            color = on_color
        else:
            color = off_color
        
        if self.is_hovered and not self.is_on:
            hover_alpha = 50 + int(30 * pygame.time.get_ticks() / 200 % 2)
            hover_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(hover_surface, (hover_color[0], hover_color[1], hover_color[2], hover_alpha), 
                           (0, 0, self.size, self.size), border_radius=8)
            screen.blit(hover_surface, (self.x, self.y))
        
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=8)
        
        if self.is_on:
            center_x = self.x + self.size // 2
            center_y = self.y + self.size // 2
            
            inner_circle_radius = self.size // 5
            inner_color = (255, 255, 200)
            pygame.draw.circle(screen, inner_color, (center_x, center_y), inner_circle_radius)
            
            highlight_radius = inner_circle_radius // 2
            highlight_color = (255, 255, 255)
            pygame.draw.circle(screen, highlight_color, 
                             (center_x - highlight_radius // 2, center_y - highlight_radius // 2), 
                             highlight_radius)
    
    def toggle(self):
        if not self.is_obstacle and not self.is_frozen:
            self.is_on = not self.is_on
    
    def set_state(self, state):
        if not self.is_obstacle:
            self.is_on = state
    
    def get_state(self):
        return self.is_on
    
    def check_hover(self, mouse_pos):
        if not self.is_obstacle:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
        else:
            self.is_hovered = False
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos) and not self.is_obstacle
    
    def set_obstacle(self, value=True):
        self.is_obstacle = value
        if value:
            self.is_on = False
    
    def set_frozen(self, value=True):
        self.is_frozen = value
    
    def get_cell_center(self):
        return (self.x + self.size // 2, self.y + self.size // 2)