import pygame

class StartView:
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
            'button': (50, 150, 255),
            'button_hover': (100, 200, 255),
            'text': (255, 255, 255),
            'accent': (255, 200, 100)
        }
        
        self.start_button = pygame.Rect(self.width // 2 - 120, self.height // 2 - 30, 240, 60)
        self.continue_button = pygame.Rect(self.width // 2 - 120, self.height // 2 + 50, 240, 60)
        self.quit_button = pygame.Rect(self.width // 2 - 120, self.height // 2 + 130, 240, 60)
        
        self.has_save = False
        self.saved_level = 1
        self.saved_score = 0

    def set_save_data(self, has_save, level, score):
        self.has_save = has_save
        self.saved_level = level
        self.saved_score = score

    def draw_background(self):
        self.screen.fill(self.colors['background'])
        
        for i in range(0, self.width, 30):
            for j in range(0, self.height, 30):
                size = ((i + j) // 30) % 3 + 1
                pygame.draw.circle(self.screen, (30, 30, 60), (i, j), size)

    def draw_title(self):
        title_text = self.font.render("打砖块", True, self.colors['title'])
        subtitle_text = self.small_font.render("高难度挑战版", True, self.colors['accent'])
        
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3 - 50))
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, self.height // 3))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)

    def draw_button(self, rect, text, is_hovered):
        color = self.colors['button_hover'] if is_hovered else self.colors['button']
        
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        
        text_surface = self.medium_font.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_instructions(self):
        instructions = [
            "← → 或鼠标移动挡板",
            "空格键发射小球",
            "P 键暂停游戏",
            "道具说明：",
            "↔ 挡板变大  ↕ 挡板变小",
            "▲ 加速  ▼ 减速",
            "✦ 分裂  ♥ 生命",
            "● 吸附  ★ 无敌"
        ]
        
        y = self.height - 280
        for i, line in enumerate(instructions):
            text = self.small_font.render(line, True, (150, 150, 200))
            self.screen.blit(text, (self.width // 2 - 150, y + i * 25))

    def draw_save_info(self):
        if self.has_save:
            save_text = self.small_font.render(f"存档: 关卡 {self.saved_level} | 得分 {self.saved_score}", True, (100, 255, 100))
            self.screen.blit(save_text, (self.width // 2 - 150, self.height // 2 + 200))

    def render(self, mouse_pos):
        self.draw_background()
        self.draw_title()
        
        start_hovered = self.start_button.collidepoint(mouse_pos)
        continue_hovered = self.continue_button.collidepoint(mouse_pos) if self.has_save else False
        quit_hovered = self.quit_button.collidepoint(mouse_pos)
        
        self.draw_button(self.start_button, "开始游戏", start_hovered)
        
        if self.has_save:
            self.draw_button(self.continue_button, "继续游戏", continue_hovered)
        
        self.draw_button(self.quit_button, "退出游戏", quit_hovered)
        
        self.draw_instructions()
        self.draw_save_info()
        
        pygame.display.flip()

    def get_clicked_button(self, mouse_pos):
        if self.start_button.collidepoint(mouse_pos):
            return 'start'
        if self.has_save and self.continue_button.collidepoint(mouse_pos):
            return 'continue'
        if self.quit_button.collidepoint(mouse_pos):
            return 'quit'
        return None