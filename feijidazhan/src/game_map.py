import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_COLORS

class GameMap:
    def __init__(self):
        self.stars = []
        self.scroll_speed = 2
        self.init_stars()
        
    def init_stars(self):
        for _ in range(100):
            x = pygame.randint(0, SCREEN_WIDTH)
            y = pygame.randint(0, SCREEN_HEIGHT)
            size = pygame.randint(1, 3)
            speed = pygame.randint(1, 3)
            self.stars.append({'x': x, 'y': y, 'size': size, 'speed': speed})
            
    def update(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = pygame.randint(0, SCREEN_WIDTH)
                
    def draw(self, screen):
        screen.fill(GAME_COLORS['background'])
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), 
                             (star['x'], star['y']), star['size'])
            
    def check_bounds(self, x, y, size):
        return (x >= size // 2 and 
                x <= SCREEN_WIDTH - size // 2 and 
                y >= size // 2 and 
                y <= SCREEN_HEIGHT - size // 2)
    
    def is_out_of_bounds(self, x, y, size):
        return (x < -size or 
                x > SCREEN_WIDTH + size or 
                y < -size or 
                y > SCREEN_HEIGHT + size)
    
    def get_center(self):
        return (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def get_player_spawn_position(self):
        return (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)