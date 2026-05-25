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
        
        self.action_buttons = [
            {'action': 'delete', 'label': '删除选中'},
            {'action': 'clear', 'label': '清空画布'},
            {'action': 'save', 'label': '保存图片'}
        ]
        
        self.button_height = 35
        self.button_padding = 10
        self.section_spacing = 25
        
        self.color_button_size = 28
        self.color_button_gap = 4
        self.num_color_columns = 4
        self.num_color_rows = (len(self.color_buttons) + self.num_color_columns - 1) // self.num_color_columns
        
        self.slider_width = 110
        self.slider_height = 20
        
        self.rotate_slider_width = 110
        self.rotate_slider_height = 20
        self.rotate_slider_y_offset = 60
        
        self.scale_slider_width = 110
        self.scale_slider_height = 20
        self.scale_slider_y_offset = 110
        
        self.layout_positions()
    
    def layout_positions(self):
        y = 60
        self.title_y = y
        
        y += 30
        self.shape_button_start_y = y
        y += (self.button_height + self.button_padding) * len(self.shape_buttons)
        
        y += self.section_spacing
        self.color_title_y = y
        
        y += 20
        self.color_button_start_y = y
        y += (self.color_button_size + self.color_button_gap) * self.num_color_rows
        
        y += self.section_spacing
        self.size_title_y = y
        
        y += 20
        self.size_slider_y = y
        self.size_slider_rect = pygame.Rect(20, self.size_slider_y, self.slider_width, self.slider_height)
        
        y += 35
        self.rotate_title_y = y
        
        y += 20
        self.rotate_slider_y = y
        self.rotate_slider_rect = pygame.Rect(20, self.rotate_slider_y, self.rotate_slider_width, self.rotate_slider_height)
        
        y += 35
        self.scale_title_y = y
        
        y += 20
        self.scale_slider_y = y
        self.scale_slider_rect = pygame.Rect(20, self.scale_slider_y, self.scale_slider_width, self.scale_slider_height)
        
        y += self.section_spacing
        self.action_button_start_y = y
        y += (self.button_height + self.button_padding) * len(self.action_buttons)
        
        y += 10
        self.custom_color_button_y = y
        custom_color_rect = pygame.Rect(10, y, self.width - 20, self.button_height)
        pygame.draw.rect(self.screen, (80, 80, 80), custom_color_rect, border_radius=5)
        text_surface = self.font.render('自定义颜色', True, self.text_color)
        self.screen.blit(text_surface, (custom_color_rect.centerx - text_surface.get_width() // 2,
                                       custom_color_rect.centery - text_surface.get_height() // 2))
    
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
    
    def draw(self, current_shape_type, current_color, current_size, current_rotation=0, current_scale=1.0):
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
        row = 0
        for i, color in enumerate(self.color_buttons):
            color_rect = pygame.Rect(x, y_color, self.color_button_size, self.color_button_size)
            pygame.draw.rect(self.screen, color, color_rect, border_radius=3)
            if color == current_color:
                pygame.draw.rect(self.screen, (255, 255, 255), color_rect, 2, border_radius=3)
            x += self.color_button_size + self.color_button_gap
            if (i + 1) % self.num_color_columns == 0:
                x = 20
                row += 1
                y_color = self.color_button_start_y + row * (self.color_button_size + self.color_button_gap)
        
        size_title = self.font.render(f'大小: {current_size}', True, self.text_color)
        self.screen.blit(size_title, (20, self.size_title_y))
        
        pygame.draw.rect(self.screen, (60, 60, 60), self.size_slider_rect)
        slider_pos = ((current_size - 10) / 80) * (self.size_slider_rect.width - 10)
        pygame.draw.circle(self.screen, (100, 150, 200), 
                          (int(self.size_slider_rect.x + slider_pos + 5), self.size_slider_rect.centery), 8)
        
        rotation_label = self.font.render(f'旋转: {int(current_rotation)}°', True, self.text_color)
        self.screen.blit(rotation_label, (20, self.rotate_title_y))
        
        pygame.draw.rect(self.screen, (60, 60, 60), self.rotate_slider_rect)
        rotate_pos = ((current_rotation + 180) / 360) * (self.rotate_slider_rect.width - 10)
        rotate_pos = max(0, min(rotate_pos, self.rotate_slider_rect.width - 10))
        pygame.draw.circle(self.screen, (100, 150, 200), 
                          (int(self.rotate_slider_rect.x + rotate_pos + 5), self.rotate_slider_rect.centery), 8)
        
        scale_label = self.font.render(f'缩放: {int(current_scale * 100)}%', True, self.text_color)
        self.screen.blit(scale_label, (20, self.scale_title_y))
        
        pygame.draw.rect(self.screen, (60, 60, 60), self.scale_slider_rect)
        scale_pos = ((current_scale - 0.5) / 1.5) * (self.scale_slider_rect.width - 10)
        scale_pos = max(0, min(scale_pos, self.scale_slider_rect.width - 10))
        pygame.draw.circle(self.screen, (100, 150, 200), 
                          (int(self.scale_slider_rect.x + scale_pos + 5), self.scale_slider_rect.centery), 8)
        
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
        
        if y >= self.shape_button_start_y and y <= self.shape_button_start_y + (self.button_height + self.button_padding) * len(self.shape_buttons):
            btn_y = self.shape_button_start_y
            for btn in self.shape_buttons:
                btn_rect = pygame.Rect(10, btn_y, self.width - 20, self.button_height)
                if btn_rect.collidepoint(pos):
                    return 'shape', btn['type']
                btn_y += self.button_height + self.button_padding
        
        if y >= self.color_button_start_y and y <= self.color_button_start_y + (self.color_button_size + self.color_button_gap) * self.num_color_rows:
            x_btn = 20
            y_color = self.color_button_start_y
            row = 0
            for i, color in enumerate(self.color_buttons):
                color_rect = pygame.Rect(x_btn, y_color, self.color_button_size, self.color_button_size)
                if color_rect.collidepoint(pos):
                    return 'color', color
                x_btn += self.color_button_size + self.color_button_gap
                if (i + 1) % self.num_color_columns == 0:
                    x_btn = 20
                    row += 1
                    y_color = self.color_button_start_y + row * (self.color_button_size + self.color_button_gap)
        
        if self.size_slider_rect.collidepoint(pos):
            relative_x = pos[0] - self.size_slider_rect.x
            new_size = int(10 + (relative_x / self.size_slider_rect.width) * 80)
            new_size = max(10, min(90, new_size))
            return 'size', new_size
        
        if self.rotate_slider_rect.collidepoint(pos):
            relative_x = pos[0] - self.rotate_slider_rect.x
            new_rotation = -180 + (relative_x / self.rotate_slider_rect.width) * 360
            new_rotation = max(-180, min(180, new_rotation))
            return 'rotate', int(new_rotation)
        
        if self.scale_slider_rect.collidepoint(pos):
            relative_x = pos[0] - self.scale_slider_rect.x
            new_scale = 0.5 + (relative_x / self.scale_slider_rect.width) * 1.5
            new_scale = max(0.5, min(2.0, new_scale))
            return 'scale', round(new_scale, 2)
        
        if y >= self.action_button_start_y and y <= self.action_button_start_y + (self.button_height + self.button_padding) * len(self.action_buttons):
            btn_y = self.action_button_start_y
            for btn in self.action_buttons:
                btn_rect = pygame.Rect(10, btn_y, self.width - 20, self.button_height)
                if btn_rect.collidepoint(pos):
                    return 'action', btn['action']
                btn_y += self.button_height + self.button_padding
        
        return None, None