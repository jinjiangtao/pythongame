import pygame

class LevelView:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        self.font = pygame.font.Font(None, 72)
        self.medium_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        self.colors = {
            'background': (10, 10, 30),
            'title': (100, 200, 255),
            'text': (255, 255, 255),
            'accent': (255, 200, 100)
        }
        
        self.level = 1
        self.countdown = 3
        
    def set_level(self, level):
        self.level = level
        self.countdown = 3
    
    def set_countdown(self, countdown):
        self.countdown = countdown
    
    def draw_background(self):
        self.screen.fill(self.colors['background'])
        
        for i in range(0, self.width, 30):
            for j in range(0, self.height, 30):
                dist = ((i - self.width // 2) ** 2 + (j - self.height // 2) ** 2) ** 0.5
                alpha = max(0, 255 - int(dist / 2))
                pygame.draw.circle(self.screen, (50, 100, 150, alpha), (i, j), 2)

    def draw_level_text(self):
        level_text = self.font.render(f"关卡 {self.level}", True, self.colors['title'])
        level_rect = level_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(level_text, level_rect)
        
        ready_text = self.medium_font.render("准备开始", True, self.colors['accent'])
        ready_rect = ready_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(ready_text, ready_rect)

    def draw_countdown(self):
        if self.countdown > 0:
            countdown_text = self.font.render(str(self.countdown), True, (255, 100, 100))
            countdown_rect = countdown_text.get_rect(center=(self.width // 2, self.height // 2 + 100))
            self.screen.blit(countdown_text, countdown_rect)

    def render(self):
        self.draw_background()
        self.draw_level_text()
        self.draw_countdown()
        pygame.display.flip()