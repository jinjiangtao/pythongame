import pygame
import config
import shapes

class Card:
    def __init__(self, index, shape_type):
        self.index = index
        self.shape_type = shape_type
        self.shape_color = config.SHAPE_COLORS[shape_type]
        self.x, self.y = config.get_card_position(index)
        self.rect = pygame.Rect(self.x, self.y, config.CARD_WIDTH, config.CARD_HEIGHT)
        self.is_flipped = False
        self.is_matched = False
        self.show_check = False
        self.check_timer = 0
    
    def flip(self):
        """翻转卡片"""
        if not self.is_matched:
            self.is_flipped = not self.is_flipped
    
    def match(self):
        """配对成功"""
        self.is_matched = True
        self.show_check = True
        self.check_timer = 500
    
    def update(self, dt):
        """更新卡片状态"""
        if self.show_check:
            self.check_timer -= dt
            if self.check_timer <= 0:
                self.show_check = False
    
    def draw(self, surface):
        """绘制卡片"""
        if self.is_matched:
            color = config.CARD_MATCHED_COLOR
            alpha = 128
        else:
            color = config.CARD_BACK_COLOR if not self.is_flipped else config.CARD_FRONT_COLOR
            alpha = 255
        
        card_surface = pygame.Surface((config.CARD_WIDTH, config.CARD_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(card_surface, (*color, alpha) if alpha < 255 else color, 
                        (0, 0, config.CARD_WIDTH, config.CARD_HEIGHT), border_radius=8)
        pygame.draw.rect(card_surface, (50, 50, 70), 
                        (0, 0, config.CARD_WIDTH, config.CARD_HEIGHT), 2, border_radius=8)
        
        if self.is_flipped or self.is_matched:
            center_x = config.CARD_WIDTH // 2
            center_y = config.CARD_HEIGHT // 2 - 5
            shapes.draw_shape(card_surface, self.shape_type, self.shape_color, (center_x, center_y), 70)
        
        if self.show_check:
            font = pygame.font.Font(None, 50)
            check_text = font.render("✓", True, config.ACCENT_COLOR)
            check_rect = check_text.get_rect(center=(config.CARD_WIDTH // 2, config.CARD_HEIGHT // 2 - 5))
            card_surface.blit(check_text, check_rect)
        
        surface.blit(card_surface, (self.x, self.y))
    
    def contains_point(self, pos):
        """检查点是否在卡片范围内"""
        return self.rect.collidepoint(pos)
    
    def reset(self):
        """重置卡片状态"""
        self.is_flipped = False
        self.is_matched = False
        self.show_check = False
        self.check_timer = 0
