import pygame
import os

class Toolbar:
    def __init__(self, screen, width=150):
        self.screen = screen
        self.width = width
        self.height = screen.get_height()
        self.rect = pygame.Rect(0, 50, width, self.height - 50)
        self.bg_color = (45, 45, 45)
        self.button_color = (60, 60, 60)
        self.button_hover_color = (80, 80, 80)
        self.button_selected_color = (100, 150, 200)
        self.text_color = (255, 255, 255)
        
        self.font = self.get_chinese_font(14)
        
        self.shape_buttons = [
            {'type': 'circle', 'label': '圆形'},
            {'type': 'rectangle', 'label': '矩形'},
            {'type': 'triangle', 'label': '三角形'},
            {'type': 'diamond', 'label': '四边形'},
            {'type': 'star', 'label': '星形'}
        ]
        
        self.color_buttons = [
            (255, 0, 0),    # 红
            (0, 255, 0),    # 绿
            (0, 0, 255),    # 蓝
            (255, 255, 0),  # 黄
            (255, 165, 0),  # 橙
            (128, 0, 128),  # 紫
            (255, 192, 203),# 粉
            (0, 255, 255),  # 青
        ]
        
        self.size_slider_rect = pygame.Rect(20, 350, 110, 20)
        self.size_value = 30
        
        self.action_buttons = [
            {'action': 'delete', 'label': '删除选中'},
            {'action': 'clear', 'label': '清空画布'},
            {'action': 'save', 'label': '保存图片'}
        ]
        
        self.button_height = 35
        self.button_padding = 8
        
        self.title_y = 60
        self.shape_button_start_y = 90
        self.color_title_y = 280
        self.color_button_start_y = 300
        self.color_button_size = 28
        self.color_button_gap = 4
        self.size_title_y = 380
        self.action_button_start_y = 420
    
    def get_chinese_font(self, size):
        font_paths = [
            'msyh.ttc',
            'simsun.ttc',
            'simhei.ttf',
            'STSong.ttf',
            'STHeiti.ttf'
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                return pygame.font.Font(font_path, size)
        
        font_dirs = [
            'C:/Windows/Fonts/',
            'C:/Windows/WinSxS/'
        ]
        
        for font_dir in font_dirs:
            for font_path in font_paths:
                full_path = os.path.join(font_dir, font_path)
                if os.path.exists(full_path):
                    return pygame.font.Font(full_path, size)
        
        return pygame.font.Font(None, size)
    
    def draw(self, current_shape_type, current_color, current_size):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        
        title_surface = self.font.render('素材工具栏', True, self.text_color)
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, self.title_y))
        
        y = self.shape_button_start_y
        for btn in self.shape_buttons:
            btn_rect = pygame.Rect(10, y, self.width - 20, self.button_height)
            if btn['type'] == current_shape_type:
                pygame.draw.rect(self.screen, self.button_selected_color, btn_rect, border_radius=5)
            else:
                pygame.draw.rect(self.screen, self.button_color, btn_rect, border_radius=5)
            
            text_surface = self.font.render(btn['label'], True, self.text_color)
            self.screen.blit(text_surface, (btn_rect.centerx - text_surface.get_width() // 2, 
                                           btn_rect.centery - text_surface.get_height() // 2))
            y += self.button_height + self.button_padding
        
        color_title = self.font.render('颜色选择', True, self.text_color)
        self.screen.blit(color_title, (20, self.color_title_y))
        
        x = 20
        y_color = self.color_button_start_y
        for color in self.color_buttons:
            color_rect = pygame.Rect(x, y_color, self.color_button_size, self.color_button_size)
            pygame.draw.rect(self.screen, color, color_rect, border_radius=3)
            if color == current_color:
                pygame.draw.rect(self.screen, (255, 255, 255), color_rect, 2, border_radius=3)
            x += self.color_button_size + self.color_button_gap
            if x + self.color_button_size > self.width - 20:
                x = 20
                y_color += self.color_button_size + self.color_button_gap
        
        size_title = self.font.render(f'大小: {current_size}', True, self.text_color)
        self.screen.blit(size_title, (20, self.size_title_y))
        
        pygame.draw.rect(self.screen, (60, 60, 60), self.size_slider_rect)
        slider_pos = ((current_size - 10) / 80) * (self.size_slider_rect.width - 10)
        pygame.draw.circle(self.screen, (100, 150, 200), 
                          (int(self.size_slider_rect.x + slider_pos + 5), self.size_slider_rect.centery), 8)
        
        y = self.action_button_start_y
        for btn in self.action_buttons:
            btn_rect = pygame.Rect(10, y, self.width - 20, self.button_height)
            pygame.draw.rect(self.screen, (80, 80, 80), btn_rect, border_radius=5)
            
            text_surface = self.font.render(btn['label'], True, self.text_color)
            self.screen.blit(text_surface, (btn_rect.centerx - text_surface.get_width() // 2, 
                                           btn_rect.centery - text_surface.get_height() // 2))
            y += self.button_height + self.button_padding
    
    def handle_click(self, pos, current_shape_type):
        x, y = pos
        
        if x > self.width or y < 50:
            return None, None
        
        y -= 50
        
        if y >= self.shape_button_start_y - 50 and y <= self.shape_button_start_y - 50 + (self.button_height + self.button_padding) * len(self.shape_buttons):
            btn_y = self.shape_button_start_y - 50
            for btn in self.shape_buttons:
                btn_rect = pygame.Rect(10, btn_y + 50, self.width - 20, self.button_height)
                if btn_rect.collidepoint(pos):
                    return 'shape', btn['type']
                btn_y += self.button_height + self.button_padding
        
        y_screen = y + 50
        if y_screen >= self.color_button_start_y and y_screen <= self.color_button_start_y + self.color_button_size * 2:
            x_btn = 20
            y_color = self.color_button_start_y
            for color in self.color_buttons:
                color_rect = pygame.Rect(x_btn, y_color, self.color_button_size, self.color_button_size)
                if color_rect.collidepoint(pos):
                    return 'color', color
                x_btn += self.color_button_size + self.color_button_gap
                if x_btn + self.color_button_size > self.width - 20:
                    x_btn = 20
                    y_color += self.color_button_size + self.color_button_gap
        
        if self.size_slider_rect.collidepoint(pos):
            relative_x = pos[0] - self.size_slider_rect.x
            new_size = int(10 + (relative_x / self.size_slider_rect.width) * 80)
            new_size = max(10, min(90, new_size))
            return 'size', new_size
        
        if y_screen >= self.action_button_start_y and y_screen <= self.action_button_start_y + (self.button_height + self.button_padding) * len(self.action_buttons):
            btn_y = self.action_button_start_y
            for btn in self.action_buttons:
                btn_rect = pygame.Rect(10, btn_y, self.width - 20, self.button_height)
                if btn_rect.collidepoint(pos):
                    return 'action', btn['action']
                btn_y += self.button_height + self.button_padding
        
        return None, None