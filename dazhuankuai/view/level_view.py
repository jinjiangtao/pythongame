import pygame
from view.font_utils import get_chinese_font

class LevelView:
    def __init__(self, screen):
        self.screen = screen
        self.font = get_chinese_font(64)
        self.medium_font = get_chinese_font(36)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (100, 150, 255)

    def render(self, level, countdown):
        self.screen.fill(self.black)
        
        level_text = self.font.render(f"第 {level} 关", True, self.white)
        level_rect = level_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(level_text, level_rect)
        
        pygame.draw.line(self.screen, self.blue, (self.screen.get_width() // 2 - 100, 250), 
                        (self.screen.get_width() // 2 + 100, 250), 3)
        
        if countdown > 0:
            countdown_text = self.font.render(str(countdown), True, self.blue)
            countdown_rect = countdown_text.get_rect(center=(self.screen.get_width() // 2, 350))
            self.screen.blit(countdown_text, countdown_rect)
        else:
            ready_text = self.medium_font.render("准备开始!", True, self.white)
            ready_rect = ready_text.get_rect(center=(self.screen.get_width() // 2, 350))
            self.screen.blit(ready_text, ready_rect)
        
        hint_text = self.medium_font.render("按空格键发射小球", True, (100, 100, 100))
        hint_rect = hint_text.get_rect(center=(self.screen.get_width() // 2, 450))
        self.screen.blit(hint_text, hint_rect)
