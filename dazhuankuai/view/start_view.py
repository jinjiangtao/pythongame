import pygame
from view.font_utils import get_chinese_font

class StartView:
    def __init__(self, screen):
        self.screen = screen
        self.font = get_chinese_font(64)
        self.medium_font = get_chinese_font(36)
        self.small_font = get_chinese_font(24)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grey = (100, 100, 100)
        self.blue = (100, 150, 255)
        self.buttons = []
        self._init_buttons()

    def _init_buttons(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        start_button = {
            'rect': pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 30, 200, 50),
            'text': '开始游戏',
            'action': 'start'
        }
        
        continue_button = {
            'rect': pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 30, 200, 50),
            'text': '继续游戏',
            'action': 'continue'
        }
        
        self.buttons = [start_button, continue_button]

    def render(self, high_score):
        self.screen.fill(self.black)
        title_text = self.font.render("打砖块", True, self.white)
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        pygame.draw.line(self.screen, self.blue, (self.screen.get_width() // 2 - 150, 140), 
                        (self.screen.get_width() // 2 + 150, 140), 3)
        
        high_score_text = self.medium_font.render(f"最高分: {high_score}", True, self.blue)
        high_score_rect = high_score_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(high_score_text, high_score_rect)
        
        for button in self.buttons:
            hover_color = (150, 200, 255) if button['rect'].collidepoint(pygame.mouse.get_pos()) else self.blue
            pygame.draw.rect(self.screen, hover_color, button['rect'])
            pygame.draw.rect(self.screen, self.white, button['rect'], 2)
            text = self.medium_font.render(button['text'], True, self.black)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        
        instructions = [
            "操作说明:",
            "← → 或 A D: 移动挡板",
            "鼠标: 控制挡板位置",
            "空格键: 发射小球/暂停",
            "ESC: 返回主菜单"
        ]
        
        y = 350
        for i, line in enumerate(instructions):
            text = self.small_font.render(line, True, self.grey)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += 30
        
        props_info = [
            "道具说明:",
            "+ 挡板变大  ↓ 小球减速  ○ 挡板吸附",
            "- 挡板变小  ↑ 小球加速  ★ 无敌时间",
            "×2 分裂小球  ❤ 额外生命"
        ]
        
        y = 500
        for i, line in enumerate(props_info):
            text = self.small_font.render(line, True, self.grey)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text, text_rect)
            y += 25

    def handle_click(self, pos):
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                return button['action']
        return None
