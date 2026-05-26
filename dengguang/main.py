import pygame
import sys
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "灯光迷阵"

pygame.init()

def get_chinese_font():
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "/Library/Fonts/SimHei.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path
    return None

CHINESE_FONT_PATH = get_chinese_font()
FONT_LARGE = pygame.font.Font(CHINESE_FONT_PATH, 36) if CHINESE_FONT_PATH else pygame.font.Font(None, 36)
FONT_MEDIUM = pygame.font.Font(CHINESE_FONT_PATH, 24) if CHINESE_FONT_PATH else pygame.font.Font(None, 24)
FONT_XLARGE = pygame.font.Font(CHINESE_FONT_PATH, 48) if CHINESE_FONT_PATH else pygame.font.Font(None, 48)
FONT_SMALL = pygame.font.Font(CHINESE_FONT_PATH, 20) if CHINESE_FONT_PATH else pygame.font.Font(None, 20)

from modules.game_logic import GameLogic
from modules.game_stats import GameStats
from modules.settings import Settings
from modules.save import SaveManager

class Button:
    def __init__(self, x, y, width, height, text, callback=None, icon=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.icon = icon
        self.is_hovered = False
    
    def draw(self, screen, theme):
        color = theme["button_hover"] if self.is_hovered else theme["button_color"]
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        
        if self.icon:
            icon_text = FONT_LARGE.render(self.icon, True, theme["text_color"])
            icon_rect = icon_text.get_rect(left=self.rect.left + 10, top=self.rect.top + 5)
            screen.blit(icon_text, icon_rect)
        
        text_surface = FONT_MEDIUM.render(self.text, True, theme["text_color"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_click(self, mouse_pos):
        if self.is_hovered and self.callback:
            self.callback()
            return True
        return False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.settings = Settings()
        self.save_manager = SaveManager()
        self.game_logic = GameLogic()
        self.game_stats = GameStats()
        
        self.game_logic.set_save_manager(self.save_manager)
        self.game_logic.set_settings(self.settings)
        
        self.current_screen = "menu"
        self.current_level = 0
        self.buttons = []
        self.create_menu_buttons()
    
    def create_menu_buttons(self):
        self.buttons = []
        button_width = 220
        button_height = 55
        start_y = 180
        spacing = 35
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.buttons.append(Button(button_x, start_y, button_width, button_height, "开始游戏", self.start_game, "🎮"))
        self.buttons.append(Button(button_x, start_y + spacing, button_width, button_height, "关卡选择", self.show_level_select, "📋"))
        self.buttons.append(Button(button_x, start_y + spacing * 2, button_width, button_height, "游戏设置", self.show_settings, "⚙️"))
        self.buttons.append(Button(button_x, start_y + spacing * 3, button_width, button_height, "游戏规则", self.show_rules, "📖"))
        self.buttons.append(Button(button_x, start_y + spacing * 4, button_width, button_height, "退出游戏", self.quit_game, "❌"))
    
    def start_game(self, level_index=0):
        print(f"开始游戏，关卡: {level_index}")
        self.current_level = level_index
        self.game_logic.init_board(SCREEN_WIDTH, SCREEN_HEIGHT, level_index)
        self.game_stats.reset()
        self.game_stats.start_timer()
        self.current_screen = "game"
    
    def show_level_select(self):
        print("显示关卡选择")
        self.current_screen = "level_select"
    
    def show_settings(self):
        print("显示设置")
        self.current_screen = "settings"
    
    def show_rules(self):
        print("显示规则")
        self.current_screen = "rules"
    
    def quit_game(self):
        pygame.quit()
        sys.exit()
    
    def back_to_menu(self):
        self.current_screen = "menu"
        self.create_menu_buttons()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.current_screen == "menu":
                    for button in self.buttons:
                        if button.handle_click(mouse_pos):
                            break
                
                elif self.current_screen == "game":
                    if self.game_logic.handle_click(mouse_pos):
                        self.game_stats.increment_steps()
                        
                        if self.game_logic.check_win():
                            self.current_screen = "win"
                    
                    back_button_rect = pygame.Rect(SCREEN_WIDTH - 130, 10, 120, 40)
                    if back_button_rect.collidepoint(mouse_pos):
                        self.back_to_menu()
                
                elif self.current_screen == "settings":
                    back_button_rect = pygame.Rect((SCREEN_WIDTH - 150) // 2, 520, 150, 45)
                    if back_button_rect.collidepoint(mouse_pos):
                        self.back_to_menu()
                    
                    options = ["sound", "music", "animation"]
                    for i, opt in enumerate(options):
                        y = 150 + i * 60
                        option_rect = pygame.Rect(150, y, 500, 45)
                        if option_rect.collidepoint(mouse_pos):
                            if opt == "sound":
                                self.settings.toggle_sound()
                                print(f"音效: {'开启' if self.settings.sound_enabled else '关闭'}")
                            elif opt == "music":
                                self.settings.toggle_music()
                                print(f"音乐: {'开启' if self.settings.music_enabled else '关闭'}")
                            elif opt == "animation":
                                self.settings.toggle_animation()
                                print(f"动画: {'开启' if self.settings.animation_enabled else '关闭'}")
                            break
                
                elif self.current_screen in ["level_select", "rules", "win"]:
                    back_button_rect = pygame.Rect((SCREEN_WIDTH - 150) // 2, 520, 150, 45)
                    if back_button_rect.collidepoint(mouse_pos):
                        self.back_to_menu()
                
                elif self.current_screen == "level_select":
                    total_levels = self.game_logic.get_total_levels()
                    cols = 4
                    for i in range(total_levels):
                        row = i // cols
                        col = i % cols
                        x = 100 + col * 180
                        y = 120 + row * 120
                        level_rect = pygame.Rect(x, y, 120, 90)
                        if level_rect.collidepoint(mouse_pos) and self.game_logic.is_level_unlocked(i):
                            self.start_game(i)
                            break
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.current_screen == "menu":
            for button in self.buttons:
                button.update(mouse_pos)
        
        elif self.current_screen == "game":
            self.game_logic.update_hover(mouse_pos)
            self.game_stats.update()
    
    def draw(self):
        theme = self.settings.get_theme()
        self.screen.fill(theme["bg_color"])
        
        if self.current_screen == "menu":
            title = FONT_XLARGE.render("灯光迷阵", True, (255, 255, 0))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
            self.screen.blit(title, title_rect)
            
            for button in self.buttons:
                button.draw(self.screen, theme)
        
        elif self.current_screen == "game":
            stats_bg = pygame.Rect(0, 0, SCREEN_WIDTH, 60)
            pygame.draw.rect(self.screen, (200, 200, 200), stats_bg)
            
            level_info = self.game_logic.get_level_info(self.current_level)
            level_name = level_info["name"] if level_info else "未知关卡"
            
            level_text = FONT_MEDIUM.render(f"关卡: {level_name}", True, (0, 0, 0))
            self.screen.blit(level_text, (20, 15))
            
            steps_text = FONT_MEDIUM.render(f"步数: {self.game_stats.get_steps()}", True, (0, 0, 0))
            self.screen.blit(steps_text, (180, 15))
            
            time_text = FONT_MEDIUM.render(f"时间: {self.game_stats.format_time()}", True, (0, 0, 0))
            self.screen.blit(time_text, (330, 15))
            
            back_button = pygame.Rect(SCREEN_WIDTH - 130, 10, 120, 40)
            pygame.draw.rect(self.screen, theme["button_color"], back_button, border_radius=8)
            back_text = FONT_MEDIUM.render("返回菜单", True, theme["text_color"])
            back_rect = back_text.get_rect(center=back_button.center)
            self.screen.blit(back_text, back_rect)
            
            self.game_logic.draw(self.screen)
        
        elif self.current_screen == "level_select":
            title = FONT_LARGE.render("选择关卡", True, theme["text_color"])
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(title, title_rect)
            
            total_levels = self.game_logic.get_total_levels()
            cols = 4
            for i in range(total_levels):
                row = i // cols
                col = i % cols
                x = 100 + col * 180
                y = 120 + row * 120
                
                level_info = self.game_logic.get_level_info(i)
                is_unlocked = self.game_logic.is_level_unlocked(i)
                
                color = theme["button_color"] if is_unlocked else (80, 80, 80)
                pygame.draw.rect(self.screen, color, (x, y, 120, 90), border_radius=8)
                
                if is_unlocked:
                    num_text = FONT_LARGE.render(str(i + 1), True, theme["text_color"])
                    self.screen.blit(num_text, (x + 50, y + 10))
                    name_text = FONT_MEDIUM.render(level_info["name"], True, theme["text_color"])
                    name_rect = name_text.get_rect(center=(x + 60, y + 55))
                    self.screen.blit(name_text, name_rect)
            
            self.draw_back_button()
        
        elif self.current_screen == "settings":
            title = FONT_LARGE.render("游戏设置", True, theme["text_color"])
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(title, title_rect)
            
            options = [("音效", self.settings.sound_enabled), 
                       ("音乐", self.settings.music_enabled), 
                       ("动画", self.settings.animation_enabled)]
            for i, (opt, enabled) in enumerate(options):
                y = 150 + i * 60
                option_rect = pygame.Rect(150, y, 500, 45)
                
                color = (0, 200, 0) if enabled else theme["button_color"]
                pygame.draw.rect(self.screen, color, option_rect, border_radius=8)
                
                option_text = FONT_MEDIUM.render(opt, True, theme["text_color"])
                self.screen.blit(option_text, (170, y + 10))
                
                status_text = FONT_MEDIUM.render("开启" if enabled else "关闭", True, theme["text_color"])
                status_rect = status_text.get_rect(right=630, centery=y + 22)
                self.screen.blit(status_text, status_rect)
            
            self.draw_back_button()
        
        elif self.current_screen == "rules":
            title = FONT_LARGE.render("游戏规则", True, theme["text_color"])
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(title, title_rect)
            
            rules = [
                "🎮 点击灯格翻转自身及相邻格子",
                "🎯 点亮所有灯格即可通关",
                "🧱 障碍格子无法点击",
                "❄️ 冰冻格子状态固定",
                "💡 使用提示功能获得帮助"
            ]
            for i, rule in enumerate(rules):
                rule_text = FONT_MEDIUM.render(rule, True, theme["text_color"])
                self.screen.blit(rule_text, (50, 150 + i * 40))
            
            self.draw_back_button()
        
        elif self.current_screen == "win":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            win_text = FONT_XLARGE.render("🎉 恭喜通关！", True, (255, 255, 0))
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(win_text, win_rect)
            
            stats_text = FONT_MEDIUM.render(f"步数: {self.game_stats.get_steps()} | 时间: {self.game_stats.format_time()}", True, (255, 255, 255))
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
            self.screen.blit(stats_text, stats_rect)
            
            self.draw_back_button()
        
        pygame.display.flip()
    
    def draw_back_button(self):
        theme = self.settings.get_theme()
        back_button = pygame.Rect((SCREEN_WIDTH - 150) // 2, 520, 150, 45)
        pygame.draw.rect(self.screen, theme["button_color"], back_button, border_radius=8)
        back_text = FONT_MEDIUM.render("返回菜单", True, theme["text_color"])
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    game = Game()
    game.run()