import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, FONT_LARGE, FONT_MEDIUM, FONT_XLARGE, FONT_SMALL, FONT_XXLARGE, WHITE, BLACK, LIGHT_GRAY, MAX_HINTS, GAME_MODES, DIFFICULTIES

class Button:
    def __init__(self, x, y, width, height, text, callback=None, icon=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_hovered = False
        self.icon = icon
    
    def draw(self, screen, theme):
        color = theme["button_hover"] if self.is_hovered else theme["button_color"]
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        if self.icon:
            icon_text = FONT_LARGE.render(self.icon, True, theme["text_color"])
            icon_rect = icon_text.get_rect(left=self.rect.left + 10, top=self.rect.top + 5)
            screen.blit(icon_text, icon_rect)
            text_x = self.rect.left + 45
        else:
            text_x = self.rect.left
        
        text_surface = FONT_MEDIUM.render(self.text, True, theme["text_color"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        if self.icon:
            text_rect.left = text_x
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_click(self, mouse_pos):
        if self.is_hovered and self.callback:
            self.callback()
            return True
        return False

class LevelButton:
    def __init__(self, x, y, width, height, level_num, level_name, is_unlocked, is_completed, stars, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.level_num = level_num
        self.level_name = level_name
        self.is_unlocked = is_unlocked
        self.is_completed = is_completed
        self.stars = stars
        self.callback = callback
        self.is_hovered = False
    
    def draw(self, screen, theme):
        if self.is_unlocked:
            if self.is_completed:
                color = (0, 200, 0)
            else:
                color = theme["button_hover"] if self.is_hovered else theme["button_color"]
        else:
            color = (80, 80, 80)
        
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        if self.is_unlocked:
            num_text = FONT_LARGE.render(str(self.level_num), True, theme["text_color"])
            num_rect = num_text.get_rect(center=(self.rect.centerx, self.rect.top + 15))
            screen.blit(num_text, num_rect)
            
            name_text = FONT_SMALL.render(self.level_name, True, theme["text_color"])
            name_rect = name_text.get_rect(center=self.rect.center)
            name_rect.top = num_rect.bottom + 5
            screen.blit(name_text, name_rect)
            
            star_x = self.rect.centerx - 25
            star_y = self.rect.bottom - 20
            for i in range(3):
                star = "★" if i < self.stars else "☆"
                star_text = FONT_MEDIUM.render(star, True, (255, 255, 0) if i < self.stars else (100, 100, 100))
                star_rect = star_text.get_rect(left=star_x + i * 20, top=star_y)
                screen.blit(star_text, star_rect)
        else:
            lock_text = FONT_LARGE.render("🔒", True, (100, 100, 100))
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

class ToggleButton(Button):
    def __init__(self, x, y, width, height, text, is_on, callback=None):
        super().__init__(x, y, width, height, text, callback)
        self.is_on = is_on
    
    def draw(self, screen, theme):
        color = theme["button_hover"] if self.is_hovered else theme["button_color"]
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        text_surface = FONT_MEDIUM.render(self.text, True, theme["text_color"])
        text_rect = text_surface.get_rect(left=self.rect.left + 15, centerx=self.rect.left + 15 + text_surface.get_width() // 2, centery=self.rect.centery)
        screen.blit(text_surface, text_rect)
        
        toggle_width = 40
        toggle_height = 20
        toggle_x = self.rect.right - toggle_width - 10
        toggle_y = self.rect.centery - toggle_height // 2
        
        toggle_bg = (100, 100, 100) if not self.is_on else (0, 200, 0)
        pygame.draw.rect(screen, toggle_bg, (toggle_x, toggle_y, toggle_width, toggle_height), border_radius=10)
        
        knob_x = toggle_x + 3 + (toggle_width - 14) * self.is_on
        pygame.draw.circle(screen, WHITE, (int(knob_x + 7), toggle_y + 10), 7)
    
    def toggle(self):
        self.is_on = not self.is_on
        if self.callback:
            self.callback(self.is_on)

class UIManager:
    def __init__(self):
        self.buttons = []
        self.level_buttons = []
        self.current_screen = "menu"
        self.theme = {
            "bg_color": (30, 30, 40),
            "button_color": (50, 150, 255),
            "button_hover": (70, 170, 255),
            "text_color": (255, 255, 255),
            "stats_bg": (200, 200, 200),
            "stats_text": (0, 0, 0)
        }
        
        self.on_start_game = None
        self.on_select_level = None
        self.on_show_rules = None
        self.on_quit = None
        self.on_back_to_menu = None
        self.on_restart = None
        self.on_hint = None
        self.on_next_level = None
        self.on_show_settings = None
        self.on_show_difficulty = None
        self.on_show_mode = None
        self.on_show_theme = None
        self.on_select_difficulty = None
        self.on_select_mode = None
        self.on_select_theme = None
        self.on_toggle_sound = None
        self.on_toggle_music = None
        self.on_toggle_animation = None
        self.on_clear_save = None
        self.on_continue_game = None
        
        self.current_difficulty = "normal"
        self.current_mode = "classic"
        self.current_theme_name = "classic"
        self.sound_enabled = True
        self.music_enabled = True
        self.animation_enabled = True
    
    def set_theme(self, theme):
        self.theme = theme
    
    def get_theme(self):
        return self.theme
    
    def set_callbacks(self, callbacks):
        self.on_start_game = callbacks.get("start_game")
        self.on_select_level = callbacks.get("select_level")
        self.on_show_rules = callbacks.get("show_rules")
        self.on_quit = callbacks.get("quit")
        self.on_back_to_menu = callbacks.get("back_to_menu")
        self.on_restart = callbacks.get("restart")
        self.on_hint = callbacks.get("hint")
        self.on_next_level = callbacks.get("next_level")
        self.on_show_settings = callbacks.get("show_settings")
        self.on_show_difficulty = callbacks.get("show_difficulty")
        self.on_show_mode = callbacks.get("show_mode")
        self.on_show_theme = callbacks.get("show_theme")
        self.on_select_difficulty = callbacks.get("select_difficulty")
        self.on_select_mode = callbacks.get("select_mode")
        self.on_select_theme = callbacks.get("select_theme")
        self.on_toggle_sound = callbacks.get("toggle_sound")
        self.on_toggle_music = callbacks.get("toggle_music")
        self.on_toggle_animation = callbacks.get("toggle_animation")
        self.on_clear_save = callbacks.get("clear_save")
        self.on_continue_game = callbacks.get("continue_game")
    
    def show_menu(self):
        self.current_screen = "menu"
        self.buttons = []
        
        button_width = 220
        button_height = 55
        start_y = 180
        spacing = 35
        
        if self.on_continue_game and self._has_progress():
            self.buttons.append(Button(
                (SCREEN_WIDTH - button_width) // 2,
                start_y,
                button_width,
                button_height,
                "继续游戏",
                self.on_continue_game,
                "▶"
            ))
            actual_start_y = start_y + spacing
        else:
            actual_start_y = start_y
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            actual_start_y,
            button_width,
            button_height,
            "开始游戏",
            self.on_start_game,
            "🎮"
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            actual_start_y + spacing,
            button_width,
            button_height,
            "关卡选择",
            self.on_select_level,
            "📋"
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            actual_start_y + spacing * 2,
            button_width,
            button_height,
            "难度选择",
            self.on_show_difficulty,
            "⚡"
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            actual_start_y + spacing * 3,
            button_width,
            button_height,
            "主题切换",
            self.on_show_theme,
            "🎨"
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            actual_start_y + spacing * 4,
            button_width,
            button_height,
            "游戏设置",
            self.on_show_settings,
            "⚙️"
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            actual_start_y + spacing * 5,
            button_width,
            button_height,
            "游戏规则",
            self.on_show_rules,
            "📖"
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            actual_start_y + spacing * 6,
            button_width,
            button_height,
            "退出游戏",
            self.on_quit,
            "❌"
        ))
    
    def _has_progress(self):
        return False
    
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
            is_completed = game_logic.get_level_stars(i) > 0
            stars = game_logic.get_level_stars(i)
            
            self.level_buttons.append(LevelButton(
                x, y, button_width, button_height,
                i + 1, level_info["name"],
                is_unlocked, is_completed, stars,
                self._on_level_selected
            ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - 150) // 2,
            520,
            150,
            45,
            "返回菜单",
            self.on_back_to_menu
        ))
    
    def _on_level_selected(self, level_index):
        if self.on_start_game:
            self.on_start_game(level_index)
    
    def show_game_ui(self, hints_remaining=MAX_HINTS):
        self.current_screen = "game"
        self.buttons = []
        
        button_width = 130
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
    
    def show_win_dialog(self, stars=1):
        self.current_screen = "win_dialog"
        self.buttons = []
        self.win_stars = stars
        
        button_width = 150
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
    
    def show_failure_dialog(self, reason=""):
        self.current_screen = "failure_dialog"
        self.buttons = []
        self.failure_reason = reason
        
        button_width = 150
        button_height = 50
        start_y = 420
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width * 2 - 20) // 2,
            start_y,
            button_width,
            button_height,
            "重新挑战",
            self.on_restart
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width * 2 - 20) // 2 + button_width + 20,
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
    
    def show_settings(self):
        self.current_screen = "settings"
        self.buttons = []
        
        button_width = 280
        button_height = 45
        start_y = 150
        spacing = 35
        
        self.buttons.append(ToggleButton(
            (SCREEN_WIDTH - button_width) // 2,
            start_y,
            button_width,
            button_height,
            "音效",
            self.sound_enabled,
            self.on_toggle_sound
        ))
        
        self.buttons.append(ToggleButton(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + spacing,
            button_width,
            button_height,
            "背景音乐",
            self.music_enabled,
            self.on_toggle_music
        ))
        
        self.buttons.append(ToggleButton(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + spacing * 2,
            button_width,
            button_height,
            "动画效果",
            self.animation_enabled,
            self.on_toggle_animation
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + spacing * 3,
            button_width,
            button_height,
            "清除存档",
            self._confirm_clear_save,
            "🗑️"
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - 150) // 2,
            520,
            150,
            45,
            "返回菜单",
            self.on_back_to_menu
        ))
    
    def _confirm_clear_save(self):
        self.current_screen = "confirm_clear"
        self.buttons = []
        
        button_width = 150
        button_height = 50
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width * 2 - 30) // 2,
            350,
            button_width,
            button_height,
            "确认清除",
            self.on_clear_save
        ))
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - button_width * 2 - 30) // 2 + button_width + 30,
            350,
            button_width,
            button_height,
            "取消",
            self.show_settings
        ))
    
    def show_difficulty_select(self):
        self.current_screen = "difficulty_select"
        self.buttons = []
        
        button_width = 200
        button_height = 55
        start_y = 180
        spacing = 30
        
        for key, diff in DIFFICULTIES.items():
            is_selected = self.current_difficulty == key
            
            btn = Button(
                (SCREEN_WIDTH - button_width) // 2,
                start_y,
                button_width,
                button_height,
                diff["name"],
                lambda k=key: self._select_difficulty(k)
            )
            btn.is_selected = is_selected
            self.buttons.append(btn)
            start_y += spacing
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - 150) // 2,
            520,
            150,
            45,
            "返回菜单",
            self.on_back_to_menu
        ))
    
    def _select_difficulty(self, difficulty):
        self.current_difficulty = difficulty
        if self.on_select_difficulty:
            self.on_select_difficulty(difficulty)
        self.show_menu()
    
    def show_mode_select(self):
        self.current_screen = "mode_select"
        self.buttons = []
        
        button_width = 250
        button_height = 60
        start_y = 180
        spacing = 35
        
        for key, mode in GAME_MODES.items():
            is_selected = self.current_mode == key
            
            btn = Button(
                (SCREEN_WIDTH - button_width) // 2,
                start_y,
                button_width,
                button_height,
                mode["name"],
                lambda k=key: self._select_mode(k)
            )
            btn.is_selected = is_selected
            btn.mode_desc = mode["description"]
            self.buttons.append(btn)
            start_y += spacing
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - 150) // 2,
            520,
            150,
            45,
            "返回菜单",
            self.on_back_to_menu
        ))
    
    def _select_mode(self, mode):
        self.current_mode = mode
        if self.on_select_mode:
            self.on_select_mode(mode)
        self.show_menu()
    
    def show_theme_select(self, themes):
        self.current_screen = "theme_select"
        self.buttons = []
        self.themes = themes
        
        button_width = 140
        button_height = 140
        cols = 4
        start_x = (SCREEN_WIDTH - button_width * cols - 20 * (cols - 1)) // 2
        start_y = 120
        
        for i, (key, theme) in enumerate(themes.items()):
            row = i // cols
            col = i % cols
            x = start_x + col * (button_width + 20)
            y = start_y + row * (button_height + 20)
            
            btn = Button(x, y, button_width, button_height, theme["name"], 
                       lambda k=key: self._select_theme(k))
            btn.theme_key = key
            btn.theme_color = theme["cell_on"]
            btn.is_selected = self.current_theme_name == key
            self.buttons.append(btn)
        
        self.buttons.append(Button(
            (SCREEN_WIDTH - 150) // 2,
            520,
            150,
            45,
            "返回菜单",
            self.on_back_to_menu
        ))
    
    def _select_theme(self, theme_name):
        self.current_theme_name = theme_name
        if self.on_select_theme:
            self.on_select_theme(theme_name)
        self.show_menu()
    
    def draw(self, screen):
        screen.fill(self.theme["bg_color"])
        
        if self.current_screen == "menu":
            self.draw_menu(screen)
        elif self.current_screen == "level_select":
            self.draw_level_select(screen)
        elif self.current_screen == "game":
            pass
        elif self.current_screen == "win_dialog":
            pass
        elif self.current_screen == "failure_dialog":
            pass
        elif self.current_screen == "rules":
            self.draw_rules(screen)
        elif self.current_screen == "settings":
            self.draw_settings(screen)
        elif self.current_screen == "confirm_clear":
            self.draw_confirm_clear(screen)
        elif self.current_screen == "difficulty_select":
            self.draw_difficulty_select(screen)
        elif self.current_screen == "mode_select":
            self.draw_mode_select(screen)
        elif self.current_screen == "theme_select":
            self.draw_theme_select(screen)
        
        for button in self.buttons:
            button.draw(screen, self.theme)
    
    def draw_menu(self, screen):
        title = FONT_XXLARGE.render("灯光迷阵", True, (255, 255, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        subtitle = FONT_MEDIUM.render("点击灯格翻转自身及相邻格子，点亮所有灯即可通关！", True, self.theme["text_color"])
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 530))
        screen.blit(subtitle, subtitle_rect)
    
    def draw_level_select(self, screen):
        title = FONT_LARGE.render("选择关卡", True, self.theme["text_color"])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        for button in self.level_buttons:
            button.draw(screen, self.theme)
    
    def draw_rules(self, screen):
        title = FONT_LARGE.render("游戏规则", True, self.theme["text_color"])
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
            "🧱 特殊格子：",
            "   障碍格子（灰色）：无法点击和翻转",
            "   冰冻格子（蓝色）：状态固定，不可翻转",
            "",
            "💡 游戏提示：",
            "   灯格变亮为黄色，熄灭为灰色",
            "   鼠标悬浮时灯格会高亮显示",
            "",
            "🏆 星级评价：",
            "   根据用时和步数获得1-3星评价",
            "   挑战更高难度获取更多星星！"
        ]
        
        y = 100
        for rule in rules:
            text = FONT_MEDIUM.render(rule, True, self.theme["text_color"])
            text_rect = text.get_rect(left=50, top=y)
            screen.blit(text, text_rect)
            y += 35
    
    def draw_settings(self, screen):
        title = FONT_LARGE.render("游戏设置", True, self.theme["text_color"])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        note_text = FONT_SMALL.render("清除存档将删除所有游戏进度，此操作不可撤销", True, (255, 100, 100))
        note_rect = note_text.get_rect(center=(SCREEN_WIDTH // 2, 340))
        screen.blit(note_text, note_rect)
    
    def draw_confirm_clear(self, screen):
        title = FONT_LARGE.render("确认清除存档？", True, (255, 100, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(title, title_rect)
        
        desc_text = FONT_MEDIUM.render("此操作将删除所有关卡进度和星级评价", True, self.theme["text_color"])
        desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(desc_text, desc_rect)
    
    def draw_difficulty_select(self, screen):
        title = FONT_LARGE.render("选择难度", True, self.theme["text_color"])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        for button in self.buttons[:-1]:
            if button.is_selected:
                pygame.draw.rect(screen, (0, 200, 0), button.rect, 3, border_radius=8)
    
    def draw_mode_select(self, screen):
        title = FONT_LARGE.render("选择游戏模式", True, self.theme["text_color"])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        for button in self.buttons[:-1]:
            if button.is_selected:
                pygame.draw.rect(screen, (0, 200, 0), button.rect, 3, border_radius=8)
            
            if hasattr(button, 'mode_desc'):
                desc_text = FONT_SMALL.render(button.mode_desc, True, (150, 150, 150))
                desc_rect = desc_text.get_rect(center=(button.rect.centerx, button.rect.bottom + 10))
                screen.blit(desc_text, desc_rect)
    
    def draw_theme_select(self, screen):
        title = FONT_LARGE.render("选择主题", True, self.theme["text_color"])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        for button in self.buttons[:-1]:
            if hasattr(button, 'theme_color'):
                preview_rect = pygame.Rect(button.rect.left + 10, button.rect.top + 10, 
                                         button.rect.width - 20, button.rect.height - 50)
                pygame.draw.rect(screen, button.theme_color, preview_rect, border_radius=5)
                
                if button.is_selected:
                    pygame.draw.rect(screen, (0, 200, 0), button.rect, 3, border_radius=8)
    
    def update(self, mouse_pos):
        for button in self.buttons:
            button.update(mouse_pos)
        
        if self.current_screen == "level_select":
            for button in self.level_buttons:
                button.update(mouse_pos)
    
    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if button.handle_click(mouse_pos):
                return True
        
        if self.current_screen == "level_select":
            for button in self.level_buttons:
                if button.handle_click(mouse_pos):
                    return True
        
        return False
    
    def get_current_screen(self):
        return self.current_screen
    
    def update_hint_button(self, hints_remaining):
        for button in self.buttons:
            if hasattr(button, 'text') and button.text.startswith("提示"):
                button.text = f"提示 ({hints_remaining})"
                if hints_remaining <= 0:
                    button.callback = None
    
    def set_sound_enabled(self, enabled):
        self.sound_enabled = enabled
    
    def set_music_enabled(self, enabled):
        self.music_enabled = enabled
    
    def set_animation_enabled(self, enabled):
        self.animation_enabled = enabled