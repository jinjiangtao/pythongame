"""
游戏UI绘制 - 显示分数、血量、时间等信息
"""

import os
import pygame

class GameUI:
    def __init__(self):
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.fonts_initialized = False

    def init_fonts(self):
        pygame.font.init()
        
        font_paths = [
            "C:/Users/84012/AppData/Local/Microsoft/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            None
        ]
        
        for font_path in font_paths:
            try:
                if font_path and os.path.exists(font_path):
                    self.font_large = pygame.font.Font(font_path, 48)
                    self.font_medium = pygame.font.Font(font_path, 32)
                    self.font_small = pygame.font.Font(font_path, 24)
                else:
                    try:
                        self.font_large = pygame.font.SysFont('Microsoft YaHei', 48)
                        self.font_medium = pygame.font.SysFont('Microsoft YaHei', 32)
                        self.font_small = pygame.font.SysFont('Microsoft YaHei', 24)
                    except:
                        self.font_large = pygame.font.SysFont('Arial', 48)
                        self.font_medium = pygame.font.SysFont('Arial', 32)
                        self.font_small = pygame.font.SysFont('Arial', 24)
                
                self.font_large.set_bold(True)
                self.font_medium.set_bold(True)
                self.fonts_initialized = True
                return
            except:
                continue
        
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.fonts_initialized = True

    def draw_score_panel(self, surface, game_data, x=20, y=20):
        time_text = self.font_small.render(f"生存时间: {game_data.get_display_time()}", True, (255, 255, 255))
        surface.blit(time_text, (x, y))
        
        score_text = self.font_small.render(f"得分: {game_data.score}", True, (255, 255, 255))
        surface.blit(score_text, (x, y + 30))
        
        diff_text = self.font_small.render(f"难度: {game_data.difficulty:.1f}x", True, (255, 200, 100))
        surface.blit(diff_text, (x, y + 60))

    def draw_health_bar(self, surface, game_data, x, y, width=200, height=25):
        pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height), border_radius=5)
        
        health_ratio = game_data.health / game_data.max_health
        health_width = int(width * health_ratio)
        
        if health_ratio > 0.6:
            color = (50, 255, 50)
        elif health_ratio > 0.3:
            color = (255, 255, 50)
        else:
            color = (255, 50, 50)
        
        pygame.draw.rect(surface, color, (x, y, health_width, height), border_radius=5)
        
        health_text = self.font_small.render(f"血量: {game_data.health}%", True, (255, 255, 255))
        text_rect = health_text.get_rect(center=(x + width // 2, y + height // 2))
        surface.blit(health_text, text_rect)

    def draw_game_over(self, surface, game_data, screen_width, screen_height):
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        title = self.font_large.render("游戏结束", True, (255, 50, 50))
        title_rect = title.get_rect(center=(screen_width // 2, screen_height // 3))
        surface.blit(title, title_rect)
        
        score_label = self.font_medium.render(f"最终得分: {game_data.score}", True, (255, 255, 255))
        score_rect = score_label.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        surface.blit(score_label, score_rect)
        
        time_label = self.font_medium.render(f"生存时间: {game_data.get_display_time()}", True, (255, 255, 255))
        time_rect = time_label.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
        surface.blit(time_label, time_rect)
        
        restart_text = self.font_small.render("按 R 键重新开始", True, (100, 255, 100))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        surface.blit(restart_text, restart_rect)
        
        quit_text = self.font_small.render("按 ESC 退出游戏", True, (255, 100, 100))
        quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 140))
        surface.blit(quit_text, quit_rect)
