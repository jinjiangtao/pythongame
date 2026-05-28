import pygame
from config import *

class ScoreTimer:
    def __init__(self):
        self.score = 0
        self.level = INITIAL_LEVEL
        self.time_left = GAME_DURATION
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
    
    def update(self):
        if self.game_over:
            return
        
        elapsed = pygame.time.get_ticks() - self.start_time
        self.time_left = max(0, GAME_DURATION - elapsed // 1000)
        
        if self.time_left <= 0:
            self.game_over = True
        
        new_level = self.score // LEVEL_UP_SCORE + 1
        if new_level > self.level:
            self.level = new_level
    
    def add_score(self, points):
        self.score += points
    
    def reset(self):
        self.score = 0
        self.level = INITIAL_LEVEL
        self.time_left = GAME_DURATION
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
    
    def draw(self, screen):
        font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        
        pygame.draw.rect(screen, TOP_BAR_COLOR, (0, 0, SCREEN_WIDTH, TOP_BAR_HEIGHT))
        
        score_text = font_large.render(f'得分: {self.score}', True, TEXT_COLOR)
        score_rect = score_text.get_rect(left=20, centery=TOP_BAR_HEIGHT // 2)
        screen.blit(score_text, score_rect)
        
        time_text = font_large.render(f'时间: {self.time_left}s', True, TEXT_COLOR)
        time_rect = time_text.get_rect(centerx=SCREEN_WIDTH // 2, centery=TOP_BAR_HEIGHT // 2)
        screen.blit(time_text, time_rect)
        
        level_text = font_large.render(f'关卡: {self.level}', True, TEXT_COLOR)
        level_rect = level_text.get_rect(right=SCREEN_WIDTH - 20, centery=TOP_BAR_HEIGHT // 2)
        screen.blit(level_text, level_rect)