import pygame

class EndView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 64)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grey = (100, 100, 100)
        self.red = (255, 100, 100)
        self.blue = (100, 150, 255)
        self.buttons = []
        self._init_buttons()

    def _init_buttons(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        restart_button = {
            'rect': pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50),
            'text': '重新开始',
            'action': 'restart'
        }
        
        menu_button = {
            'rect': pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 60, 200, 50),
            'text': '返回主菜单',
            'action': 'menu'
        }
        
        self.buttons = [restart_button, menu_button]

    def render(self, score, level, high_score, is_new_high_score):
        self.screen.fill(self.black)
        
        game_over_text = self.font.render("游戏结束", True, self.red)
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        if is_new_high_score:
            new_high_text = self.medium_font.render("🎉 新纪录! 🎉", True, (255, 200, 50))
            new_high_rect = new_high_text.get_rect(center=(self.screen.get_width() // 2, 160))
            self.screen.blit(new_high_text, new_high_rect)
        
        score_text = self.medium_font.render(f"最终得分: {score}", True, self.white)
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 250))
        self.screen.blit(score_text, score_rect)
        
        level_text = self.medium_font.render(f"到达关卡: {level}", True, self.white)
        level_rect = level_text.get_rect(center=(self.screen.get_width() // 2, 300))
        self.screen.blit(level_text, level_rect)
        
        high_score_text = self.small_font.render(f"最高分: {high_score}", True, self.blue)
        high_score_rect = high_score_text.get_rect(center=(self.screen.get_width() // 2, 350))
        self.screen.blit(high_score_text, high_score_rect)
        
        pygame.draw.line(self.screen, self.grey, (self.screen.get_width() // 2 - 120, 400), 
                        (self.screen.get_width() // 2 + 120, 400), 2)
        
        for button in self.buttons:
            hover_color = (150, 200, 255) if button['rect'].collidepoint(pygame.mouse.get_pos()) else self.blue
            pygame.draw.rect(self.screen, hover_color, button['rect'])
            pygame.draw.rect(self.screen, self.white, button['rect'], 2)
            text = self.medium_font.render(button['text'], True, self.black)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

    def handle_click(self, pos):
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                return button['action']
        return None
