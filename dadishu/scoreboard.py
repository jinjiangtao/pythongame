import pygame
from constants import *

class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.time_left = GAME_DURATION
        self.font = pygame.font.Font(None, FONT_SIZE)
    
    def add_score(self, points=10):
        self.score += points
    
    def set_time(self, time):
        self.time_left = time
    
    def reset(self):
        self.score = 0
        self.time_left = GAME_DURATION
    
    def draw(self, screen):
        score_text = self.font.render(f"得分: {self.score}", True, BLACK)
        time_text = self.font.render(f"时间: {self.time_left}秒", True, BLACK)
        
        screen.blit(score_text, (20, 20))
        screen.blit(time_text, (SCREEN_WIDTH - 150, 20))
    
    def get_score(self):
        return self.score
    
    def get_time(self):
        return self.time_left