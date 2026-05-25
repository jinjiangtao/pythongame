"""
主菜单绘制 - 游戏开始界面
"""

import os
import pygame

class MainMenu:
    def __init__(self):
        self.font_title = None
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
                    self.font_title = pygame.font.Font(font_path, 72)
                    self.font_large = pygame.font.Font(font_path, 36)
                    self.font_medium = pygame.font.Font(font_path, 28)
                    self.font_small = pygame.font.Font(font_path, 22)
                else:
                    try:
                        self.font_title = pygame.font.SysFont('Microsoft YaHei', 72)
                        self.font_large = pygame.font.SysFont('Microsoft YaHei', 36)
                        self.font_medium = pygame.font.SysFont('Microsoft YaHei', 28)
                        self.font_small = pygame.font.SysFont('Microsoft YaHei', 22)
                    except:
                        self.font_title = pygame.font.SysFont('Arial', 72)
                        self.font_large = pygame.font.SysFont('Arial', 36)
                        self.font_medium = pygame.font.SysFont('Arial', 28)
                        self.font_small = pygame.font.SysFont('Arial', 22)
                
                self.font_title.set_bold(True)
                self.fonts_initialized = True
                return
            except:
                continue
        
        self.font_title = pygame.font.Font(None, 100)
        self.font_large = pygame.font.Font(None, 54)
        self.font_medium = pygame.font.Font(None, 42)
        self.font_small = pygame.font.Font(None, 34)
        self.fonts_initialized = True

    def draw(self, surface, screen_width, screen_height):
        surface.fill((0, 0, 10))
        
        title = self.font_title.render("太空陨石躲避战", True, (100, 200, 255))
        title_rect = title.get_rect(center=(screen_width // 2, 120))
        surface.blit(title, title_rect)
        
        subtitle = self.font_medium.render("Space Asteroid Survival", True, (150, 150, 200))
        subtitle_rect = subtitle.get_rect(center=(screen_width // 2, 170))
        surface.blit(subtitle, subtitle_rect)
        
        instructions = [
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "  游戏说明",
            "",
            "  🎮 操控飞船: 鼠标移动飞船位置",
            "",
            "  ⭐ 目标: 躲避不断掉落的陨石",
            "",
            "  ❤️ 血量: 被陨石砸中会扣血",
            "",
            "  ⏱️ 坚持越久，得分越高",
            "",
            "  📈 难度: 生存时间越长，难度越高",
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        ]
        
        y_offset = 230
        for line in instructions:
            text = self.font_small.render(line, True, (200, 200, 200))
            text_rect = text.get_rect(center=(screen_width // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 30
        
        start_text = self.font_large.render("点击任意位置开始游戏", True, (100, 255, 100))
        start_rect = start_text.get_rect(center=(screen_width // 2, 680))
        surface.blit(start_text, start_rect)
        
        quit_text = self.font_medium.render("按 ESC 退出", True, (255, 100, 100))
        quit_rect = quit_text.get_rect(center=(screen_width // 2, 730))
        surface.blit(quit_text, quit_rect)
