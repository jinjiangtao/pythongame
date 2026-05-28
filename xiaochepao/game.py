import pygame
import random
import sys
import os
from constants import *
from car import Car
from obstacle import Obstacle

def get_chinese_font(size):
    font_names = ['simhei', 'simsun', 'msyh', 'microsoftyahei', 'kaiti', 'fangsong']
    for font_name in font_names:
        try:
            return pygame.font.SysFont(font_name, size)
        except:
            continue
    
    font_paths = [
        'C:\\Windows\\Fonts\\simhei.ttf',
        'C:\\Windows\\Fonts\\simsun.ttc',
        'C:\\Windows\\Fonts\\msyh.ttc',
        'C:\\Windows\\Fonts\\msyhbd.ttc',
    ]
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                continue
    
    return pygame.font.Font(None, size)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("小车跑酷")
        
        self.clock = pygame.time.Clock()
        self.reset()
        
        self.font = get_chinese_font(36)
        self.small_font = get_chinese_font(24)
        
        self.last_obstacle_time = 0
        self.obstacle_interval = random.randint(OBSTACLE_SPAWN_INTERVAL_MIN, OBSTACLE_SPAWN_INTERVAL_MAX)
    
    def reset(self):
        self.car = Car()
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.last_score_time = pygame.time.get_ticks()
    
    def spawn_obstacle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > self.obstacle_interval:
            self.obstacles.append(Obstacle())
            self.last_obstacle_time = current_time
            self.obstacle_interval = random.randint(OBSTACLE_SPAWN_INTERVAL_MIN, OBSTACLE_SPAWN_INTERVAL_MAX)
    
    def update_score(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_score_time >= 100:
            self.score += 1
            self.last_score_time = current_time
    
    def check_collisions(self):
        car_rect = self.car.get_rect()
        for obstacle in self.obstacles:
            obstacle_rect = obstacle.get_rect()
            if car_rect.colliderect(obstacle_rect):
                self.game_over = True
                break
    
    def update(self):
        if not self.game_over:
            self.car.update()
            
            self.spawn_obstacle()
            
            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)
            
            self.update_score()
            self.check_collisions()
    
    def draw_background(self):
        self.screen.fill(BLUE)
        
        for i in range(0, SCREEN_WIDTH, 100):
            pygame.draw.rect(self.screen, (70, 180, 255), (i, 0, 50, SCREEN_HEIGHT))
        
        pygame.draw.rect(self.screen, GREEN, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))
        
        pygame.draw.rect(self.screen, DARK_GRAY, (0, GROUND_Y, SCREEN_WIDTH, 10))
        
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.rect(self.screen, GRAY, (i, GROUND_Y + 20, 20, 5))
    
    def draw_ui(self):
        score_text = self.font.render(f"分数: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        hint_text = self.small_font.render("空格键跳跃 | R键重新开始 | ESC键退出", True, WHITE)
        self.screen.blit(hint_text, (SCREEN_WIDTH - 350, 20))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("游戏结束!", True, RED)
        score_text = self.font.render(f"最终分数: {self.score}", True, YELLOW)
        restart_text = self.small_font.render("按 R 键重新开始 | 按 ESC 键退出", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        self.draw_background()
        
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        self.car.draw(self.screen)
        
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.car.jump()
                
                if event.key == pygame.K_r:
                    self.reset()
                
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)