import pygame
import config
import os

class UI:
    def __init__(self):
        pygame.font.init()
        
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc"
        ]
        
        font = None
        valid_font_path = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = pygame.font.Font(font_path, 24)
                    valid_font_path = font_path
                    break
                except:
                    continue
        
        if valid_font_path:
            self.font_large = pygame.font.Font(valid_font_path, 48)
            self.font_medium = pygame.font.Font(valid_font_path, 32)
            self.font_small = pygame.font.Font(valid_font_path, 22)
        else:
            self.font_large = pygame.font.Font(None, 60)
            self.font_medium = pygame.font.Font(None, 40)
            self.font_small = pygame.font.Font(None, 30)
        
        self.timer_color = config.TEXT_COLOR
        self.message_surface = None
        self.message_timer = 0
    
    def draw_stats(self, surface, time_left, steps, pairs_left):
        """绘制统计信息"""
        if time_left <= 10:
            self.timer_color = config.WARNING_COLOR
        else:
            self.timer_color = config.TEXT_COLOR
        
        timer_text = self.font_large.render(f"Time: {int(time_left)}s", True, self.timer_color)
        surface.blit(timer_text, (config.STATS_LEFT_MARGIN, config.UI_TOP_MARGIN))
        
        steps_text = self.font_large.render(f"Steps: {steps}", True, config.TEXT_COLOR)
        surface.blit(steps_text, (config.SCREEN_WIDTH - steps_text.get_width() - config.STATS_RIGHT_MARGIN, config.UI_TOP_MARGIN))
        
        pairs_text = self.font_medium.render(f"Pairs Left: {pairs_left}", True, config.ACCENT_COLOR)
        pairs_rect = pairs_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.UI_TOP_MARGIN + 20))
        surface.blit(pairs_text, pairs_rect)
    
    def draw_message(self, surface, message, submessage=""):
        """绘制居中消息"""
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        main_text = self.font_large.render(message, True, config.TEXT_COLOR)
        main_rect = main_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 30))
        surface.blit(main_text, main_rect)
        
        if submessage:
            sub_text = self.font_medium.render(submessage, True, config.TEXT_COLOR)
            sub_rect = sub_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 30))
            surface.blit(sub_text, sub_rect)
    
    def draw_preview_message(self, surface):
        """绘制预览提示"""
        preview_text = self.font_medium.render("记住卡片位置!", True, config.WARNING_COLOR)
        preview_rect = preview_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        surface.blit(preview_text, preview_rect)
    
    def draw_controls_hint(self, surface):
        """绘制控制提示"""
        hint_text = self.font_small.render("按 R 重新开始  |  按 ESC 退出", True, (150, 150, 150))
        hint_rect = hint_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 30))
        surface.blit(hint_text, hint_rect)
