import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, FONT_LARGE, FONT_MEDIUM, FONT_XLARGE, WHITE, BLACK, LIGHT_GRAY, MAX_HINTS

class Button:
    def __init__(self, x, y, width, height, text, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_hovered = False
    
    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        text_surface = FONT_MEDIUM.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_click(self, mouse_pos):
        if self.is_hovered and self.callback:
            self.callback()
            return True
        return False

class LevelButton:
    def __init__(self, x, y, width, height, level_num, level_name, is_unlocked, is_completed, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.level_num = level_num
        self.level_name = level_name
        self.is_unlocked = is_unlocked
        self.is_completed = is_completed
        self.callback = callback
        self.is_hovered = False
    
    def draw(self, screen):
        if self.is_unlocked:
            if self.is_completed:
                color = (0, 200, 0)
            else:
                color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        else:
            color = LIGHT_GRAY
        
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        if self.is_unlocked:
            num_text = FONT_LARGE.render(str(self.level_num), True, WHITE)
            num_rect = num_text.get_rect(center=(self.rect.centerx, self.rect.top + 15))
            screen.blit(num_text, num_rect)
            
            name_text = FONT_MEDIUM.render(self.level_name, True, WHITE)
            name_rect = name_text.get_rect(center=self.rect.center)
            name_rect.top = num_rect.bottom + 5
            screen.blit(name_text, name_rect)
            
            if self.is_completed:
                check_text = FONT_LARGE.render("✓", True, WHITE)
                check_rect = check_text.get_rect(center=(self.rect.centerx, self.rect.bottom - 15))
                screen.blit(check_text, check_rect)
        else:
            lock_text = FONT_LARGE.render("🔒", True, GRAY)
            lock_rect = lock_text.get_rect(center=self.rect.center)
            screen.blit(lock_text, lock_rect)
    
    def update(self, mouse_pos):
        if self.is_unlocked:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
        else:
            self.is_hovered = False
    
    def handle_click(self, mouse_pos):
        if self.is_unlocked and self.is_hovered and self.callback:
            self.callback(self.level_num - 1)
            return True
        return False

class UIManager:
    def __init__(self):
        self.buttons = []
        self.level_buttons = []
        self.current_screen = "menu"
    
    def show_menu(self):
        self.current_screen = "menu"
        self.buttons = []
        
        button_width = 200
        button_height = 50
        start_y = 180
        spacing = 40
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y,
            button_width,
            button_height,
            "开始游戏",
            self.on_start_game
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + spacing,
            button_width,
            button_height,
            "关卡选择",
            self.on_select_level
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + spacing * 2,
            button_width,
            button_height,
            "游戏规则",
            self.on_show_rules
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + spacing * 3,
            button_width,
            button_height,
            "退出游戏",
            self.on_quit
        ))
    
    def show_level_select(self, game_logic):
        self.current_screen = "level_select"
        self.buttons = []
        self.level_buttons = []
        
        button_width = 120
        button_height = 90
        cols = 4
        start_x = (SCREEN_WIDTH - button_width * cols - 20 * (cols - 1)) // 2
        start_y = 100
        
        total_levels = game_logic.get_total_levels()
        
        for i in range(total_levels):
            row = i // cols
            col = i % cols
            x = start_x + col * (button_width + 20)
            y = start_y + row * (button_height + 20)
            
            level_info = game_logic.get_level_info(i)
            is_unlocked = game_logic.is_level_unlocked(i)
            is_completed = False
            
            self.level_buttons.append(LevelButton(
                x, y, button_width, button_height,
                i + 1, level_info["name"],
                is_unlocked, is_completed,
                self.on_level_selected
            ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - 150) // 2,
            520,
            150,
            45,
            "返回菜单",
            self.on_back_to_menu
        ))
    
    def show_game_ui(self, hints_remaining=MAX_HINTS):
        self.current_screen = "game"
        self.buttons = []
        
        button_width = 140
        button_height = 45
        
        self.buttons.append(Button(
            SCREEN_WIDTH - button_width - 20,
            100,
            button_width,
            button_height,
            "重新开始",
            self.on_restart
        ))
        
        self.buttons.append(Button(
            SCREEN_WIDTH - button_width - 20,
            160,
            button_width,
            button_height,
            f"提示 ({hints_remaining})",
            self.on_hint
        ))
        
        self.buttons.append(Button(
            SCREEN_WIDTH - button_width - 20,
            220,
            button_width,
            button_height,
            "返回菜单",
            self.on_back_to_menu
        ))
    
    def show_win_dialog(self):
        self.current_screen = "win_dialog"
        self.buttons = []
        
        button_width = 160
        button_height = 50
        start_y = 420
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width * 3 - 30) // 2,
            start_y,
            button_width,
            button_height,
            "下一关",
            self.on_next_level
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width * 3 - 30) // 2 + button_width + 15,
            start_y,
            button_width,
            button_height,
            "重新挑战",
            self.on_restart
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width * 3 - 30) // 2 + (button_width + 15) * 2,
            start_y,
            button_width,
            button_height,
            "返回菜单",
            self.on_back_to_menu
        ))
    
    def show_rules(self):
        self.current_screen = "rules"
        self.buttons = []
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - 150) // 2,
            520,
            150,
            45,
            "返回菜单",
            self.on_back_to_menu
        ))
    
    def draw(self, screen):
        if self.current_screen == "menu":
            self.draw_menu(screen)
        elif self.current_screen == "level_select":
            self.draw_level_select(screen)
        elif self.current_screen == "game":
            self.draw_game_ui(screen)
        elif self.current_screen == "win_dialog":
            pass
        elif self.current_screen == "rules":
            self.draw_rules(screen)
    
    def draw_menu(self, screen):
        screen.fill((30, 30, 40))
        
        title = FONT_XLARGE.render("灯光迷阵", True, (255, 255, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        for button in self.buttons:
            button.draw(screen)
        
        intro_text = FONT_MEDIUM.render("点击灯格翻转自身及相邻格子，点亮所有灯即可通关！", True, WHITE)
        intro_rect = intro_text.get_rect(center=(SCREEN_WIDTH // 2, 520))
        screen.blit(intro_text, intro_rect)
    
    def draw_level_select(self, screen):
        screen.fill((30, 30, 40))
        
        title = FONT_LARGE.render("选择关卡", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        for button in self.level_buttons:
            button.draw(screen)
        
        for button in self.buttons:
            button.draw(screen)
    
    def draw_game_ui(self, screen):
        for button in self.buttons:
            button.draw(screen)
    
    def draw_rules(self, screen):
        screen.fill((30, 30, 40))
        
        title = FONT_LARGE.render("游戏规则", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        rules = [
            "🎮 游戏目标：",
            "   将棋盘上所有灯格全部点亮即可通关",
            "",
            "👆 操作方式：",
            "   点击任意灯格，会翻转该灯格及其",
            "   上下左右四个相邻灯格的亮灭状态",
            "",
            "💡 游戏提示：",
            "   灯格变亮为黄色，熄灭为灰色",
            "   鼠标悬浮时灯格会高亮显示",
            "   每局游戏有3次提示机会",
            "",
            "🏆 关卡系统：",
            "   通关当前关卡后解锁下一关",
            "   已解锁关卡可重复游玩"
        ]
        
        y = 100
        for rule in rules:
            text = FONT_MEDIUM.render(rule, True, WHITE)
            text_rect = text.get_rect(left=50, top=y)
            screen.blit(text, text_rect)
            y += 35
        
        for button in self.buttons:
            button.draw(screen)
    
    def update(self, mouse_pos):
        if self.current_screen == "menu" or self.current_screen == "game" or self.current_screen == "rules":
            for button in self.buttons:
                button.update(mouse_pos)
        elif self.current_screen == "level_select":
            for button in self.level_buttons:
                button.update(mouse_pos)
            for button in self.buttons:
                button.update(mouse_pos)
        elif self.current_screen == "win_dialog":
            for button in self.buttons:
                button.update(mouse_pos)
    
    def handle_click(self, mouse_pos):
        if self.current_screen == "menu" or self.current_screen == "game" or self.current_screen == "rules":
            for button in self.buttons:
                if button.handle_click(mouse_pos):
                    return True
        elif self.current_screen == "level_select":
            for button in self.level_buttons:
                if button.handle_click(mouse_pos):
                    return True
            for button in self.buttons:
                if button.handle_click(mouse_pos):
                    return True
        elif self.current_screen == "win_dialog":
            for button in self.buttons:
                if button.handle_click(mouse_pos):
                    return True
        return False
    
    def set_callbacks(self, start_game, select_level, show_rules, quit_game, back_to_menu, restart, hint, next_level):
        self.on_start_game = start_game
        self.on_select_level = select_level
        self.on_show_rules = show_rules
        self.on_quit = quit_game
        self.on_back_to_menu = back_to_menu
        self.on_restart = restart
        self.on_hint = hint
        self.on_next_level = next_level
    
    def update_hint_button(self, hints_remaining):
        for button in self.buttons:
            if button.text.startswith("提示"):
                button.text = f"提示 ({hints_remaining})"
                if hints_remaining <= 0:
                    button.callback = None
    
    def get_current_screen(self):
        return self.current_screen