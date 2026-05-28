import pygame
from constants import *
from font_utils import get_chinese_font

class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.time_left = GAME_DURATION
        self.combo = 0
        self.max_combo = 0
        self.level = 1
        self.font = get_chinese_font(FONT_SIZE)
        self.level_font = get_chinese_font(32)
    
    def add_score(self, points=10):
        combo_bonus = int(points * self.combo * COMBO_MULTIPLIER)
        self.score += points + combo_bonus
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        return combo_bonus
    
    def reset_combo(self):
        self.combo = 0
    
    def set_time(self, time):
        self.time_left = time
    
    def add_time(self, seconds):
        self.time_left += seconds
    
    def level_up(self):
        if self.level < MAX_LEVEL:
            self.level += 1
            return True
        return False
    
    def get_level(self):
        return self.level
    
    def reset(self):
        self.score = 0
        self.time_left = GAME_DURATION
        self.combo = 0
        self.max_combo = 0
        self.level = 1
    
    def draw(self, screen):
        score_text = self.font.render(f"得分: {self.score}", True, BLACK)
        time_text = self.font.render(f"时间: {self.time_left}秒", True, BLACK)
        level_text = self.level_font.render(f"关卡: {self.level}", True, BLUE)
        
        screen.blit(score_text, (20, 20))
        screen.blit(time_text, (SCREEN_WIDTH - 150, 20))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 20))
        
        if self.combo > 1:
            combo_font = get_chinese_font(28)
            combo_color = ORANGE if self.combo < 5 else RED
            combo_text = combo_font.render(f"连击 x{self.combo}", True, combo_color)
            combo_rect = combo_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            screen.blit(combo_text, combo_rect)
    
    def get_score(self):
        return self.score
    
    def get_time(self):
        return self.time_left