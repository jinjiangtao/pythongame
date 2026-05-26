import random

class PropManager:
    def __init__(self):
        self.props = {
            "hint": {"name": "提示", "icon": "💡", "description": "显示一个未点亮的灯格"},
            "reset": {"name": "重置", "icon": "🔄", "description": "重置当前关卡"},
            "random": {"name": "随机", "icon": "🎲", "description": "随机点亮一些灯格"}
        }
        
        self.available_props = {
            "hint": 3,
            "reset": 1,
            "random": 2
        }
    
    def get_props(self):
        return self.props
    
    def get_available_count(self, prop_name):
        return self.available_props.get(prop_name, 0)
    
    def use_prop(self, prop_name, game_logic):
        if self.available_props.get(prop_name, 0) <= 0:
            return None
        
        self.available_props[prop_name] -= 1
        
        if prop_name == "hint":
            return self._use_hint(game_logic)
        elif prop_name == "reset":
            return self._use_reset(game_logic)
        elif prop_name == "random":
            return self._use_random(game_logic)
        
        return None
    
    def _use_hint(self, game_logic):
        for row in game_logic.cells:
            for cell in row:
                if not cell.is_on and not cell.is_obstacle and not cell.is_frozen:
                    return (cell.row, cell.col)
        return None
    
    def _use_reset(self, game_logic):
        game_logic.reset_level()
        return "reset"
    
    def _use_random(self, game_logic):
        size = game_logic.get_grid_size()
        cells_to_toggle = random.randint(1, min(3, size))
        
        for _ in range(cells_to_toggle):
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            
            if game_logic.cells[row][col].is_obstacle:
                continue
            
            game_logic.toggle_cell(row, col)
        
        return "random"
    
    def add_prop(self, prop_name, count=1):
        if prop_name in self.available_props:
            self.available_props[prop_name] += count
    
    def reset_props(self, hint_count=3):
        self.available_props = {
            "hint": hint_count,
            "reset": 1,
            "random": 2
        }
    
    def set_hint_count(self, count):
        self.available_props["hint"] = count

class PropButton:
    def __init__(self, x, y, width, height, prop_name, prop_info, callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.prop_name = prop_name
        self.prop_info = prop_info
        self.callback = callback
        self.is_hovered = False
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen, theme, available_count):
        color = theme["button_hover"] if self.is_hovered else theme["button_color"]
        
        if available_count <= 0:
            color = (100, 100, 100)
        
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        icon_text = FONT_LARGE.render(self.prop_info["icon"], True, theme["text_color"])
        icon_rect = icon_text.get_rect(left=self.x + 10, top=self.y + 5)
        screen.blit(icon_text, icon_rect)
        
        name_text = FONT_SMALL.render(self.prop_info["name"], True, theme["text_color"])
        name_rect = name_text.get_rect(left=self.x + 10, top=self.y + self.height - 25)
        screen.blit(name_text, name_rect)
        
        count_text = FONT_MEDIUM.render(f"x{available_count}", True, theme["text_color"])
        count_rect = count_text.get_rect(right=self.x + self.width - 10, centerx=self.x + self.width - 10, centery=self.y + self.height // 2)
        screen.blit(count_text, count_rect)
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_click(self, mouse_pos, available_count):
        if self.is_hovered and self.callback and available_count > 0:
            self.callback(self.prop_name)
            return True
        return False

import pygame
from config import FONT_LARGE, FONT_MEDIUM, FONT_SMALL