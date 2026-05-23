import pygame

class EndView:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font = pygame.font.Font(None, 72)
        self.medium_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        self.colors = {
            'background': (10, 10, 30),
            'title': (255, 100, 100),
            'button': (50, 150, 255),
            'button_hover': (100, 200, 255),
            'text': (255, 255, 255),
            'accent': (255, 200, 100),
            'success': (100, 255, 100)
        }
        
        self.restart_button = pygame.Rect(self.width // 2 - 120, self.height // 2 + 20, 240, 60)
        self.main_menu_button = pygame.Rect(self.width // 2 - 120, self.height // 2 + 100, 240, 60)
        
        self.score = 0
        self.level = 1
        self.high_score = 0
        self.is_new_high_score = False

    def set_data(self, score, level, high_score):
        self.score = score
        self.level = level
        self.high_score = high_score
        self.is_new_high_score = score >= high_score

    def draw_background(self):
        self.screen.fill(self.colors['background'])
        
        for i in range(0, self.width, 40):
            pygame.draw.line(self.screen, (30, 30, 60), (i, 0), (i, self.height), 1)
        for i in range(0, self.height, 40):
            pygame.draw.line(self.screen, (30, 30, 60), (0, i), (self.width, i), 1)

    def draw_title(self):
        title_text = self.font.render("游戏结束", True, self.colors['title'])
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3 - 50))
        self.screen.blit(title_text, title_rect)
        
        if self.is_new_high_score:
            new_high_text = self.medium_font.render("🎉 新纪录！", True, self.colors['success'])
            new_high_rect = new_high_text.get_rect(center=(self.width // 2, self.height // 3 + 20))
            self.screen.blit(new_high_text, new_high_rect)

    def draw_stats(self):
        score_text = self.medium_font.render(f"最终得分: {self.score}", True, self.colors['accent'])
        level_text = self.medium_font.render(f"到达关卡: {self.level}", True, (100, 255, 200))
        high_score_text = self.small_font.render(f"最高分: {self.high_score}", True, (200, 200, 200))
        
        self.screen.blit(score_text, (self.width // 2 - 120, self.height // 2 - 80))
        self.screen.blit(level_text, (self.width // 2 - 120, self.height // 2 - 30))
        self.screen.blit(high_score_text, (self.width // 2 - 100, self.height // 2 + 170))

    def draw_button(self, rect, text, is_hovered):
        color = self.colors['button_hover'] if is_hovered else self.colors['button']
        
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        
        text_surface = self.medium_font.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def render(self, mouse_pos):
        self.draw_background()
        self.draw_title()
        self.draw_stats()
        
        restart_hovered = self.restart_button.collidepoint(mouse_pos)
        menu_hovered = self.main_menu_button.collidepoint(mouse_pos)
        
        self.draw_button(self.restart_button, "重新开始", restart_hovered)
        self.draw_button(self.main_menu_button, "返回主菜单", menu_hovered)
        
        pygame.display.flip()

    def get_clicked_button(self, mouse_pos):
        if self.restart_button.collidepoint(mouse_pos):
            return 'restart'
        if self.main_menu_button.collidepoint(mouse_pos):
            return 'menu'
        return None